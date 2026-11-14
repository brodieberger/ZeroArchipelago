# Fields to be read from gAp and gApSeedConfig.
# EWRAM address minus 0x02000000

# gAp.ready reads AP_READY once the game has booted, and gAp.version reads AP_VERSION.
AP_READY = 0x335A5041      # Spells out 'APZ3' in little endian
AP_VERSION = 26

# Constants from ap.h and constants/constants.h
AP_KILL_REQUESTED = 1
AP_TAKEN_BYTE = 8
AP_TAKEN_SUBTANK1 = 1
AP_TAKEN_SUBTANK2 = 2
AP_LOC_SUBTANK_1 = 221
AP_LOC_SUBTANK_2 = 222
AP_ITEM_DISK_FIRST = 1
AP_ITEM_DISK_LAST = 180
AP_DISK_BYTES = 45
AP_UNLOCK_BYTE = 12
AP_MAX_LOCATION_ID = 655
AP_SELECT_CYCLE_SUB_WEAPON = 0
AP_SELECT_CYCLE_MAIN_WEAPON = 1
AP_SELECT_CYCLE_HEAD_CHIP = 2
AP_SELECT_CYCLE_BODY_CHIP = 3
AP_SELECT_CYCLE_FOOT_CHIP = 4
AP_SELECT_USE_SUBTANK = 5
AP_ELVES_VANILLA = 0
AP_ELVES_NO_PENALTY = 1
AP_ELVES_AUTO = 2
AP_LOC_EXLIFE_FIRST = 231
AP_EXLIFE_COUNT = 10
AP_LOC_ITEMSANITY_FIRST = 301
AP_ITEMSANITY_COUNT = 82
AP_LOC_IMPORT_FIRST = 400
AP_IMPORT_ELF_COUNT = 28
AP_ITEM_IMPORT_ACCESS_FIRST = 320
AP_IMPORT_COUNT = 14
AP_SHOP_LOCATION_FIRST = 253
AP_SHOP_TEXT_COLS = 12
AP_SHOP_NAME_LINES = 3
AP_SHOP_PLAYER_LINES = 2
AP_SHOP_TEXT_END = 255
AP_SHOP_KIND_PLAIN = 0
AP_SHOP_KIND_PROGRESSION = 1
AP_SHOP_KIND_TRAP = 2
AP_SHOP_OWN_WORLD = 4
AP_SHOP_SLOTS_MAX = 48
AP_ITEM_STORY_MID = 229
AP_ITEM_STORY_LATE = 230
AP_ITEM_WEAPON_LEVEL_FIRST = 400
AP_ITEM_CODES_PER_WEAPON = 8
RANK_F = 0
RANK_E = 1
RANK_D = 2
RANK_C = 3
RANK_B = 4
RANK_A = 5
RANK_S = 6
AP_FINAL_RANK_NONE = 255

# gAp
GAP = 0x0003EE80
READY = 0x0003EE80
VERSION = 0x0003EE84
ITEM_INBOX = 0x0003EE86
ITEM_INBOX_COUNT = 16
ITEM_INBOX_ELEMENT_SIZE = 2
ITEMS_APPLIED = 0x0003EEA6
INBOX_WRITE_INDEX = 0x0003EEA8
INBOX_READ_INDEX = 0x0003EEA9
CHECKED_LOCATIONS = 0x0003EEAA
CHECKED_LOCATIONS_COUNT = 82
SERVER_CHECKED = 0x0003EEFC
SERVER_CHECKED_COUNT = 82
RANK_ELF_USED = 0x0003EF4E
DISKS_OWNED = 0x0003EF50
DEATH_COUNT = 0x0003EF52
KILL_REQUEST = 0x0003EF54
CAN_ACCEPT_ITEMS = 0x0003EF55
SHOP_SEEN = 0x0003EF56
SHOP_SEEN_COUNT = 6

# gStageRun.id: Current stage
STAGE_ID = 0x000301A0

# gSpawnManager.area: Individual area of the stage
STAGE_AREA = 0x000300E1

# gApShopPrices
SHOP_PRICES_ROM_OFFSET = 0x00102AE0
SHOP_PRICES_COUNT = 48
SHOP_PRICES_ELEMENT_SIZE = 2

# gApShopItems
SHOP_ITEMS_ROM_OFFSET = 0x00102B40
SHOP_ITEMS_COUNT = 48
SHOP_ITEMS_SIZE = 68

# The game's text encoding, for names the shop prints
CHARMAP = {
    ' ': 0x00,
    '!': 0xCA,
    '"': 0xE9,
    '#': 0xCC,
    '$': 0xFF,
    '%': 0xCE,
    '&': 0xCF,
    "'": 0xD0,
    '(': 0xD1,
    ')': 0xD2,
    '*': 0xD3,
    '+': 0xD4,
    ',': 0xE8,
    '-': 0xD6,
    '.': 0xE5,
    '/': 0xD8,
    '0': 0x01,
    '1': 0x02,
    '2': 0x03,
    '3': 0x04,
    '4': 0x05,
    '5': 0x06,
    '6': 0x07,
    '7': 0x08,
    '8': 0x09,
    '9': 0x0A,
    ':': 0xD9,
    '=': 0xDB,
    '?': 0xDD,
    'A': 0x0B,
    'B': 0x0C,
    'C': 0x0D,
    'D': 0x0E,
    'E': 0x0F,
    'F': 0x10,
    'G': 0x11,
    'H': 0x12,
    'I': 0x13,
    'J': 0x14,
    'K': 0x15,
    'L': 0x16,
    'M': 0x17,
    'N': 0x18,
    'O': 0x19,
    'P': 0x1A,
    'Q': 0x1B,
    'R': 0x1C,
    'S': 0x1D,
    'T': 0x1E,
    'U': 0x1F,
    'V': 0x20,
    'W': 0x21,
    'X': 0x22,
    'Y': 0x23,
    'Z': 0x24,
    '[': 0xDE,
    ']': 0xDF,
    '_': 0xE0,
    'a': 0x25,
    'b': 0x26,
    'c': 0x27,
    'd': 0x28,
    'e': 0x29,
    'f': 0x2A,
    'g': 0x2B,
    'h': 0x2C,
    'i': 0x2D,
    'j': 0x2E,
    'k': 0x2F,
    'l': 0x30,
    'm': 0x31,
    'n': 0x32,
    'o': 0x33,
    'p': 0x34,
    'q': 0x35,
    'r': 0x36,
    's': 0x37,
    't': 0x38,
    'u': 0x39,
    'v': 0x3A,
    'w': 0x3B,
    'x': 0x3C,
    'y': 0x3D,
    'z': 0x3E,
}

# gApSeedConfig, ROM data
SEED_CONFIG_ROM_OFFSET = 0x00100130
SEED_CONFIG_SIZE = 16
SEED_CONFIG_FIELDS = {   # ap.h name: (offset, size)
    "requiredDisks": (0, 2),
    "startingWeapons": (2, 1),
    "exSkillRank": (3, 1),
    "itemsanity": (4, 1),
    "exLifeSanity": (5, 1),
    "selectButton": (6, 1),
    "damageUpgrades": (7, 1),
    "cyberElves": (8, 1),
    "diskNamePopup": (9, 1),
    "infiniteLives": (10, 1),
    "finalStageRank": (11, 1),
    "enemyDiskMarkers": (12, 1),
    "legacyStages": (13, 1),
    "unused": (14, 1),
}

# Stage id: the ROM offset and byte size of each BG palette
STAGE_PALETTES = {
    1: [(0xC2C620, 96), (0xC2F180, 128), (0xC32C40, 192), (0xC357C0, 192), (0xC37954, 128)],
    2: [(0xC49C24, 192), (0xC4D8E4, 192), (0xC51364, 192), (0xC553A4, 224), (0xC573B0, 192), (0xC59344, 192), (0xC5A908, 96)],
    3: [(0xC5D8A4, 192), (0xC5F8C4, 224), (0xC62160, 224), (0xC63C48, 160)],
    4: [(0xC6B854, 224), (0xC6F834, 128), (0xC72EF4, 32), (0xC76F14, 192), (0xC7AFD4, 224)],
    5: [(0xC7DF64, 160), (0xC80878, 192), (0xC835B4, 160), (0xC85B68, 96)],
    6: [(0xC878C8, 192), (0xC89674, 192), (0xC8ADCC, 64), (0xC8C43C, 224), (0xC8DB20, 224), (0xC90714, 192), (0xC91A48, 224)],
    7: [(0xC940AC, 224), (0xC97E8C, 224), (0xC98DAC, 32), (0xC99864, 32)],
    8: [(0xC9C1F0, 224), (0xC9F520, 192), (0xCA0FF0, 224), (0xCA2E2C, 224)],
    9: [(0xCA45D8, 224), (0xCA7468, 224), (0xCA9A2C, 224), (0xCAB5E0, 224), (0xCAD918, 192)],
    10: [(0xCAFCFC, 192), (0xCB1A9C, 224), (0xCB3C84, 160), (0xCB5838, 96)],
    11: [(0xCB98FC, 224), (0xCBCE5C, 224), (0xCC057C, 192), (0xCC30FC, 128), (0xCC717C, 224)],
    12: [(0xC2C620, 96), (0xC3B994, 96), (0xC3F274, 64), (0xC42EB4, 160), (0xC45B58, 64)],
    13: [(0xC5F8C4, 224), (0xC65804, 224), (0xC6721C, 224), (0xC68F84, 224)],
    14: [(0xCC9724, 160), (0xCCBA24, 96), (0xCCE534, 96), (0xCD08E0, 96), (0xCD35B4, 96)],
    15: [(0xCD5898, 224), (0xCD7B34, 160), (0xCD92A4, 128), (0xCDBA6C, 224)],
    16: [(0xCDDCFC, 224), (0xCE0974, 192), (0xCE1970, 160), (0xCE422C, 224), (0xCE7E18, 192), (0xCEB280, 224)],
    17: [(0xCECBDC, 224), (0xCEE7A8, 224), (0xCF2888, 224), (0xCF6968, 224), (0xCF8A28, 224), (0xCF9DBC, 160)],
}
