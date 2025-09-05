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


# Stage names as they appear in game order
stage_names = [
    "Derelict Spacecraft", "Aegis Volcano Base", "Oceanic Highway Ruins",
    "Weapons Repair Factory", "Old Residential", "Missile Factory",
    "Twilight Desert", "Forest of Anatre", "Frontline Ice Base",
    "Area X-2", "Energy Facility", "Snowy Plains",
    "Sunken Library", "Giant Elevator", "Sub Arcadia"
]

# Exclude these items. They are all of the files that can be found in the Hub area
# These are excluded to due issues with the memory manipulation I am using, hopefully only a temp fix.
exclude = [23, 44, 58, 92, 99, 106, 107, 116, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176]
item_data_table: Dict[str, MMZero3ItemData] = {
    "Z Saber": MMZero3ItemData(code=999,type=ItemClassification.progression),
    "Secret Disk 001: Auto-Charge Head Chip": MMZero3ItemData(code=1, type=ItemClassification.useful),
    "Secret Disk 002: Auto-Recover Head Chip": MMZero3ItemData(code=2, type=ItemClassification.useful),
    "Secret Disk 003: Quick-Charge Head Chip": MMZero3ItemData(code=3, type=ItemClassification.useful),
    "Secret Disk 004: Frog Foot Chip": MMZero3ItemData(code=4, type=ItemClassification.useful),
    "Secret Disk 005: Splash Jump Foot Chip": MMZero3ItemData(code=5, type=ItemClassification.progression),
    "Secret Disk 006: Ultima Foot Chip": MMZero3ItemData(code=6, type=ItemClassification.progression),
    "Secret Disk 007: File A": MMZero3ItemData(code=7, type=ItemClassification.filler),
    "Secret Disk 008: File B": MMZero3ItemData(code=8, type=ItemClassification.filler),
    "Secret Disk 009: File C": MMZero3ItemData(code=9, type=ItemClassification.filler),
    "Secret Disk 010: File D": MMZero3ItemData(code=10, type=ItemClassification.filler),
    "Secret Disk 011: File E": MMZero3ItemData(code=11, type=ItemClassification.filler),
    "Secret Disk 012: File F": MMZero3ItemData(code=12, type=ItemClassification.filler),
    "Secret Disk 013: File G": MMZero3ItemData(code=13, type=ItemClassification.filler),
    "Secret Disk 014: File H": MMZero3ItemData(code=14, type=ItemClassification.filler),
    "Secret Disk 015: File I": MMZero3ItemData(code=15, type=ItemClassification.filler),
    "Secret Disk 016: File J": MMZero3ItemData(code=16, type=ItemClassification.filler),
    "Secret Disk 017: File K": MMZero3ItemData(code=17, type=ItemClassification.filler),
    "Secret Disk 018: File L": MMZero3ItemData(code=18, type=ItemClassification.filler),
    "Secret Disk 019: File M": MMZero3ItemData(code=19, type=ItemClassification.filler),
    "Secret Disk 020: File N": MMZero3ItemData(code=20, type=ItemClassification.filler),
    "Secret Disk 021: Martina (Double Health)": MMZero3ItemData(code=21, type=ItemClassification.useful),
    "Secret Disk 022: Milvy (+4 Max Health)": MMZero3ItemData(code=22, type=ItemClassification.useful),
    "Secret Disk 024: Sylphy (+4 Max Health)": MMZero3ItemData(code=24, type=ItemClassification.useful),
    "Secret Disk 025: Rilphy (+4 Max Health)": MMZero3ItemData(code=25, type=ItemClassification.useful),
    "Secret Disk 026: Artan (Sub Tank)": MMZero3ItemData(code=26, type=ItemClassification.useful),
    "Secret Disk 027: Zictan (Sub Tank)": MMZero3ItemData(code=27, type=ItemClassification.useful),
    "Secret Disk 028: Mott (Extra Lives)": MMZero3ItemData(code=28, type=ItemClassification.filler),
    "Secret Disk 029: Dott (Extra Lives)": MMZero3ItemData(code=29, type=ItemClassification.filler),
    "Secret Disk 030: Curiph (Small Heal)": MMZero3ItemData(code=30, type=ItemClassification.filler),
    "Secret Disk 031: Luriph (Small Heal)": MMZero3ItemData(code=31, type=ItemClassification.filler),
    "Secret Disk 032: Suriph (Small Heal)": MMZero3ItemData(code=32, type=ItemClassification.filler),
    "Secret Disk 033: Tiriph (Small Heal)": MMZero3ItemData(code=33, type=ItemClassification.filler),
    "Secret Disk 034: Yuriph (Small Heal)": MMZero3ItemData(code=34, type=ItemClassification.filler),
    "Secret Disk 035: Beriph (Small Heal)": MMZero3ItemData(code=35, type=ItemClassification.filler),
    "Secret Disk 036: Wiliph (Small Heal)": MMZero3ItemData(code=36, type=ItemClassification.filler),
    "Secret Disk 037: Cyliph (Small Heal)": MMZero3ItemData(code=37, type=ItemClassification.filler),
    "Secret Disk 038: Snoq (Large Heal)": MMZero3ItemData(code=38, type=ItemClassification.filler),
    "Secret Disk 039: Mathiq (Large Heal)": MMZero3ItemData(code=39, type=ItemClassification.filler),
    "Secret Disk 040: Mylaq (Large Heal)": MMZero3ItemData(code=40, type=ItemClassification.filler),
    "Secret Disk 041: Ajiq (Large Heal)": MMZero3ItemData(code=41, type=ItemClassification.filler),
    "Secret Disk 042: Dobuq (Large Heal)": MMZero3ItemData(code=42, type=ItemClassification.filler),
    "Secret Disk 043: Mulaq (Large Heal)": MMZero3ItemData(code=43, type=ItemClassification.filler),
    "Secret Disk 045: Miulla (Bullets to Health)": MMZero3ItemData(code=45, type=ItemClassification.useful),
    "Secret Disk 046: Cloppe (Drops Health)": MMZero3ItemData(code=46, type=ItemClassification.useful),
    "Secret Disk 047: Sloppe (Drops Health)": MMZero3ItemData(code=47, type=ItemClassification.useful),
    "Secret Disk 048: Putite (Non-Lethal Spikes)": MMZero3ItemData(code=48, type=ItemClassification.useful),
    "Secret Disk 049: Balette (Run Faster)": MMZero3ItemData(code=49, type=ItemClassification.useful),
    "Secret Disk 050: Maya (Faster Ladders)": MMZero3ItemData(code=50, type=ItemClassification.useful),
    "Secret Disk 051: Kwappa (Slower Sliding)": MMZero3ItemData(code=51, type=ItemClassification.useful),
    "Secret Disk 052: Gambul (No Recoil)": MMZero3ItemData(code=52, type=ItemClassification.useful),
    "Secret Disk 053: Biraid (Pit Recovery)": MMZero3ItemData(code=53, type=ItemClassification.useful),
    "Secret Disk 054: Birleaf (Pit Recovery)": MMZero3ItemData(code=54, type=ItemClassification.useful),
    "Secret Disk 055: Pitaph (Slows Enemies)": MMZero3ItemData(code=55, type=ItemClassification.useful),
    "Secret Disk 056: Pitapuh (Slows Enemies)": MMZero3ItemData(code=56, type=ItemClassification.useful),
    "Secret Disk 057: Beetack (Direct Bullets)": MMZero3ItemData(code=57, type=ItemClassification.useful),
    "Secret Disk 059: Archim (Arcing Bullets)": MMZero3ItemData(code=59, type=ItemClassification.useful),
    "Secret Disk 060: Archil (Arcing Bullets)": MMZero3ItemData(code=60, type=ItemClassification.useful),
    "Secret Disk 061: Byse (Double Drop Value)": MMZero3ItemData(code=61, type=ItemClassification.useful),
    "Secret Disk 062: Dylphina (Drop Rate Up)": MMZero3ItemData(code=62, type=ItemClassification.useful),
    "Secret Disk 063: Lizetus (Up Saber Combo)": MMZero3ItemData(code=63, type=ItemClassification.useful),
    "Secret Disk 064: Cottus (Down Saber Combo)": MMZero3ItemData(code=64, type=ItemClassification.useful),
    "Secret Disk 065: Shuthas (4 Buster Shots)": MMZero3ItemData(code=65, type=ItemClassification.useful),
    "Secret Disk 066: Malthas (Saber Spin)": MMZero3ItemData(code=66, type=ItemClassification.useful),
    "Secret Disk 067: Ilethas (Slash Bullets)": MMZero3ItemData(code=67, type=ItemClassification.useful),
    "Secret Disk 068: Enethas (EC from Block)": MMZero3ItemData(code=68, type=ItemClassification.useful),
    "Secret Disk 069: Busras (Buster +1)": MMZero3ItemData(code=69, type=ItemClassification.useful),
    "Secret Disk 070: Sabras (Saber +1)": MMZero3ItemData(code=70, type=ItemClassification.useful),
    "Secret Disk 071: Roderas (Recoil Rod +1)": MMZero3ItemData(code=71, type=ItemClassification.useful),
    "Secret Disk 072: Boomeras (Shield +1)": MMZero3ItemData(code=72, type=ItemClassification.useful),
    "Secret Disk 073: Clokkle (Faster Charge)": MMZero3ItemData(code=73, type=ItemClassification.useful),
    "Secret Disk 074: Metoras (Enemies to Mets)": MMZero3ItemData(code=74, type=ItemClassification.filler),
    "Secret Disk 075: Metorika (Enemies to Mets)": MMZero3ItemData(code=75, type=ItemClassification.filler),
    "Secret Disk 076: Metorph (Enemies to Mets)": MMZero3ItemData(code=76, type=ItemClassification.filler),
    "Secret Disk 077: Metella (Enemies to Mets)": MMZero3ItemData(code=77, type=ItemClassification.filler),
    "Secret Disk 078: Meterom (Enemies to Mets)": MMZero3ItemData(code=78, type=ItemClassification.filler),
    "Secret Disk 079: Kynite (Kill All Enemies)": MMZero3ItemData(code=79, type=ItemClassification.filler),
    "Secret Disk 080: Surnite (Kill All Enemies)": MMZero3ItemData(code=80, type=ItemClassification.filler),
    "Secret Disk 081: Tenite (Kill All Enemies)": MMZero3ItemData(code=81, type=ItemClassification.filler),
    "Secret Disk 082: Stopalla (Stun Enemies)": MMZero3ItemData(code=82, type=ItemClassification.filler),
    "Secret Disk 083: Stopina (Stun Enemies)": MMZero3ItemData(code=83, type=ItemClassification.filler),
    "Secret Disk 084: Stopule (Stun Enemies)": MMZero3ItemData(code=84, type=ItemClassification.filler),
    "Secret Disk 085: Stopeta (Stun Enemies)": MMZero3ItemData(code=85, type=ItemClassification.filler),
    "Secret Disk 086: Stoposa (Stun Enemies)": MMZero3ItemData(code=86, type=ItemClassification.filler),
    "Secret Disk 087: Hanmarga (Half Boss HP)": MMZero3ItemData(code=87, type=ItemClassification.useful),
    "Secret Disk 088: Hanmarji (Half Boss HP)": MMZero3ItemData(code=88, type=ItemClassification.useful),
    "Secret Disk 089: Hanmarbo (Half Boss HP)": MMZero3ItemData(code=89, type=ItemClassification.useful),
    "Secret Disk 090: Aina (Sets Rank to A)": MMZero3ItemData(code=90, type=ItemClassification.useful),
    "Secret Disk 091: Acooi (Sets Rank to A)": MMZero3ItemData(code=91, type=ItemClassification.useful),
    "Secret Disk 093: Anater (Sets Rank to A)": MMZero3ItemData(code=93, type=ItemClassification.useful),
    "Secret Disk 094: Awarne (Sets Rank to A)": MMZero3ItemData(code=94, type=ItemClassification.useful),
    "Secret Disk 095: 80 E-Crystals": MMZero3ItemData(code=95, type=ItemClassification.filler),
    "Secret Disk 096: 100 E-Crystals": MMZero3ItemData(code=96, type=ItemClassification.filler),
    "Secret Disk 097: 200 E-Crystals": MMZero3ItemData(code=97, type=ItemClassification.filler),
    "Secret Disk 098: 150 E-Crystals": MMZero3ItemData(code=98, type=ItemClassification.filler),
    "Secret Disk 100: 100 E-Crystals": MMZero3ItemData(code=100, type=ItemClassification.filler),
    "Secret Disk 101: 100 E-Crystals": MMZero3ItemData(code=101, type=ItemClassification.filler),
    "Secret Disk 102: 50 E-Crystals": MMZero3ItemData(code=102, type=ItemClassification.filler),
    "Secret Disk 103: 80 E-Crystals": MMZero3ItemData(code=103, type=ItemClassification.filler),
    "Secret Disk 104: 100 E-Crystals": MMZero3ItemData(code=104, type=ItemClassification.filler),
    "Secret Disk 105: 100 E-Crystals": MMZero3ItemData(code=105, type=ItemClassification.filler),
    "Secret Disk 108: 100 E-Crystals": MMZero3ItemData(code=108, type=ItemClassification.filler),
    "Secret Disk 109: 100 E-Crystals": MMZero3ItemData(code=109, type=ItemClassification.filler),
    "Secret Disk 110: 100 E-Crystals": MMZero3ItemData(code=110, type=ItemClassification.filler),
    # bitflags
    "Secret Disk 111: Potted Plants to Base": MMZero3ItemData(code=111, type=ItemClassification.filler),
    "Secret Disk 112: Change Nurse Elf Design": MMZero3ItemData(code=112, type=ItemClassification.filler),
    "Secret Disk 113: Reploid to Base Hall": MMZero3ItemData(code=113, type=ItemClassification.filler),
    "Secret Disk 114: Change Alouette Dress Design": MMZero3ItemData(code=114, type=ItemClassification.filler),

    "Secret Disk 115: Reploid to Room 02A": MMZero3ItemData(code=115, type=ItemClassification.filler),
    #Secret Disk 116 found in base, excluded
    "Secret Disk 117: Orange Cats to Base": MMZero3ItemData(code=117, type=ItemClassification.filler),
    "Secret Disk 118: Phantom Cyber Elf to Base Roof": MMZero3ItemData(code=118, type=ItemClassification.filler),
    "Secret Disk 119: Posters to Base": MMZero3ItemData(code=119, type=ItemClassification.filler),
    "Secret Disk 120: New Room Near Andrew": MMZero3ItemData(code=120, type=ItemClassification.filler),
    "Secret Disk 121: Reploid to Room 1F-A": MMZero3ItemData(code=121, type=ItemClassification.filler),
    
    "Secret Disk 122: Flowers to Base Roof": MMZero3ItemData(code=122, type=ItemClassification.filler),
    "Secret Disk 123: Change Animal Elf Design": MMZero3ItemData(code=123, type=ItemClassification.filler),
    "Secret Disk 124: Young Andrew": MMZero3ItemData(code=124, type=ItemClassification.filler),
    "Secret Disk 125: Seagulls to Base": MMZero3ItemData(code=125, type=ItemClassification.filler),
    "Secret Disk 126: Tabby Cats to Base": MMZero3ItemData(code=126, type=ItemClassification.filler),
    "Secret Disk 127: Grafitti to Base": MMZero3ItemData(code=127, type=ItemClassification.filler),
    "Secret Disk 128: Reploid to Room 02D": MMZero3ItemData(code=128, type=ItemClassification.filler),
    
    "Secret Disk 129: Right Tower Reploid Added Dialogue": MMZero3ItemData(code=129, type=ItemClassification.filler),
    "Secret Disk 130: Reploid to Room 02B": MMZero3ItemData(code=130, type=ItemClassification.filler),
    "Secret Disk 131: Reploid to Room 02C": MMZero3ItemData(code=131, type=ItemClassification.filler),
    "Secret Disk 132: Reploid to Floor 2": MMZero3ItemData(code=132, type=ItemClassification.filler),
    "Secret Disk 133: Elpizo Cyber Elf by Command Room": MMZero3ItemData(code=133, type=ItemClassification.filler),
    "Secret Disk 134: Left Tower Reploid Added Dialogue": MMZero3ItemData(code=134, type=ItemClassification.filler),
    
    "Secret Disk 135: Change Hacker Elf Design": MMZero3ItemData(code=135, type=ItemClassification.filler),
    "Secret Disk 136: Lilies to Base": MMZero3ItemData(code=136, type=ItemClassification.filler),
    "Secret Disk 137: Flying Fish to the Base Dock": MMZero3ItemData(code=137, type=ItemClassification.filler),
    "Secret Disk 138: Reploid to Room 03C": MMZero3ItemData(code=138, type=ItemClassification.filler),
    "Secret Disk 139: Reploid to Floor 3": MMZero3ItemData(code=139, type=ItemClassification.filler),
    "Secret Disk 140: Reploid to Room 03D": MMZero3ItemData(code=140, type=ItemClassification.filler),
    # non-bitflags
    "Secret Disk 141: Dialogue Window: Silver": MMZero3ItemData(code=141, type=ItemClassification.filler),
    "Secret Disk 142: Dialogue Window: Blue": MMZero3ItemData(code=142, type=ItemClassification.filler),
    "Secret Disk 143: Dialogue Window: Action": MMZero3ItemData(code=143, type=ItemClassification.filler),
    "Secret Disk 144: Dialogue Window: Mechanical": MMZero3ItemData(code=144, type=ItemClassification.filler),
    "Secret Disk 145: Dialogue Window: Rosebush": MMZero3ItemData(code=145, type=ItemClassification.filler),
    "Secret Disk 146: Dialogue Window: Command Line": MMZero3ItemData(code=146, type=ItemClassification.filler),
    "Secret Disk 147: Dialogue Window: Chains": MMZero3ItemData(code=147, type=ItemClassification.filler),
    "Secret Disk 148: Dialogue Window: Explosion ": MMZero3ItemData(code=148, type=ItemClassification.filler),
    "Secret Disk 149: Title Screen: Alt 1": MMZero3ItemData(code=149, type=ItemClassification.filler),
    "Secret Disk 150: Title Screen: Alt 2": MMZero3ItemData(code=150, type=ItemClassification.filler),
    "Secret Disk 151: Title Screen: Alt 3": MMZero3ItemData(code=151, type=ItemClassification.filler),
    "Secret Disk 152: Title Screen: Ciel": MMZero3ItemData(code=152, type=ItemClassification.filler),
    "Secret Disk 153: Elevator: Wood": MMZero3ItemData(code=153, type=ItemClassification.filler),
    "Secret Disk 154: Elevator: Capsule": MMZero3ItemData(code=154, type=ItemClassification.filler),
    "Secret Disk 155: Base Environment: Night": MMZero3ItemData(code=155, type=ItemClassification.filler),
    "Secret Disk 156: Base Environment: Snowy": MMZero3ItemData(code=156, type=ItemClassification.filler),
    "Secret Disk 157: Ciel Computer: New": MMZero3ItemData(code=157, type=ItemClassification.filler),
    "Secret Disk 158: Ciel Computer: Vending Machine": MMZero3ItemData(code=158, type=ItemClassification.filler),
    "Secret Disk 159: Ciel Computer: Monument": MMZero3ItemData(code=159, type=ItemClassification.filler),
    "Secret Disk 160: Ciel Computer: Supercomputer": MMZero3ItemData(code=160, type=ItemClassification.filler),
    "Secret Disk 161: Life Pickup: Blue Orbs": MMZero3ItemData(code=161, type=ItemClassification.filler),
    "Secret Disk 162: Life Pickup: Flashing Squares": MMZero3ItemData(code=162, type=ItemClassification.filler),
    "Secret Disk 163: E-Crystals: Orbs": MMZero3ItemData(code=163, type=ItemClassification.filler),
    "Secret Disk 164: E-Crystals: Green Crystals": MMZero3ItemData(code=164, type=ItemClassification.filler),
    "Secret Disk 177: Extra Life: Blue Z": MMZero3ItemData(code=177, type=ItemClassification.filler),
    "Secret Disk 178: Extra Life: Green Z": MMZero3ItemData(code=178, type=ItemClassification.filler),
    "Secret Disk 179: Buster Shot: Black Bullets": MMZero3ItemData(code=179, type=ItemClassification.filler),
    "Secret Disk 180: Buster Shot: Realistic Bullets": MMZero3ItemData(code=180, type=ItemClassification.filler),
    
    "Victory": MMZero3ItemData(code=300,type=ItemClassification.progression),
    **{
        f"{stage} Cleared": MMZero3ItemData(
            code=180 + idx + 1,
            type=ItemClassification.progression,
        )
        for idx, stage in enumerate(stage_names)
    },
    "100 Energy Crystals (Unimplemented)": MMZero3ItemData(
        code=301,
        can_create=lambda world: False  # Only created from `get_filler_item_name`.
    ),
}

item_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}
