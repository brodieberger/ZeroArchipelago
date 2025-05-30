import typing

from BaseClasses import Item, ItemClassification


class ItemData(typing.NamedTuple):
    code: int
    itemName: str
    classification: ItemClassification
    itemID: int


class MLSSItem(Item):
    game: str = "Mario & Luigi Superstar Saga"


itemList: typing.List[ItemData] = [
    ItemData(77771000, "5 Coins", ItemClassification.filler, 0x4),
    ItemData(77771001, "Mushroom", ItemClassification.filler, 0xA),
    ItemData(77771002, "Super Mushroom", ItemClassification.filler, 0xB),
    ItemData(77771003, "Ultra Mushroom", ItemClassification.filler, 0xC),
    ItemData(77771004, "Max Mushroom", ItemClassification.filler, 0xD),
    ItemData(77771005, "Nuts", ItemClassification.filler, 0xE),
    ItemData(77771006, "Super Nuts", ItemClassification.filler, 0xF),
    ItemData(77771007, "Ultra Nuts", ItemClassification.useful, 0x10),
    ItemData(77771008, "Max Nuts", ItemClassification.useful, 0x11),
    ItemData(77771009, "Syrup", ItemClassification.filler, 0x12),
    ItemData(77771010, "Super Syrup", ItemClassification.filler, 0x13),
    ItemData(77771011, "Ultra Syrup", ItemClassification.useful, 0x14),
    ItemData(77771012, "Max Syrup", ItemClassification.useful, 0x15),
    ItemData(77771013, "1-UP Mushroom", ItemClassification.useful, 0x16),
    ItemData(77771014, "1-UP Super", ItemClassification.useful, 0x17),
    ItemData(77771015, "Golden Mushroom", ItemClassification.useful, 0x18),
    ItemData(77771016, "Refreshing Herb", ItemClassification.filler, 0x19),
    ItemData(77771017, "Red Pepper", ItemClassification.useful, 0x1A),
    ItemData(77771018, "Green Pepper", ItemClassification.useful, 0x1B),
    ItemData(77771019, "Hoo Bean", ItemClassification.filler, 0x1D),
    ItemData(77771020, "Chuckle Bean", ItemClassification.filler, 0x1E),
    ItemData(77771021, "Woohoo Blend", ItemClassification.useful, 0x20),
    ItemData(77771022, "Hoohoo Blend", ItemClassification.useful, 0x21),
    ItemData(77771023, "Chuckle Blend", ItemClassification.useful, 0x22),
    ItemData(77771024, "Teehee Blend", ItemClassification.useful, 0x23),
    ItemData(77771025, "Hoolumbian", ItemClassification.useful, 0x24),
    ItemData(77771026, "Chuckoccino", ItemClassification.useful, 0x25),
    ItemData(77771027, "Teeheespresso", ItemClassification.useful, 0x26),
    ItemData(77771028, "Peasley's Rose", ItemClassification.progression, 0x31),
    ItemData(77771029, "Beanbean Brooch", ItemClassification.progression, 0x32),
    ItemData(77771030, "Red Goblet", ItemClassification.progression, 0x33),
    ItemData(77771031, "Green Goblet", ItemClassification.progression, 0x34),
    ItemData(77771032, "Red Chuckola Fruit", ItemClassification.progression, 0x35),
    ItemData(77771033, "White Chuckola Fruit", ItemClassification.progression, 0x36),
    ItemData(77771034, "Purple Chuckola Fruit", ItemClassification.progression, 0x37),
    ItemData(77771035, "Hammers", ItemClassification.progression, 0x38),
    ItemData(77771036, "Firebrand", ItemClassification.progression, 0x39),
    ItemData(77771037, "Thunderhand", ItemClassification.progression, 0x3A),
    ItemData(77771038, "Membership Card", ItemClassification.progression, 0x40),
    ItemData(77771039, "Winkle Card", ItemClassification.progression, 0x41),
    ItemData(77771040, "Peach's Extra Dress", ItemClassification.progression, 0x42),
    ItemData(77771041, "Fake Beanstar", ItemClassification.progression, 0x43),
    ItemData(77771042, "Red Pearl Bean", ItemClassification.progression, 0x45),
    ItemData(77771043, "Green Pearl Bean", ItemClassification.progression, 0x46),
    ItemData(77771044, "Bean Fruit 1", ItemClassification.progression_skip_balancing, 0x47),
    ItemData(77771045, "Bean Fruit 2", ItemClassification.progression_skip_balancing, 0x50),
    ItemData(77771046, "Bean Fruit 3", ItemClassification.progression_skip_balancing, 0x51),
    ItemData(77771047, "Bean Fruit 4", ItemClassification.progression_skip_balancing, 0x52),
    ItemData(77771048, "Bean Fruit 5", ItemClassification.progression_skip_balancing, 0x53),
    ItemData(77771049, "Bean Fruit 6", ItemClassification.progression_skip_balancing, 0x54),
    ItemData(77771050, "Bean Fruit 7", ItemClassification.progression_skip_balancing, 0x55),
    ItemData(77771051, "Blue Neon Egg", ItemClassification.progression, 0x56),
    ItemData(77771052, "Red Neon Egg", ItemClassification.progression, 0x57),
    ItemData(77771053, "Green Neon Egg", ItemClassification.progression, 0x60),
    ItemData(77771054, "Yellow Neon Egg", ItemClassification.progression, 0x61),
    ItemData(77771055, "Purple Neon Egg", ItemClassification.progression, 0x62),
    ItemData(77771056, "Orange Neon Egg", ItemClassification.progression, 0x63),
    ItemData(77771057, "Azure Neon Egg", ItemClassification.progression, 0x64),
    ItemData(77771058, "Beanstar Piece 1", ItemClassification.progression, 0x65),
    ItemData(77771059, "Beanstar Piece 2", ItemClassification.progression, 0x66),
    ItemData(77771060, "Beanstar Piece 3", ItemClassification.progression, 0x67),
    ItemData(77771061, "Beanstar Piece 4", ItemClassification.progression, 0x70),
    ItemData(77771062, "Spangle", ItemClassification.progression, 0x72),
    ItemData(77771063, "Beanlet 1", ItemClassification.useful, 0x73),
    ItemData(77771064, "Beanlet 2", ItemClassification.useful, 0x74),
    ItemData(77771065, "Beanlet 3", ItemClassification.useful, 0x75),
    ItemData(77771066, "Beanlet 4", ItemClassification.useful, 0x76),
    ItemData(77771067, "Beanlet 5", ItemClassification.useful, 0x77),
    ItemData(77771068, "Beanstone 1", ItemClassification.useful, 0x80),
    ItemData(77771069, "Beanstone 2", ItemClassification.useful, 0x81),
    ItemData(77771070, "Beanstone 3", ItemClassification.useful, 0x82),
    ItemData(77771071, "Beanstone 4", ItemClassification.useful, 0x83),
    ItemData(77771072, "Beanstone 5", ItemClassification.useful, 0x84),
    ItemData(77771073, "Beanstone 6", ItemClassification.useful, 0x85),
    ItemData(77771074, "Beanstone 7", ItemClassification.useful, 0x86),
    ItemData(77771075, "Beanstone 8", ItemClassification.useful, 0x87),
    ItemData(77771076, "Beanstone 9", ItemClassification.useful, 0x90),
    ItemData(77771077, "Beanstone 10", ItemClassification.useful, 0x91),
    ItemData(77771078, "Secret Scroll 1", ItemClassification.useful, 0x92),
    ItemData(77771079, "Secret Scroll 2", ItemClassification.useful, 0x93),
    ItemData(77771080, "Castle Badge", ItemClassification.useful, 0x9F),
    ItemData(77771081, "Pea Badge", ItemClassification.useful, 0xA0),
    ItemData(77771082, "Bean B. Badge", ItemClassification.useful, 0xA1),
    ItemData(77771083, "Counter Badge", ItemClassification.useful, 0xA2),
    ItemData(77771084, "Charity Badge", ItemClassification.useful, 0xA3),
    ItemData(77771085, "Bros. Badge", ItemClassification.useful, 0xA4),
    ItemData(77771086, "Miracle Badge", ItemClassification.useful, 0xA5),
    ItemData(77771087, "Ohoracle Badge", ItemClassification.useful, 0xA6),
    ItemData(77771088, "Mush Badge", ItemClassification.useful, 0xA7),
    ItemData(77771089, "Mari-Lui Badge", ItemClassification.useful, 0xA8),
    ItemData(77771090, "Muscle Badge", ItemClassification.useful, 0xA9),
    ItemData(77771091, "Spiny Badge AA", ItemClassification.useful, 0xAA),
    ItemData(77771092, "Mush Badge A", ItemClassification.useful, 0xAB),
    ItemData(77771093, "Grab Badge", ItemClassification.useful, 0xAC),
    ItemData(77771094, "Mush Badge AA", ItemClassification.useful, 0xAD),
    ItemData(77771095, "Power Badge", ItemClassification.useful, 0xAE),
    ItemData(77771096, "Wonder Badge", ItemClassification.useful, 0xAF),
    ItemData(77771097, "Beauty Badge", ItemClassification.useful, 0xB0),
    ItemData(77771098, "Salvage Badge", ItemClassification.useful, 0xB1),
    ItemData(77771099, "Oh-Pah Badge", ItemClassification.useful, 0xB2),
    ItemData(77771100, "Brilliant Badge", ItemClassification.useful, 0xB3),
    ItemData(77771101, "Sarge Badge", ItemClassification.useful, 0xB4),
    ItemData(77771102, "General Badge", ItemClassification.useful, 0xB5),
    ItemData(77771103, "Tank Badge", ItemClassification.useful, 0xB6),
    ItemData(77771104, "Bros. Rock", ItemClassification.useful, 0xBD),
    ItemData(77771105, "Soulful Bros.", ItemClassification.useful, 0xC0),
    ItemData(77771106, "High-End Badge", ItemClassification.useful, 0xC1),
    ItemData(77771107, "Bean Pants", ItemClassification.useful, 0xCC),
    ItemData(77771108, "Bean Trousers", ItemClassification.useful, 0xCD),
    ItemData(77771109, "Blue Jeans", ItemClassification.useful, 0xCE),
    ItemData(77771110, "Parasol Pants", ItemClassification.useful, 0xCF),
    ItemData(77771111, "Hard Pants", ItemClassification.useful, 0xD0),
    ItemData(77771112, "Heart Jeans", ItemClassification.useful, 0xD1),
    ItemData(77771113, "Plaid Trousers", ItemClassification.useful, 0xD2),
    ItemData(77771114, "#1 Trousers", ItemClassification.useful, 0xD3),
    ItemData(77771115, "Safety Slacks", ItemClassification.useful, 0xD4),
    ItemData(77771116, "Shroom Pants", ItemClassification.useful, 0xD5),
    ItemData(77771117, "Shroom Bells", ItemClassification.useful, 0xD6),
    ItemData(77771118, "Shroom Slacks", ItemClassification.useful, 0xD7),
    ItemData(77771119, "Peachy Jeans", ItemClassification.useful, 0xD8),
    ItemData(77771120, "Mushwin Pants", ItemClassification.useful, 0xD9),
    ItemData(77771121, "Mushluck Pants", ItemClassification.useful, 0xDA),
    ItemData(77771122, "Scandal Jeans", ItemClassification.useful, 0xDB),
    ItemData(77771123, "Street Jeans", ItemClassification.useful, 0xDC),
    ItemData(77771124, "Tropic Slacks", ItemClassification.useful, 0xDD),
    ItemData(77771125, "Hermetic Pants", ItemClassification.useful, 0xDE),
    ItemData(77771126, "Beanstar Pants", ItemClassification.useful, 0xDF),
    ItemData(77771127, "Peasley Slacks", ItemClassification.useful, 0xE0),
    ItemData(77771128, "Queen B. Jeans", ItemClassification.useful, 0xE1),
    ItemData(77771129, "B. Brand Jeans", ItemClassification.useful, 0xE2),
    ItemData(77771130, "Heart Slacks", ItemClassification.useful, 0xE3),
    ItemData(77771131, "Casual Slacks", ItemClassification.useful, 0xE4),
    ItemData(77771132, "Casual Coral", ItemClassification.useful, 0xEB),
    ItemData(77771133, "Harhall's Pants", ItemClassification.useful, 0xF1),
    ItemData(77771134, "Wool Trousers", ItemClassification.useful, 0xF3),
    ItemData(77771135, "Iron Pants", ItemClassification.useful, 0xF7),
    ItemData(77771136, "Greed Wallet", ItemClassification.useful, 0xF8),
    ItemData(77771137, "Bonus Ring", ItemClassification.useful, 0xF9),
    ItemData(77771138, "Excite Spring", ItemClassification.useful, 0xFA),
    ItemData(77771139, "Great Force", ItemClassification.useful, 0xFB),
    ItemData(77771140, "Power Grip", ItemClassification.useful, 0xFC),
    ItemData(77771141, "Cobalt Necktie", ItemClassification.useful, 0xFD),
    ItemData(77771142, "Game Boy Horror SP", ItemClassification.useful, 0xFE),
    ItemData(77771143, "Woo Bean", ItemClassification.skip_balancing, 0x1C),
    ItemData(77771144, "Hee Bean", ItemClassification.skip_balancing, 0x1F),
    ItemData(77771145, "Beanstar Emblem", ItemClassification.progression, 0x3E),
]

item_frequencies: typing.Dict[str, int] = {
    "5 Coins": 40,
    "Mushroom": 55,
    "Super Mushroom": 15,
    "Ultra Mushroom": 12,
    "Nuts": 10,
    "Super Nuts": 5,
    "Ultra Nuts": 5,
    "Max Nuts": 2,
    "Syrup": 28,
    "Super Syrup": 10,
    "Ultra Syrup": 10,
    "Max Syrup": 2,
    "1-Up Mushroom": 15,
    "1-Up Super": 5,
    "Golden Mushroom": 3,
    "Refreshing Herb": 9,
    "Red Pepper": 2,
    "Green Pepper": 2,
    "Hoo Bean": 100,
    "Chuckle Bean": 200,
    "Hammers": 3,
}

mlss_item_name_groups = {
    "Beanstar Piece": { "Beanstar Piece 1", "Beanstar Piece 2", "Beanstar Piece 3", "Beanstar Piece 4"},
    "Beanfruit": { "Bean Fruit 1", "Bean Fruit 2", "Bean Fruit 3", "Bean Fruit 4", "Bean Fruit 5", "Bean Fruit 6", "Bean Fruit 7"},
    "Neon Egg": { "Blue Neon Egg", "Red Neon Egg", "Green Neon Egg", "Yellow Neon Egg", "Purple Neon Egg", "Orange Neon Egg", "Azure Neon Egg"},
    "Chuckola Fruit": { "Red Chuckola Fruit", "Purple Chuckola Fruit", "White Chuckola Fruit"}
}

item_table: typing.Dict[str, ItemData] = {item.itemName: item for item in itemList}
items_by_id: typing.Dict[int, ItemData] = {item.code: item for item in itemList}

