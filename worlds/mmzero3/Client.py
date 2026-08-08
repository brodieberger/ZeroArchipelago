import json
import logging
import pkgutil
import time
from typing import TYPE_CHECKING, Dict, Any, List, Optional

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

logger = logging.getLogger("Client")
EWRAM_BASE = 0x02000000


# itemInbox holds u16s because item codes reach 301
INBOX_ELEMENT_SIZE = 2


class ApBlock:
    """Addresses of gAp's fields, read from ap_symbols.json which gets generated on every ROM compile.

    checkedLocations: game to AP client. One bit per location ID, set by the ROM when the player checks it.

    itemInbox (16 slots):  AP client to game. For when Archipelago grants an item.
    Client fills a slot and advances inboxWriteIndex, the ROM grants it and advances inboxReadIndex. Equal indices mean no item on either side.
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
        logger.error(
            "MMZero3: could not load ap_symbols.json (%s).", exc)
        return None


# ROM
ROM_NAME_ADDR           = 0x0A0

# Inventories
CHECKED_LOCS_INV_ADDR   = 0x371B8   # save.disk -- 180 disks, 4 disks per byte
DISK_BYTES              = 45
HP_ADDR                 = 0x38044   # written to apply a received death; never read

# How long a death we caused ourselves stays un-relayed. Only has to outlast the couple of polls
# between poking HP and the ROM counting the death; expires so a poke that somehow fails to kill
# cannot swallow a later real death.
DEATHLINK_WAIT_WINDOW   = 3.0

# The four Sunken Library data files, left out of the save.disk restore as they are level logic.
# Numbers are diskno == AP location: DISK_FILE_D 10, J 16, K 17, L 18
SKIP_DISK_RESTORE       = frozenset({10, 16, 17, 18})

class MMZero3Client(BizHawkClient):
    game = "Mega Man Zero 3"
    system = "GBA"
    patch_suffix = ".apmmzero3"

    def __init__(self):
        super().__init__()

        # State tracking
        self.player_warned = False

        # gAp stuff. `ap` is None only if ap_symbols.json failed to load.
        self.ap = load_ap_symbols()
        self.ap_disabled = False       # set true in case of a version mismatch between client and the ROM
        self.ap_handshake_logged = False
        self.ap_options_pushed = False  # right now is just easyExSkill written into gAp
        self.locations_reported = set()  # location IDs already forwarded to the server
        self.items_pushed = 0          # how much of items_received is in the game's RAM
        self.items_applied_seen = 0    # last gAp.itemsApplied; a drop means a reset

        # Options (overwritten from slot data)
        self.options_set = False
        self.required_disks = 80
        self.goal_type = 0  # 0 is for default (kill boss with enough disks), 1 is vanilla (just kill the boss)
        self.easy_ex_skill = 0

        # DeathLink
        self.death_link = False
        self.pending_death_link = False
        self.death_count_seen = None   # last gAp.deathCount; None until the mailbox is live
        self.suppress_death_until = 0.0  # deaths we caused ourselves, not to be relayed back

        # Item tracking
        self.received_index = 0

        # Inventories
        self.starting_weapon_codes = []  # TEMP: AP item codes for the seed's starting weapons


    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(ROM_NAME_ADDR, 12, "ROM")]))[0]).decode("ascii")
            if rom_name != "MEGAMANZERO3":
                return False  # Not a Mega Man Zero 3 ROM
        except bizhawk.RequestFailedError:
            return False  # Not able to get a response, say no for now

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True

        return True

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: Dict[str, Any]) -> None:
        if cmd == "Bounced" and "tags" in args:
            if "DeathLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
                self.on_deathlink(ctx)

    async def send_deathlink(self, ctx: "BizHawkClientContext") -> None:
        ctx.last_death_link = time.time()
        await ctx.send_death("Zero was destroyed.")

    def on_deathlink(self, ctx: "BizHawkClientContext") -> None:
        ctx.last_death_link = time.time()
        self.pending_death_link = True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:
            # ---- gAp startup test -------------------------------------------------------
            mailbox_live = False

            inbox_write = inbox_read = items_applied = 0
            final_cleared = False
            disks_owned = 0
            death_count = None
            in_gameplay = False

            if (self.ap is not None and not self.ap_disabled
                    and ctx.slot is not None and ctx.server_locations):
                (ready_bytes, version_bytes,
                 inbox_write_bytes, inbox_read_bytes, items_applied_bytes,
                 final_cleared_bytes, disks_owned_bytes,
                 death_count_bytes, in_gameplay_bytes) = await bizhawk.read(ctx.bizhawk_ctx, [
                    # Ready and version test
                    (self.ap.addr("ready"),        4, "Combined WRAM"),
                    (self.ap.addr("version"),      2, "Combined WRAM"),

                    # Item inbox, AP client to game.
                    # inboxWriteIndex is advanced as we hand items over
                    # The ROM advances inboxReadIndex once ApGrantItem() has applied them.
                    (self.ap.addr("inboxWriteIndex"), 1, "Combined WRAM"),
                    (self.ap.addr("inboxReadIndex"),  1, "Combined WRAM"),
                    (self.ap.addr("itemsApplied"),    2, "Combined WRAM"),

                    # Goal information, game to AP client.
                    (self.ap.addr("finalCleared"),    1, "Combined WRAM"),
                    (self.ap.addr("disksOwned"),      2, "Combined WRAM"),

                    # DeathLink facts, game to AP client.
                    (self.ap.addr("deathCount"),      2, "Combined WRAM"),
                    (self.ap.addr("inGameplay"),      1, "Combined WRAM"),
                ])

                # ApInit runs on the first Process_Game(), so check it to see if the game is still booting.
                if int.from_bytes(ready_bytes, "little") == self.ap.ready_value:
                    # Check if the game's version matches. If it matches, 
                    version = int.from_bytes(version_bytes, "little")
                    if version != self.ap.version:
                        self.ap_disabled = True
                        message = (f"ROM/client version mismatch: the ROM is AP interface version {version}, "
                                   f"this apworld is version {self.ap.version}. Please Generate a new game/ROM!.")
                        logger.error("MMZero3: %s", message)
                        await ctx.send_msgs([{"cmd": "Say", "text": f"[MMZ3] {message}"}])
                    else:
                        mailbox_live = True
                        inbox_write, inbox_read = inbox_write_bytes[0], inbox_read_bytes[0]
                        items_applied = int.from_bytes(items_applied_bytes, "little")
                        final_cleared = final_cleared_bytes[0] != 0
                        disks_owned = int.from_bytes(disks_owned_bytes, "little")
                        death_count = int.from_bytes(death_count_bytes, "little")
                        in_gameplay = in_gameplay_bytes[0] != 0

                        if not self.ap_handshake_logged:
                            logger.info("MMZero3: gAp mailbox live at 0x%06X, AP interface version %d.",
                                        self.ap.base + EWRAM_BASE, version)
                            self.ap_handshake_logged = True


            # ---- OTHER GAME STUFF ----------------------------------------------------------
            (collected_in_game,) = await bizhawk.read(ctx.bizhawk_ctx, [
                (CHECKED_LOCS_INV_ADDR, DISK_BYTES, "Combined WRAM"),   # save.disk
            ])

            # ---- options -------------------------------------------------------------
            if ctx.slot_data and not self.options_set:
                self.required_disks = ctx.slot_data.get("required_secret_disks", 80)
                self.goal_type = ctx.slot_data.get("goal", 0)
                self.easy_ex_skill = ctx.slot_data.get("easy_ex_skill", 0)
                self.death_link = bool(ctx.slot_data.get("death_link", 0))
                # Starting weapons are not AP items, but still have to be added to the game via the RAM
                starting_weapons = ctx.slot_data.get("starting_weapons", [])
                weapon_name_to_code = {"Buster": 224, "Z-Saber": 225,
                                       "Recoil Rod": 226, "Shield Boomerang": 227}
                self.starting_weapon_codes = [
                    weapon_name_to_code[name]
                    for name in starting_weapons
                    if name in weapon_name_to_code
                ]
                self.options_set = True

            # ApSendStageClear() decides the A+ rank check itself, so the ROM needs this option for logic reasons.
            # ApInit() defaults it off, so it is re-pushed after any handshake, not once a session.
            if mailbox_live and self.options_set and not self.ap_options_pushed:
                await bizhawk.write(ctx.bizhawk_ctx,
                                    [(self.ap.addr("easyExSkill"), [1 if self.easy_ex_skill else 0],
                                      "Combined WRAM")])
                self.ap_options_pushed = True

            # ---- read checked locations (game to AP client) -----------------------------
            if mailbox_live:
                checked_bits = (await bizhawk.read(
                    ctx.bizhawk_ctx,
                    [(self.ap.addr("checkedLocations"),
                      self.ap.count("checkedLocations"), "Combined WRAM")]))[0]

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
                    logger.debug("MMZero3: reported %d location(s): %s",
                                 len(newly_checked), newly_checked)

            # ---- push items (AP client to game) -----------------------------------------
            if mailbox_live:
                await self.push_items(ctx, inbox_write, inbox_read, items_applied)

            # ---- DeathLink -----------------------------------------------------------
            if self.death_link:
                await ctx.update_death_link(True)

            if mailbox_live:
                if self.death_count_seen is None:
                    # First sight of a live mailbox: adopt the count rather than treat every
                    # death so far as new. Also covers a client restart mid-session.
                    self.death_count_seen = death_count
                elif death_count > self.death_count_seen:
                    self.death_count_seen = death_count
                    if time.time() < self.suppress_death_until:
                        # The death we just caused by honouring someone else's. Relaying it
                        # would bounce back and forth around the group forever.
                        self.suppress_death_until = 0.0
                    elif "DeathLink" in ctx.tags:
                        await self.send_deathlink(ctx)
                elif death_count < self.death_count_seen:
                    # gAp lives in EWRAM, so loading a savestate rewinds the counter. Nobody
                    # died; re-baseline so the next real death still registers as an increase.
                    self.death_count_seen = death_count

            if self.pending_death_link and in_gameplay:
                self.pending_death_link = False
                self.suppress_death_until = time.time() + DEATHLINK_WAIT_WINDOW
                await bizhawk.write(ctx.bizhawk_ctx, [(HP_ADDR, [0, 0], "Combined WRAM")])

            # ---- goal ----------------------------------------------------------------
            if mailbox_live and final_cleared and not ctx.finished_game:
                if self.goal_type == 1 or disks_owned >= self.required_disks:
                    if self.goal_type == 1:
                        text = "Final stage cleared! Game completed!"
                    elif self.player_warned:
                        text = f"{disks_owned} Disks collected! Game completed!"
                    else:
                        extra_disks_collected = disks_owned - self.required_disks
                        text = (f"Final stage cleared with {disks_owned} Disks, "
                                f"{extra_disks_collected} more than needed!")
                    await ctx.send_msgs([
                        {"cmd": "Say", "text": text},
                        {"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL},
                    ])
                    ctx.finished_game = True
                elif not self.player_warned:
                    await ctx.send_msgs([
                        {"cmd": "Say", "text": f"Final stage cleared! You still need "
                                               f"{self.required_disks - disks_owned} more disks."},
                        {"cmd": "Say", "text": "Collect more disks and the goal will send itself."},
                        {"cmd": "Say", "text": "Do NOT save over your file after the credits!"} # TODO is this needed?
                    ])
                    self.player_warned = True

            await self.restore_collected_disks(ctx, collected_in_game)

        except bizhawk.RequestFailedError:
            pass

    async def restore_collected_disks(self, ctx, collected_in_game: bytes) -> None:
        """
        Keep save.disk synced with the locations the AP server says are checked.
        Basically ensures that disks that are collected don't show up in game again.

        Only the lower nibble (found) is touched. The upper nibble is the disks opened state
        """
        collected_after_restore = bytearray(collected_in_game)
        for location_id in ctx.checked_locations:
            if location_id in SKIP_DISK_RESTORE:
                continue
            if 1 <= location_id <= 180:
                disk_index = location_id - 1
                collected_after_restore[disk_index // 4] |= 1 << (disk_index % 4)

        if collected_after_restore != collected_in_game:
            await bizhawk.write(ctx.bizhawk_ctx, [
                (CHECKED_LOCS_INV_ADDR, list(collected_after_restore), "Combined WRAM"),
            ])

    async def push_items(self, ctx: "BizHawkClientContext",
                         inbox_write: int, inbox_read: int, items_applied: int) -> None:
        """Hand received items to the game through the itemInbox field."""
        slot_count = self.ap.count("itemInbox")
        wrap_mask = slot_count - 1
        max_items_waiting = slot_count - 1

        # Starting weapons go first
        every_code = self.starting_weapon_codes + [int(item.item) for item in ctx.items_received]

        # itemsApplied going backwards means the game rewound for any reason.
        if items_applied < self.items_applied_seen:
            logger.info("MMZero3: game rewound (applied %d -> %d); resuming from %d.",
                        self.items_applied_seen, items_applied, items_applied)
            self.items_pushed = min(items_applied, len(every_code))
            self.ap_options_pushed = False
        self.items_applied_seen = items_applied

        codes_to_push = every_code[self.items_pushed:]
        if not codes_to_push:
            return

        items_waiting = (inbox_write - inbox_read) & wrap_mask
        slots_free = max_items_waiting - items_waiting
        if slots_free <= 0:
            # Wait until there are slots free (next game watcher check)
            return

        writes = []
        next_slot = inbox_write
        pushing = min(slots_free, len(codes_to_push))
        for code in codes_to_push[:pushing]:
            writes.append((self.ap.addr("itemInbox") + next_slot * INBOX_ELEMENT_SIZE,
                           list(code.to_bytes(INBOX_ELEMENT_SIZE, "little")),
                           "Combined WRAM"))
            next_slot = (next_slot + 1) & wrap_mask  # loop back around

        writes.append((self.ap.addr("inboxWriteIndex"), [next_slot], "Combined WRAM"))
        await bizhawk.write(ctx.bizhawk_ctx, writes)

        self.items_pushed += pushing
        logger.debug("MMZero3: pushed %d item(s) to the game; %d still waiting.",
                     pushing, len(codes_to_push) - pushing)
