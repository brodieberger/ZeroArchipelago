from typing import List, Dict, Any

from BaseClasses import Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Items import MMZero3Item, item_data_table, item_table
from .Locations import MMZero3Location, location_data_table, location_table, locked_locations
from .Options import MMZero3Options
from .Regions import region_data_table
#from .Rules import get_button_rule


class MMZero3WebWorld(WebWorld):
    theme = "ice"
    bug_report_page = "https://github.com/brodieberger/ZeroArchipelago/"


class MMZero3World(World):
    """
    Play as Zero, kill the robots and save the day
    """

    game = "Mega Man Zero 3"

    item_name_to_id = item_table
    location_name_to_id = location_table

    web = MMZero3WebWorld()
    options_dataclass = MMZero3Options
    options: MMZero3Options
    #settings: typing.ClassVar[MMZero3Settings]
    #required_client_version = (0, 5, 0)

    def create_item(self, name: str) -> MMZero3Item:
        return MMZero3Item(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        item_pool: List[MMZero3Item] = []
        # Exclude locked items from the item pool
        locked_item_names = {data.locked_item for data in locked_locations.values() if data.locked_item}
        for name, item in item_data_table.items():
            if item.code and item.can_create(self) and name not in locked_item_names:
                item_pool.append(self.create_item(name))

        self.multiworld.itempool += item_pool

    def create_regions(self) -> None:
        # Create regions.
        for region_name in region_data_table.keys():
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Create locations.
        for region_name, region_data in region_data_table.items():
            region = self.get_region(region_name)
            region.add_locations({
                location_name: location_data.address for location_name, location_data in location_data_table.items()
                if location_data.region == region_name and location_data.can_create(self)
            }, MMZero3Location)
            region.add_exits(region_data_table[region_name].connecting_regions)

        # Place locked locations.
        for location_name, location_data in locked_locations.items():
            # Ignore locations we never created.
            if not location_data.can_create(self):
                continue

            locked_item = self.create_item(location_data_table[location_name].locked_item)
            self.get_location(location_name).place_locked_item(locked_item)

    def get_filler_item_name(self) -> str:
        return "100 Energy Crystals"
    
    def set_rules(self) -> None:
        # Cyber Elves require access to Level 1
        for elf in ["Cyber Elf 1", "Cyber Elf 2", "Cyber Elf 3", "Cyber Elf 4"]:
            self.multiworld.get_location(elf, self.player).access_rule = \
                lambda state, player=self.player: state.can_reach("Level 1", "Region", player)

        # Kill Omega requires access to Boss Stage
        self.multiworld.get_location("Kill Omega", self.player).access_rule = \
            lambda state, player=self.player: state.can_reach("Boss Stage", "Region", player)

        # Completion condition
        self.multiworld.completion_condition[self.player] = \
            lambda state: state.has("Victory", self.player)