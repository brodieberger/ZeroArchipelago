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
AP_MAX_LOCATION_ID = 673
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
AP_IMPORT_COUNT = 16
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
AP_SLOT_OWN = 255
AP_LOC_FORM_FIRST = 383
AP_LOC_IMPORT_MINIBOSS_FIRST = 656
AP_IMPORT_MINIBOSS_COUNT = 18

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
CHECKED_LOCATIONS_COUNT = 85
SERVER_CHECKED = 0x0003EEFF
SERVER_CHECKED_COUNT = 85
RANK_ELF_USED = 0x0003EF54
DISKS_OWNED = 0x0003EF56
DEATH_COUNT = 0x0003EF58
KILL_REQUEST = 0x0003EF5A
CAN_ACCEPT_ITEMS = 0x0003EF5B
SHOP_SEEN = 0x0003EF5C
SHOP_SEEN_COUNT = 6

# gStageRun.id: Current stage
STAGE_ID = 0x000301A0

# gSpawnManager.area: Individual area of the stage
STAGE_AREA = 0x000300E1

# gApShopPrices
SHOP_PRICES_ROM_OFFSET = 0x00102D24
SHOP_PRICES_COUNT = 48
SHOP_PRICES_ELEMENT_SIZE = 2

# gApShopItems
SHOP_ITEMS_ROM_OFFSET = 0x00102D84
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
SEED_CONFIG_ROM_OFFSET = 0x0010034C
SEED_CONFIG_SIZE = 32
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
    "slotImport": (17, 15),
}

# Stage id: the ROM offset and byte size of each BG palette
STAGE_PALETTES = {
    1: [(0xD92960, 96), (0xD954C0, 128), (0xD98F80, 192), (0xD9BB00, 192), (0xD9DC94, 128)],
    2: [(0xDAFF64, 192), (0xDB3C24, 192), (0xDB76A4, 192), (0xDBB6E4, 224), (0xDBD6F0, 192), (0xDBF684, 192), (0xDC0C48, 96)],
    3: [(0xDC3BE4, 192), (0xDC5C04, 224), (0xDC84A0, 224), (0xDC9F88, 160)],
    4: [(0xDD1B94, 224), (0xDD5B74, 128), (0xDD9234, 32), (0xDDD254, 192), (0xDE1314, 224)],
    5: [(0xDE42A4, 160), (0xDE6BB8, 192), (0xDE98F4, 160), (0xDEBEA8, 96)],
    6: [(0xDEDC08, 192), (0xDEF9B4, 192), (0xDF110C, 64), (0xDF277C, 224), (0xDF3E60, 224), (0xDF6A54, 192), (0xDF7D88, 224)],
    7: [(0xDFA3EC, 224), (0xDFE1CC, 224), (0xDFF0EC, 32), (0xDFFBA4, 32)],
    8: [(0xE02530, 224), (0xE05860, 192), (0xE07330, 224), (0xE0916C, 224)],
    9: [(0xE0A918, 224), (0xE0D7A8, 224), (0xE0FD6C, 224), (0xE11920, 224), (0xE13C58, 192)],
    10: [(0xE1603C, 192), (0xE17DDC, 224), (0xE19FC4, 160), (0xE1BB78, 96)],
    11: [(0xE1FC3C, 224), (0xE2319C, 224), (0xE268BC, 192), (0xE2943C, 128), (0xE2D4BC, 224)],
    12: [(0xD92960, 96), (0xDA1CD4, 96), (0xDA55B4, 64), (0xDA91F4, 160), (0xDABE98, 64)],
    13: [(0xDC5C04, 224), (0xDCBB44, 224), (0xDCD55C, 224), (0xDCF2C4, 224)],
    14: [(0xE2FA64, 160), (0xE31D64, 96), (0xE34874, 96), (0xE36C20, 96), (0xE398F4, 96)],
    15: [(0xE3BBD8, 224), (0xE3DE74, 160), (0xE3F5E4, 128), (0xE41DAC, 224)],
    16: [(0xE4403C, 224), (0xE46CB4, 192), (0xE47CB0, 160), (0xE4A56C, 224), (0xE4E158, 192), (0xE515C0, 224)],
    17: [(0xE52F1C, 224), (0xE54AE8, 224), (0xE58BC8, 224), (0xE5CCA8, 224), (0xE5ED68, 224), (0xE600FC, 160)],
}
