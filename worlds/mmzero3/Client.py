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

class ApBlock:
    """Addresses of gAp's fields, read from ap_symbols.json"""

    def __init__(self, doc: dict):
        state = doc["ap_state"]
        self.ready_value: int = doc["ready"]  # what gAp.ready reads once the game is up
        self.version: int = doc["version"]
        self.base: int = state["address"] - EWRAM_BASE
        self._fields: dict = state["fields"]

    def addr(self, field: str) -> int:
        return self.base + self._fields[field]["offset"]

    def count(self, field: str) -> int:
        return self._fields[field]["count"]

    def elem_size(self, field: str) -> int:
        return self._fields[field]["size"]

    def span(self, field: str) -> int:
        return self.elem_size(field) * self.count(field)


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

# Item / location tracking
ELF_FLAG_ADDR           = 0x3733C
ITEM_NOTIFY_ADDR        = 0x371E5

# Inventories
CHECKED_LOCS_INV_ADDR   = 0x371B8
EREADER_BITFLAGS_ADDR   = 0x02438
EREADER_BYTE_MAP_ADDR   = 0x02474
EX_SKILLS_ADDR          = 0x38068
BODY_INV_ADDR           = 0x3806C
FOOT_INV_ADDR           = 0x3806D
SAVE_BODY_INV_ADDR      = 0x37318
SAVE_FOOT_INV_ADDR      = 0x37319
HP_ADDR                 = 0x38044  
CRYSTAL_QUEUE_ADDR      = 0x2F5DC

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
        self.ap_drop_warned = False
        self.items_pushed = 0          # how much of items_received is in the game's RAM
        self.items_applied_seen = 0    # last gAp.itemsApplied; a drop means a reset

        # Options (overwritten from slot data)
        self.options_set = False
        self.required_disks = 80
        self.goal_type = 0  # 0 is for default (kill boss with enough disks), 1 is vanilla (just kill the boss)
        self.easy_ex_skill = 0
        self.randomize_weapons = 0

        # DeathLink
        self.death_link = False
        self.pending_death_link = False
        self.sending_death_link = True

        # Item tracking
        self.received_index = 0
        self.collected_disks = 0
        self.pending_crystals = 0

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

    async def sync_ap_mailbox(self, ctx: "BizHawkClientContext") -> None:
        """ removes checked locations, push received items.

        Game -> client, the game calls ApSendLocation() at the sites that already know a check happened 
        locQueue has the same IDs as the item/location IDs.

        Client -> game, uses push_items().
        """
        if self.ap is None or self.ap_disabled:
            return

        # Wait until connected
        if ctx.slot is None or not ctx.server_locations:
            return

        # One batch for both directions: the handshake, the location queue's indices, and the item queue's.
        (ready_b, version_b, write_b, read_b, dropped_b,
         inbox_write_b, inbox_read_b, applied_b) = await bizhawk.read(ctx.bizhawk_ctx, [
            (self.ap.addr("ready"),        4, "Combined WRAM"),
            (self.ap.addr("version"),      2, "Combined WRAM"),
            (self.ap.addr("locWrite"),     1, "Combined WRAM"),
            (self.ap.addr("locRead"),      1, "Combined WRAM"),
            (self.ap.addr("locDropped"),   1, "Combined WRAM"),
            (self.ap.addr("inboxWrite"),   1, "Combined WRAM"),
            (self.ap.addr("inboxRead"),    1, "Combined WRAM"),
            (self.ap.addr("itemsApplied"), 2, "Combined WRAM"),
        ])

        # ApInit runs on the first Process_Game. So it could still be booting.
        if int.from_bytes(ready_b, "little") != self.ap.ready_value:
            return

        version = int.from_bytes(version_b, "little")
        if version != self.ap.version:
            self.ap_disabled = True
            message = (f"ROM/client version mismatch: the ROM is AP interface version {version}, "
                       f"this apworld is version {self.ap.version}. Please Generate a new game/ROM!.")
            logger.error("MMZero3: %s", message)
            await ctx.send_msgs([{"cmd": "Say", "text": f"[MMZ3] {message}"}])
            return

        if not self.ap_handshake_logged:
            logger.info("MMZero3: gAp mailbox live at 0x%06X, AP interface version %d.",
                        self.ap.base + EWRAM_BASE, version)
            self.ap_handshake_logged = True

        # Non-zero means ApSendLocation found the queue full and threw a check away --
        # the client stalled for 63 checks. Should never happen; say so if it does.
        dropped = dropped_b[0]
        if dropped and not self.ap_drop_warned:
            self.ap_drop_warned = True
            logger.error("MMZero3: the ROM dropped %d location(s) -- gAp.locQueue "
                         "overflowed while the client was not draining it.", dropped)
            await ctx.send_msgs([{"cmd": "Say", "text":
                                  f"[MMZ3] warning: {dropped} location(s) were lost to a full "
                                  f"queue. Use !senditem if something is missing."}])

        await self.push_items(ctx, inbox_write_b[0], inbox_read_b[0],
                              int.from_bytes(applied_b, "little"))

        write, read = write_b[0], read_b[0]
        if write == read:
            return

        queue = (await bizhawk.read(
            ctx.bizhawk_ctx,
            [(self.ap.addr("locQueue"), self.ap.span("locQueue"), "Combined WRAM")]))[0]

        mask = self.ap.count("locQueue") - 1
        width = self.ap.elem_size("locQueue")

        location_ids: List[int] = []
        index = read
        while index != write:
            offset = index * width
            location_ids.append(int.from_bytes(queue[offset:offset + width], "little"))
            index = (index + 1) & mask

        known = [loc for loc in location_ids if loc in ctx.server_locations]
        unknown = sorted({loc for loc in location_ids if loc not in ctx.server_locations})
        if unknown:
            # The ROM reported a location this slot doesn't have.
            logger.warning("MMZero3: ROM reported unknown location id(s) %s; ignoring.", unknown)

        if known:
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": known}])
            logger.debug("MMZero3: drained %d location(s) from gAp: %s", len(known), known)

        await bizhawk.write(ctx.bizhawk_ctx,
                            [(self.ap.addr("locRead"), [write], "Combined WRAM")])

    async def push_items(self, ctx: "BizHawkClientContext",
                         inbox_write: int, inbox_read: int, items_applied: int) -> None:
        """Hand received items to the game through gAp.itemInbox.

        The game grants them itself through ROM edits.
        """
        capacity = self.ap.count("itemInbox")
        mask = capacity - 1
        width = self.ap.elem_size("itemInbox")

        # itemsApplied going backwards means ApInit ran again from a a reset, or a savestate. Resend everything.
        if items_applied < self.items_applied_seen:
            logger.info("MMZero3: game restarted (applied %d -> %d); resending items.",
                        self.items_applied_seen, items_applied)
            self.items_pushed = 0
        self.items_applied_seen = items_applied

        # Starting weapons go first so a fresh save has something equipped, or else it would just be the Buster
        all_codes = self.starting_weapon_codes + [int(item.item) for item in ctx.items_received]
        pending = all_codes[self.items_pushed:]
        if not pending:
            return

        in_flight = (inbox_write - inbox_read) & mask
        free = mask - in_flight
        if free <= 0:
            # The game is not draining due to being in a menu, a cutscene, a transition.
            return

        batch = []
        cursor = inbox_write
        count = min(free, len(pending))
        for code in pending[:count]:
            batch.append((self.ap.addr("itemInbox") + cursor * width,
                          list(code.to_bytes(width, "little")),
                          "Combined WRAM"))
            cursor = (cursor + 1) & mask

        batch.append((self.ap.addr("inboxWrite"), [cursor], "Combined WRAM"))
        await bizhawk.write(ctx.bizhawk_ctx, batch)

        self.items_pushed += count
        logger.debug("MMZero3: pushed %d item(s) to the game; %d still pending.",
                     count, len(pending) - count)

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:
            await self.sync_ap_mailbox(ctx)

            # Set the options
            if ctx.slot_data and not self.options_set:
                self.required_disks = ctx.slot_data.get("required_secret_disks", 80)
                self.goal_type = ctx.slot_data.get("goal", 0)
                self.easy_ex_skill = ctx.slot_data.get("easy_ex_skill", 0)
                self.randomize_weapons = ctx.slot_data.get("randomize_weapons", 0)
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

            # Read game state
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
                #print("item count has been changed!")
                #print(f"sync_counter: {(int.from_bytes(sync_counter, byteorder='little'))}")
                needs_sync = True

            if self.death_link:
                await ctx.update_death_link(True)

            hp = int.from_bytes(body_hp, "little", signed=True)
            settled = self.prev_level_value == level_data
            in_gameplay = settled and demo_screen != b'\x00' and results_screen == b'\x00'

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





            if results_screen == b'\x00':
                self.in_results_screen = False

            # Check if the player has completed a level
            # TODO: This method of checking is prone to breaking using savestates
            if results_screen != b'\x00' and not self.in_results_screen:
                level_id = int.from_bytes(level_data, byteorder='little')
                location_id = LEVEL_TO_LOCATION.get(level_id)

                if location_id:

                    # Send completion item
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": [location_id]
                    }])

                    if LOCATION_TO_CHIP.get(location_id):
                        # Send necessary chip
                        await ctx.send_msgs([{
                            "cmd": "LocationChecks",
                            "locations": [LOCATION_TO_CHIP.get(location_id)]
                        }])

                    if await self.should_reward_exskill(ctx) or self.easy_ex_skill == 1:
                        await ctx.send_msgs([{
                            "cmd": "LocationChecks",
                            "locations": [LOCATION_TO_EXSKILL.get(location_id)]
                        }])

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

            # Receive an item from AP
            for i in range(self.received_index, len(ctx.items_received)):
                needs_sync = True
                item = ctx.items_received[i]

                # Disk items
                if 1 <= item.item <= 180:
                    self.collected_disks += 1

                    # Send notification to player
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [(ITEM_NOTIFY_ADDR, [item.item], "Combined WRAM")]
                    )

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

                if item.item in CRYSTAL_ITEM_VALUES:
                    self.pending_crystals += CRYSTAL_ITEM_VALUES[item.item]


            self.received_index = len(ctx.items_received)

            if self.pending_crystals and in_gameplay:
                queue = int.from_bytes(
                    (await bizhawk.read(ctx.bizhawk_ctx, [(CRYSTAL_QUEUE_ADDR, 4, "Combined WRAM")]))[0],
                    "little",
                )
                queue = min(queue + self.pending_crystals, 9999)
                await bizhawk.write(ctx.bizhawk_ctx, [
                    (CRYSTAL_QUEUE_ADDR, list(queue.to_bytes(4, "little")), "Combined WRAM"),
                ])
                self.pending_crystals = 0

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

    async def should_reward_exskill(self, ctx) -> bool:
        """Determine if an EX Skill should be rewarded after a level."""

        level_rank, elf_flag = await bizhawk.read(
            ctx.bizhawk_ctx,
            [
                (RESULTS_SCREEN_ADDR, 1, "Combined WRAM"),
                (ELF_FLAG_ADDR,       1, "Combined WRAM"),
            ]
        )
        if level_rank[0] > 85:
            return True

        # If the player has used a rank increasing cyber elf
        if elf_flag[0] == 0x01:
            await bizhawk.write(
                ctx.bizhawk_ctx,
                [(ELF_FLAG_ADDR, [0], "Combined WRAM")]
            )
            return True

        return False

    async def sync_game_state(self, ctx) -> None:
        """Syncronizes the player's collected items and inventory in order to prevent desyncs when using savestates.

        Done whenever the player collects or receives an item, or transitions between stages."""

        # Read RAM for inventories the game also writes to, plus subtanks
        (
            foot_ram,
            body_ram,
            save_body_ram,
            save_foot_ram,
        ) = await bizhawk.read(ctx.bizhawk_ctx, [
            (FOOT_INV_ADDR,       1, "Combined WRAM"),  # Live foot chips (disk-based chips written by game)
            (BODY_INV_ADDR,       1, "Combined WRAM"),  # Live body chips (game writes on equip/load)
            (SAVE_BODY_INV_ADDR,  1, "Combined WRAM"),  # Save-copy body chips
            (SAVE_FOOT_INV_ADDR,  1, "Combined WRAM"),  # Save-copy foot chips
        ])

        # Recompute AP contributions from all received items
        # bit 0 is always on by default
        foot_ap    = 0x01
        body_ap    = 0x01
        ex_skill_ap = bytearray(2)

        received_item_ids = set()
        for item in ctx.items_received:
            item_id = item.item
            received_item_ids.add(item_id)
            if item_id in FOOT_CHIP_MAP:
                foot_ap |= FOOT_CHIP_MAP[item_id][1]
            if item_id in BODY_CHIP_MAP:
                body_ap |= BODY_CHIP_MAP[item_id][1]
            if item_id in EX_SKILL_MAP:
                byte_index, mask = EX_SKILL_MAP[item_id]
                ex_skill_ap[byte_index] |= mask

        # Merged: RAM preserves game written state and ensures AP items are always present.
        foot_merged    = bytearray([foot_ram[0] | foot_ap])
        body_merged    = bytearray([body_ram[0] | body_ap])

        # Mirror the chips into the save copy (gGameState.save.status) as well.
        save_body_merged = bytearray([save_body_ram[0] | body_ap])
        save_foot_merged = bytearray([save_foot_ram[0] | foot_ap])

        items_inventory = await self.get_items(ctx)

        await bizhawk.write(ctx.bizhawk_ctx, [
            (CHECKED_LOCS_INV_ADDR, list(items_inventory),                 "Combined WRAM"),  # Checked locations inventory
            (EREADER_BITFLAGS_ADDR, list(self.eReader_bitflag_inventory),  "Combined WRAM"),  # eReader bitflags
            (EREADER_BYTE_MAP_ADDR, self.eReader_byte_map_inventory,       "Combined WRAM"),  # eReader byte map
            (EX_SKILLS_ADDR,        ex_skill_ap,                           "Combined WRAM"),  # EX Skills
            (BODY_INV_ADDR,         body_merged,                           "Combined WRAM"),  # Body chips (live entity)
            (FOOT_INV_ADDR,         foot_merged,                           "Combined WRAM"),  # Foot chips (live entity)
            (SAVE_BODY_INV_ADDR,    save_body_merged,                      "Combined WRAM"),  # Body chips (save copy)
            (SAVE_FOOT_INV_ADDR,    save_foot_merged,                      "Combined WRAM"),  # Foot chips (save copy)
        ])

