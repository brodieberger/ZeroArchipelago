import json
import logging
import pkgutil
import time
from typing import TYPE_CHECKING, Any, Dict, Optional

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from .Locations import location_data_table

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

logger = logging.getLogger("Client")

WRAM = "Combined WRAM"
EWRAM_BASE = 0x02000000

ROM_NAME_ADDR = 0x0A0
EXPECTED_ROM_NAME = "MEGAMANZERO3"

# save.disk: 180 disks packed 4 per byte, low nibble found / high nibble analysed.
CHECKED_LOCS_INV_ADDR = 0x371B8
DISK_BYTES = 45

# The four Sunken Library data files, left out as they are used in level logic.
SKIP_DISK_RESTORE = frozenset({10, 16, 17, 18})

# itemInbox uses u16s
INBOX_ELEMENT_SIZE = 2

# gAp.killRequest, matching ap.h.
AP_KILL_REQUESTED = 1

DEFAULT_REQUIRED_DISKS = 80
FINAL_STAGE_LOCATION = location_data_table["Complete Abandoned Research Laboratory"].address


class ApBlock:
    """gAp and its fields. Read from ap_symbols.json which is created when the ROM is compiled.

    checkedLocations is game -> client: one bit per location ID, set by the ROM.
    itemInbox is client -> game: the client fills a slot and advances inboxWriteIndex, the ROM grants it and advances inboxReadIndex. 
    Equal indices mean the inbox is empty.
    """

    def __init__(self, symbols: dict):
        ap_state = symbols["ap_state"]
        self.ready_value: int = symbols["ready"]  # what gAp.ready reads once the game is up
        self.version: int = symbols["version"]
        self.base: int = ap_state["address"] - EWRAM_BASE
        self._fields: dict = ap_state["fields"]

    def addr(self, field: str) -> int:
        return self.base + self._fields[field]["offset"]

    def count(self, field: str) -> int:
        """How many elements an array field holds (16 for itemInbox, 29 for checkedLocations)."""
        return self._fields[field]["count"]


def load_ap_symbols() -> Optional[ApBlock]:
    try:
        raw = pkgutil.get_data(__name__, "ap_symbols.json")
        if raw is None:
            raise FileNotFoundError("ap_symbols.json not found in the apworld")
        return ApBlock(json.loads(raw.decode("utf-8")))
    except Exception as exc:
        logger.error("MMZero3: could not load ap_symbols.json (%s).", exc)
        return None


class MMZero3Client(BizHawkClient):
    game = "Mega Man Zero 3"
    system = "GBA"
    patch_suffix = ".apmmzero3"

    def __init__(self):
        super().__init__()

        # gAp stuff. `ap` is None only if ap_symbols.json failed to load.
        self.ap = load_ap_symbols()
        self.ap_disabled = False        # latched on a ROM/client version mismatch
        self.ap_handshake_logged = False
        self.locations_reported = set()  # location IDs already forwarded to the server
        self.items_pushed = 0           # how much of items_received is in the game's RAM
        self.items_applied_seen = 0     # last gAp.itemsApplied; a drop means a rewind

        # Options, overwritten from slot data
        self.options_set = False
        self.required_disks = DEFAULT_REQUIRED_DISKS

        # DeathLink
        self.death_link = False
        self.pending_death_link = False
        self.death_count_seen = None    # last gAp.deathCount; None until the mailbox is live

        self.player_warned = False      # told the player the final stage needs more disks

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            rom_name = (await bizhawk.read(ctx.bizhawk_ctx, [(ROM_NAME_ADDR, 12, "ROM")]))[0]
        except bizhawk.RequestFailedError:
            return False
        if rom_name.decode("ascii", "replace") != EXPECTED_ROM_NAME:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:
            self.read_slot_data(ctx)
            if self.death_link:
                await ctx.update_death_link(True)

            mailbox = await self.read_mailbox(ctx)
            if mailbox is not None:
                await self.handle_checked_locations(ctx)
                await self.handle_received_items(ctx, mailbox)
                await self.handle_death_link(ctx, mailbox)
                await self.handle_goal(ctx, mailbox)

            await self.handle_collected_disks(ctx)
        except bizhawk.RequestFailedError:
            pass

    def read_slot_data(self, ctx: "BizHawkClientContext") -> None:
        if not ctx.slot_data or self.options_set:
            return
        self.required_disks = ctx.slot_data.get("required_secret_disks", DEFAULT_REQUIRED_DISKS)
        self.death_link = bool(ctx.slot_data.get("death_link", 0))
        self.options_set = True

    async def read_mailbox(self, ctx: "BizHawkClientContext") -> Optional[Dict[str, int]]:
        """One read of gAp. None means the ROM isn't ready.

        ApInit runs on the first Process_Game(), so `ready` not matching means the game is still booting.
        """
        if self.ap is None or self.ap_disabled or ctx.slot is None or not ctx.server_locations:
            return None

        ready, version, inbox_write, inbox_read, items_applied, disks_owned, death_count = \
            await bizhawk.read(ctx.bizhawk_ctx, [
                (self.ap.addr("ready"), 4, WRAM),
                (self.ap.addr("version"), 2, WRAM),
                (self.ap.addr("inboxWriteIndex"), 1, WRAM),
                (self.ap.addr("inboxReadIndex"), 1, WRAM),
                (self.ap.addr("itemsApplied"), 2, WRAM),
                (self.ap.addr("disksOwned"), 2, WRAM),
                (self.ap.addr("deathCount"), 2, WRAM),
            ])

        if int.from_bytes(ready, "little") != self.ap.ready_value:
            return None

        rom_version = int.from_bytes(version, "little")
        if rom_version != self.ap.version:
            self.ap_disabled = True
            message = (f"ROM/client version mismatch: the ROM is AP interface version "
                       f"{rom_version}, this apworld is version {self.ap.version}. "
                       f"Please generate a new game/ROM!")
            logger.error("MMZero3: %s", message)
            await ctx.send_msgs([{"cmd": "Say", "text": f"[MMZ3] {message}"}])
            return None

        if not self.ap_handshake_logged:
            logger.info("MMZero3: gAp mailbox live at 0x%06X, AP interface version %d.",
                        self.ap.base + EWRAM_BASE, rom_version)
            self.ap_handshake_logged = True

        return {
            "inbox_write": inbox_write[0],
            "inbox_read": inbox_read[0],
            "items_applied": int.from_bytes(items_applied, "little"),
            "disks_owned": int.from_bytes(disks_owned, "little"),
            "death_count": int.from_bytes(death_count, "little"),
        }

    async def handle_checked_locations(self, ctx: "BizHawkClientContext") -> None:
        """Forward every newly set bit of gAp.checkedLocations to the server."""
        checked_bits = (await bizhawk.read(ctx.bizhawk_ctx, [
            (self.ap.addr("checkedLocations"), self.ap.count("checkedLocations"), WRAM),
        ]))[0]

        newly_checked = []
        for location_id in range(len(checked_bits) * 8):
            if not checked_bits[location_id >> 3] & (1 << (location_id & 7)):
                continue
            if location_id in self.locations_reported:
                continue
            self.locations_reported.add(location_id)
            if location_id in ctx.server_locations:
                newly_checked.append(location_id)
            else:
                logger.warning("MMZero3: ROM reported unknown location id %d; ignoring.",
                               location_id)

        if newly_checked:
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": newly_checked}])
            logger.debug("MMZero3: reported %d location(s): %s", len(newly_checked), newly_checked)

    async def handle_received_items(self, ctx: "BizHawkClientContext",
                                    mailbox: Dict[str, int]) -> None:
        """Hand received items to the game through the itemInbox ring."""
        slot_count = self.ap.count("itemInbox")
        wrap_mask = slot_count - 1
        item_codes = [int(item.item) for item in ctx.items_received]

        # itemsApplied going backwards means a savestate or other reset
        items_applied = mailbox["items_applied"]
        if items_applied < self.items_applied_seen:
            logger.info("MMZero3: game rewound (applied %d -> %d); resuming from %d.",
                        self.items_applied_seen, items_applied, items_applied)
            self.items_pushed = min(items_applied, len(item_codes))
        self.items_applied_seen = items_applied

        codes_to_push = item_codes[self.items_pushed:]
        if not codes_to_push:
            return

        # One slot is always left free so one can always be read as empty.
        items_waiting = (mailbox["inbox_write"] - mailbox["inbox_read"]) & wrap_mask
        slots_free = (slot_count - 1) - items_waiting
        if slots_free <= 0:
            return  # try again next game_watcher run

        pushing = min(slots_free, len(codes_to_push))
        next_slot = mailbox["inbox_write"]
        writes = []
        for code in codes_to_push[:pushing]:
            writes.append((self.ap.addr("itemInbox") + next_slot * INBOX_ELEMENT_SIZE,
                           list(code.to_bytes(INBOX_ELEMENT_SIZE, "little")), WRAM))
            next_slot = (next_slot + 1) & wrap_mask
        writes.append((self.ap.addr("inboxWriteIndex"), [next_slot], WRAM))
        await bizhawk.write(ctx.bizhawk_ctx, writes)

        self.items_pushed += pushing
        logger.debug("MMZero3: pushed %d item(s) to the game; %d still waiting.",
                     pushing, len(codes_to_push) - pushing)

    async def handle_death_link(self, ctx: "BizHawkClientContext",
                                mailbox: Dict[str, int]) -> None:
        death_count = mailbox["death_count"]
        if self.death_count_seen is None:
            self.death_count_seen = death_count
        elif death_count > self.death_count_seen:
            self.death_count_seen = death_count
            if "DeathLink" in ctx.tags:
                await self.send_deathlink(ctx)
        elif death_count < self.death_count_seen:
            self.death_count_seen = death_count

        if self.pending_death_link:
            self.pending_death_link = False
            await bizhawk.write(ctx.bizhawk_ctx, [
                (self.ap.addr("killRequest"), [AP_KILL_REQUESTED], WRAM),
            ])

    async def handle_goal(self, ctx: "BizHawkClientContext", mailbox: Dict[str, int]) -> None:
        """
        Clear the final stage holding the required number of disks, set by a player option.
        """
        if ctx.finished_game:
            return
        if (FINAL_STAGE_LOCATION not in ctx.checked_locations
                and FINAL_STAGE_LOCATION not in self.locations_reported):
            return

        disks_owned = mailbox["disks_owned"]
        if disks_owned < self.required_disks:
            if not self.player_warned:
                self.player_warned = True
                await ctx.send_msgs([
                    {"cmd": "Say", "text": f"Final stage cleared! You still need "
                                           f"{self.required_disks - disks_owned} more disks."},
                    {"cmd": "Say", "text": "Collect more disks and the goal will send itself."},
                    {"cmd": "Say", "text": "Feel free to start new game plus, or load an earlier save!"},
                ])
            return

        if self.required_disks == 0:
            text = "Final stage cleared! Game completed!"
        elif self.player_warned:
            text = f"{disks_owned} Disks collected! Game completed!"
        else:
            text = (f"Final stage cleared with {disks_owned} Disks, "
                    f"{disks_owned - self.required_disks} more than needed!")
        await ctx.send_msgs([
            {"cmd": "Say", "text": text},
            {"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL},
        ])
        ctx.finished_game = True

    async def handle_collected_disks(self, ctx: "BizHawkClientContext") -> None:
        """Keep save.disk synced with the locations the server says are checked.

        That array is what stops a collected disk spawning again.
        """
        collected_in_game = (await bizhawk.read(ctx.bizhawk_ctx, [
            (CHECKED_LOCS_INV_ADDR, DISK_BYTES, WRAM),
        ]))[0]

        repaired = bytearray(collected_in_game)
        for location_id in ctx.checked_locations:
            if location_id in SKIP_DISK_RESTORE or not 1 <= location_id <= 180:
                continue
            disk_index = location_id - 1
            repaired[disk_index // 4] |= 1 << (disk_index % 4)

        if repaired != collected_in_game:
            await bizhawk.write(ctx.bizhawk_ctx, [(CHECKED_LOCS_INV_ADDR, list(repaired), WRAM)])

    async def send_deathlink(self, ctx: "BizHawkClientContext") -> None:
        ctx.last_death_link = time.time()
        await ctx.send_death("Zero was destroyed.")

    def on_deathlink(self, ctx: "BizHawkClientContext") -> None:
        ctx.last_death_link = time.time()
        self.pending_death_link = True

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: Dict[str, Any]) -> None:
        if cmd == "Bounced" and "tags" in args:
            if "DeathLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
                self.on_deathlink(ctx)
