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
AP_MAX_LOCATION_ID = 792
AP_SELECT_CYCLE_SUB_WEAPON = 0
AP_SELECT_CYCLE_MAIN_WEAPON = 1
AP_SELECT_CYCLE_HEAD_CHIP = 2
AP_SELECT_CYCLE_BODY_CHIP = 3
AP_SELECT_CYCLE_FOOT_CHIP = 4
AP_SELECT_USE_SUBTANK = 5
AP_ELVES_VANILLA = 0
AP_ELVES_NO_PENALTY = 1
AP_ELVES_AUTO = 2
AP_AIR_SPIN_HOLD_UP = 0
AP_AIR_SPIN_JUMP_SLASH = 1
AP_AIR_SPIN_DOUBLE_TAP = 2
AP_LOC_EXLIFE_FIRST = 231
AP_EXLIFE_COUNT = 10
AP_LOC_ITEMSANITY_FIRST = 301
AP_ITEMSANITY_COUNT = 82
AP_LOC_IMPORT_FIRST = 400
AP_IMPORT_ELF_COUNT = 28
AP_ITEM_IMPORT_ACCESS_FIRST = 320
AP_IMPORT_COUNT = 16
AP_SHOP_LOCATION_FIRST = 703
AP_SHOP_TEXT_COLS = 12
AP_SHOP_NAME_LINES = 3
AP_SHOP_PLAYER_LINES = 2
AP_SHOP_TEXT_END = 255
AP_SHOP_KIND_PLAIN = 0
AP_SHOP_KIND_PROGRESSION = 1
AP_SHOP_KIND_TRAP = 2
AP_SHOP_OWN_WORLD = 4
AP_SHOP_SLOTS_MAX = 90
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
AP_SLOT_OWN = 255
AP_LOC_FORM_FIRST = 383
AP_LOC_IMPORT_MINIBOSS_FIRST = 656
AP_IMPORT_MINIBOSS_COUNT = 18
AP_LOC_IMPORT_EXLIFE_FIRST = 674
AP_IMPORT_EXLIFE_COUNT = 21
AP_LOC_IMPORT_SUBTANK_FIRST = 695
AP_LOC_IMPORT_REFIGHT_FIRST = 697

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
CHECKED_LOCATIONS_COUNT = 100
SERVER_CHECKED = 0x0003EF0E
SERVER_CHECKED_COUNT = 100
RANK_ELF_USED = 0x0003EF72
DISKS_OWNED = 0x0003EF74
DEATH_COUNT = 0x0003EF76
KILL_REQUEST = 0x0003EF78
CAN_ACCEPT_ITEMS = 0x0003EF79
SHOP_HINTED = 0x0003EF7A
SHOP_HINTED_COUNT = 12

# gStageRun.id: Current stage
STAGE_ID = 0x000301A0

# gSpawnManager.area: Individual area of the stage
STAGE_AREA = 0x000300E1

# gApShopPrices
SHOP_PRICES_ROM_OFFSET = 0x00103218
SHOP_PRICES_COUNT = 90
SHOP_PRICES_ELEMENT_SIZE = 2

# gApShopItems
SHOP_ITEMS_ROM_OFFSET = 0x001032CC
SHOP_ITEMS_COUNT = 90
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
SEED_CONFIG_ROM_OFFSET = 0x0010071C
SEED_CONFIG_SIZE = 36
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
    "attackMode": (14, 1),
    "randomEnemies": (15, 1),
    "doubleTapDash": (16, 1),
    "airSpinSlash": (17, 1),
    "slotImport": (18, 15),
    "requiredStages": (33, 1),
}

# Stage id: the ROM offset and byte size of each BG palette
STAGE_PALETTES = {
    1: [(0xDA8C88, 96), (0xDAB7E8, 128), (0xDAF2A8, 192), (0xDB1E28, 192), (0xDB3FBC, 128)],
    2: [(0xDC628C, 192), (0xDC9F4C, 192), (0xDCD9CC, 192), (0xDD1A0C, 224), (0xDD3A18, 192), (0xDD59AC, 192), (0xDD6F70, 96)],
    3: [(0xDD9F0C, 192), (0xDDBF2C, 224), (0xDDE7C8, 224), (0xDE02B0, 160)],
    4: [(0xDE7EBC, 224), (0xDEBE9C, 128), (0xDEF55C, 32), (0xDF357C, 192), (0xDF763C, 224)],
    5: [(0xDFA5CC, 160), (0xDFCEE0, 192), (0xDFFC1C, 160), (0xE021D0, 96)],
    6: [(0xE03F30, 192), (0xE05CDC, 192), (0xE07434, 64), (0xE08AA4, 224), (0xE0A188, 224), (0xE0CD7C, 192), (0xE0E0B0, 224)],
    7: [(0xE10714, 224), (0xE144F4, 224), (0xE15414, 32), (0xE15ECC, 32)],
    8: [(0xE18858, 224), (0xE1BB88, 192), (0xE1D658, 224), (0xE1F494, 224)],
    9: [(0xE20C40, 224), (0xE23AD0, 224), (0xE26094, 224), (0xE27C48, 224), (0xE29F80, 192)],
    10: [(0xE2C364, 192), (0xE2E104, 224), (0xE302EC, 160), (0xE31EA0, 96)],
    11: [(0xE35F64, 224), (0xE394C4, 224), (0xE3CBE4, 192), (0xE3F764, 128), (0xE437E4, 224)],
    12: [(0xDA8C88, 96), (0xDB7FFC, 96), (0xDBB8DC, 64), (0xDBF51C, 160), (0xDC21C0, 64)],
    13: [(0xDDBF2C, 224), (0xDE1E6C, 224), (0xDE3884, 224), (0xDE55EC, 224)],
    14: [(0xE45D8C, 160), (0xE4808C, 96), (0xE4AB9C, 96), (0xE4CF48, 96), (0xE4FC1C, 96)],
    15: [(0xE51F00, 224), (0xE5419C, 160), (0xE5590C, 128), (0xE580D4, 224)],
    16: [(0xE5A364, 224), (0xE5CFDC, 192), (0xE5DFD8, 160), (0xE60894, 224), (0xE64480, 192), (0xE678E8, 224)],
    17: [(0xE69244, 224), (0xE6AE10, 224), (0xE6EEF0, 224), (0xE72FD0, 224), (0xE75090, 224), (0xE76424, 160)],
}
