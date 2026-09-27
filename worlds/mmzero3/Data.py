# Fields to be read from gAp and gApSeedConfig.
# EWRAM address minus 0x02000000

# gAp.ready reads AP_READY once the game has booted, and gAp.version reads AP_VERSION.
AP_READY = 0x335A5041      # Spells out 'APZ3' in little endian
AP_VERSION = 24

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
AP_MAX_LOCATION_ID = 382
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
CHECKED_LOCATIONS_COUNT = 48
SERVER_CHECKED = 0x0003EEDA
SERVER_CHECKED_COUNT = 48
RANK_ELF_USED = 0x0003EF0A
DISKS_OWNED = 0x0003EF0C
DEATH_COUNT = 0x0003EF0E
KILL_REQUEST = 0x0003EF10
CAN_ACCEPT_ITEMS = 0x0003EF11

# gApShopPrices, ROM data: one u16 per shop slot
SHOP_PRICES_ROM_OFFSET = 0x001024D0
SHOP_PRICES_COUNT = 48
SHOP_PRICES_ELEMENT_SIZE = 2

# gApShopItems, ROM data: one fixed record a slot
SHOP_ITEMS_ROM_OFFSET = 0x00102530
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
SEED_CONFIG_ROM_OFFSET = 0x000FFBE8
SEED_CONFIG_SIZE = 12
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
}

# Stage id: the ROM offset and byte size of each BG palette
STAGE_PALETTES = {
    1: [(0x712F58, 96), (0x715AB8, 128), (0x719578, 192), (0x71C0F8, 192), (0x71E28C, 128)],
    2: [(0x73055C, 192), (0x73421C, 192), (0x737C9C, 192), (0x73BCDC, 224), (0x73DCE8, 192), (0x73FC7C, 192), (0x741240, 96)],
    3: [(0x7441DC, 192), (0x7461FC, 224), (0x748A98, 224), (0x74A580, 160)],
    4: [(0x75218C, 224), (0x75616C, 128), (0x75982C, 32), (0x75D84C, 192), (0x76190C, 224)],
    5: [(0x76489C, 160), (0x7671B0, 192), (0x769EEC, 160), (0x76C4A0, 96)],
    6: [(0x76E200, 192), (0x76FFAC, 192), (0x771704, 64), (0x772D74, 224), (0x774458, 224), (0x77704C, 192), (0x778380, 224)],
    7: [(0x77A9E4, 224), (0x77E7C4, 224), (0x77F6E4, 32), (0x78019C, 32)],
    8: [(0x782B28, 224), (0x785E58, 192), (0x787928, 224), (0x789764, 224)],
    9: [(0x78AF10, 224), (0x78DDA0, 224), (0x790364, 224), (0x791F18, 224), (0x794250, 192)],
    10: [(0x796634, 192), (0x7983D4, 224), (0x79A5BC, 160), (0x79C170, 96)],
    11: [(0x7A0234, 224), (0x7A3794, 224), (0x7A6EB4, 192), (0x7A9A34, 128), (0x7ADAB4, 224)],
    12: [(0x712F58, 96), (0x7222CC, 96), (0x725BAC, 64), (0x7297EC, 160), (0x72C490, 64)],
    13: [(0x7461FC, 224), (0x74C13C, 224), (0x74DB54, 224), (0x74F8BC, 224)],
    14: [(0x7B005C, 160), (0x7B235C, 96), (0x7B4E6C, 96), (0x7B7218, 96), (0x7B9EEC, 96)],
    15: [(0x7BC1D0, 224), (0x7BE46C, 160), (0x7BFBDC, 128), (0x7C23A4, 224)],
    16: [(0x7C4634, 224), (0x7C72AC, 192), (0x7C82A8, 160), (0x7CAB64, 224), (0x7CE750, 192), (0x7D1BB8, 224)],
    17: [(0x7D3514, 224), (0x7D50E0, 224), (0x7D91C0, 224), (0x7DD2A0, 224), (0x7DF360, 224), (0x7E06F4, 160)],
}
