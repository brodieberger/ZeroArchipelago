from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from . import MMZero3World

class MMZero3Item(Item):
    game: str = "Mega Man Zero 3"

class MMZero3ItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler
    can_create: Callable[["MMZero3World"], bool] = lambda world: True

item_data_table: Dict[str, MMZero3ItemData] = {
    "Z Saber": MMZero3ItemData(
        code=69696969,
        type=ItemClassification.progression,
    ),
    "Cyber Elf 1": MMZero3ItemData(
        code=69696968,
        type=ItemClassification.progression,
    ),
    "Cyber Elf 2": MMZero3ItemData(
        code=69696967,
        type=ItemClassification.progression,
    ),
    "Cyber Elf 3": MMZero3ItemData(
        code=69696966,
        type=ItemClassification.progression,
    ),
    "Cyber Elf 4": MMZero3ItemData(
        code=69696965,
        type=ItemClassification.progression,
    ),
    "Victory": MMZero3ItemData(
        code=69696964,
        type=ItemClassification.progression,
    ),
    "100 Energy Crystals": MMZero3ItemData(
        code=69696963,
        can_create=lambda world: False  # Only created from `get_filler_item_name`.
    ),
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
