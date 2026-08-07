import json
import logging
import pkgutil
import time
from typing import TYPE_CHECKING, Dict, Any, List, Optional

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from .Data import *

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

# Game state
CURRENT_LEVEL_ADDR      = 0x30164
RESULTS_SCREEN_ADDR     = 0x30165  # Also encodes level rank score on results screen
DEMO_SCREEN_ADDR        = 0x02AE2

# Inventories
CHECKED_LOCS_INV_ADDR   = 0x371B8
EREADER_BITFLAGS_ADDR   = 0x02438
EREADER_BYTE_MAP_ADDR   = 0x02474
HP_ADDR                 = 0x38044

# AP Related Counters
SYNC_COUNTER_ADDR       = 0x37342

class MMZero3Client(BizHawkClient):
    game = "Mega Man Zero 3"
    system = "GBA"
    patch_suffix = ".apmmzero3"

    def __init__(self):
        super().__init__()

        # State tracking
        self.prev_level_value = None
        self.in_results_screen = False
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
        self.sending_death_link = True

        # Item tracking
        self.received_index = 0
        self.collected_disks = 0

        # Inventories
        self.eReader_bitflag_inventory = [0] * 12
        self.eReader_byte_map_inventory = [0] * 10
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
        self.sending_death_link = True
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

            if (self.ap is not None and not self.ap_disabled
                    and ctx.slot is not None and ctx.server_locations):
                (ready_bytes, version_bytes,
                 inbox_write_bytes, inbox_read_bytes, items_applied_bytes) = await bizhawk.read(ctx.bizhawk_ctx, [
                    # Ready and version test
                    (self.ap.addr("ready"),        4, "Combined WRAM"),
                    (self.ap.addr("version"),      2, "Combined WRAM"),

                    # Item inbox, AP client to game.
                    # inboxWriteIndex is advanced as we hand items over
                    # The ROM advances inboxReadIndex once ApGrantItem() has applied them.
                    (self.ap.addr("inboxWriteIndex"), 1, "Combined WRAM"),
                    (self.ap.addr("inboxReadIndex"),  1, "Combined WRAM"),
                    (self.ap.addr("itemsApplied"),    2, "Combined WRAM"),
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

                        if not self.ap_handshake_logged:
                            logger.info("MMZero3: gAp mailbox live at 0x%06X, AP interface version %d.",
                                        self.ap.base + EWRAM_BASE, version)
                            self.ap_handshake_logged = True


            # ---- LEGACY GAME STUFF ----------------------------------------------------------
            # TODO Most of this has to go
            (
                level_data,
                results_screen,
                demo_screen,
                sync_counter,
                body_hp,
            ) = await bizhawk.read(ctx.bizhawk_ctx, [
                (CURRENT_LEVEL_ADDR,      1, "Combined WRAM"),  # Current level
                (RESULTS_SCREEN_ADDR,     1, "Combined WRAM"),  # Results screen flag
                (DEMO_SCREEN_ADDR,        1, "IWRAM"),          # Demo screen flag
                (SYNC_COUNTER_ADDR,       2, "Combined WRAM"),  # AP sync counter
                (HP_ADDR,                 2, "Combined WRAM"),  # Live Zero HP (DeathLink)
            ])

            # Don't process anything while on the title/menu screen.
            if level_data == b'\x00':
                self.prev_level_value = b'\x00'
                return

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
            # Will be changed to true if the gamestate needs to be synchronized.
            # Either on some update or the player changing stages.
            needs_sync = False

            # When the player transitions into the hub or a level, sync the inventory.
            # Level 0x11 is the resistance base hub.
            if self.prev_level_value != level_data:
                needs_sync = True

            # Force a sync if the counter doesn't match the server's item count.
            # Catches desyncs from savestates without requiring a level transition.
            # TODO use this as a way for the game itself to force a resync by setting it to 999 or something
            if int.from_bytes(sync_counter, "little") != len(ctx.items_received):
                needs_sync = True

            if self.death_link:
                await ctx.update_death_link(True)

            hp = int.from_bytes(body_hp, "little", signed=True)
            level_unchanged = self.prev_level_value == level_data
            in_gameplay = level_unchanged and demo_screen != b'\x00' and results_screen == b'\x00'

            if self.pending_death_link:
                self.pending_death_link = False
                self.sending_death_link = True
                if in_gameplay:
                    await bizhawk.write(ctx.bizhawk_ctx, [(HP_ADDR, [0, 0], "Combined WRAM")])

            if "DeathLink" in ctx.tags and ctx.last_death_link + 1 < time.time():
                if in_gameplay and hp <= 0 and not self.sending_death_link:
                    await self.send_deathlink(ctx)
                elif hp > 0:
                    self.sending_death_link = False

            # ---- results screen and goal ---------------------------------------------
            if results_screen == b'\x00':
                self.in_results_screen = False

            # TODO Have the goal condition be send via the game code too
            if results_screen != b'\x00' and not self.in_results_screen:
                # Completion condition. Runs If the level that was finished was the last level
                # Logic for Default game goal
                if self.goal_type == 0:
                    if level_data == b'\x10' and self.collected_disks >= self.required_disks and not ctx.finished_game:
                        await ctx.send_msgs([{
                            "cmd": "Say", "text": f"Final stage cleared! You had {self.collected_disks} Disks, which was {self.collected_disks - self.required_disks} more disks than needed!"
                            }])
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                        ctx.finished_game = True
                    elif level_data == b'\x10' and self.collected_disks < self.required_disks and not self.player_warned and not ctx.finished_game:
                        await ctx.send_msgs([
                            {"cmd": "Say", "text": f"Final stage cleared! You still need {self.required_disks - self.collected_disks} more disks."},
                            {"cmd": "Say", "text": "Load a previous save and collect more disks."},
                            {"cmd": "Say", "text": "Do NOT save over your file after the credits!"}
                        ])
                        self.player_warned = True
                # Logic for Vanilla
                elif self.goal_type == 1:
                    if level_data == b'\x10' and ctx.finished_game == False:
                        await ctx.send_msgs([{
                            "cmd": "Say", "text": "Final Stage Cleared! Game completed!"
                            }])
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                        ctx.finished_game = True

                self.in_results_screen = True

            # Additional check to see if the player collected enough disks AFTER beating final stage. Only used in default game goal
            if self.player_warned == True and self.collected_disks >= self.required_disks and ctx.finished_game == False:
                await ctx.send_msgs([{
                    "cmd": "Say", "text": f"{self.required_disks} Disks collected! Game completed!"
                }])
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True

            # ---- eReader and disk tracking -------------------------------------------
            # TODO These are still applied by the client rather than by ApGrantItem.
            for i in range(self.received_index, len(ctx.items_received)):
                needs_sync = True
                item = ctx.items_received[i]

                # Disk items
                if 1 <= item.item <= 180:
                    self.collected_disks += 1

                # If the Disk is also an eReader bitflag item
                if item.item >= 111 and item.item <= 140:
                    if item.item not in BIT_FLAGS:
                        continue
                    word_index, bit = BIT_FLAGS[item.item]

                    byte_index = word_index * 2
                    mask = 1 << (bit - 1)

                    if bit <= 8:
                        self.eReader_bitflag_inventory[byte_index]     |= mask
                    else:
                        self.eReader_bitflag_inventory[byte_index + 1] |= (mask >> 8)

                # If the disk is also is an eReader byte map item
                if item.item in BYTE_MAP:
                    addr, value = BYTE_MAP[item.item]
                    self.eReader_byte_map_inventory[addr - EREADER_BYTE_MAP_ADDR] = value



            self.received_index = len(ctx.items_received)

            # ---- sync ----------------------------------------------------------------
            if needs_sync:
                await self.sync_game_state(ctx)
                await bizhawk.write(ctx.bizhawk_ctx, [
                    (SYNC_COUNTER_ADDR, list(len(ctx.items_received).to_bytes(2, "little")), "Combined WRAM"),
                ])
            self.prev_level_value = level_data

        except bizhawk.RequestFailedError:
            pass

    async def get_items(self, ctx) -> bytearray:
        """Updates items collected by Zero based on ctx.checked_locations. Used in case of player using savestates.
        Only lower nibble (found state) is updated. Upper nibble (opened state) is untouched."""

        inventory = bytearray((await bizhawk.read(
                        ctx.bizhawk_ctx,
                        [(CHECKED_LOCS_INV_ADDR, 45, "Combined WRAM")]
                    ))[0])

        for location_id in ctx.checked_locations:
            if location_id in {10, 16, 17}:
                continue

            if 1 <= location_id <= 180:
                item_index = location_id - 1
                byte_index = item_index // 4
                bit_position = item_index % 4

                # Only set the lower nibble bit (bit positions 0–3)
                inventory[byte_index] |= (1 << bit_position)

        return inventory

    async def sync_game_state(self, ctx) -> None:
        """Syncronizes the player's collected items and inventory in order to prevent desyncs when using savestates.

        Done whenever the player collects or receives an item, or transitions between stages."""


        items_inventory = await self.get_items(ctx)

        await bizhawk.write(ctx.bizhawk_ctx, [
            (CHECKED_LOCS_INV_ADDR, list(items_inventory),                 "Combined WRAM"),  # Checked locations inventory
            (EREADER_BITFLAGS_ADDR, list(self.eReader_bitflag_inventory),  "Combined WRAM"),  # eReader bitflags
            (EREADER_BYTE_MAP_ADDR, self.eReader_byte_map_inventory,       "Combined WRAM"),  # eReader byte map
        ])

    async def push_items(self, ctx: "BizHawkClientContext",
                         inbox_write: int, inbox_read: int, items_applied: int) -> None:
        """Hand received items to the game through the itemInbox field."""
        slot_count = self.ap.count("itemInbox")
        wrap_mask = slot_count - 1
        # One slot is always left empty, otherwise a full ring would look identical to an empty one.
        max_items_waiting = slot_count - 1

        # itemsApplied going backwards means the game rewound for any reason. So resend from the start.
        if items_applied < self.items_applied_seen:
            logger.info("MMZero3: game restarted (applied %d -> %d); resending items.",
                        self.items_applied_seen, items_applied)
            self.items_pushed = 0
            self.ap_options_pushed = False
        self.items_applied_seen = items_applied

        # Starting weapons go first
        every_code = self.starting_weapon_codes + [int(item.item) for item in ctx.items_received]
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
