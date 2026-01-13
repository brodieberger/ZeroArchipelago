def parse_item_update(item_update: bytes):
    if not item_update or len(item_update) < 2:
        return None

    value = item_update[0]
    ram_offset = item_update[1]

    if value == 0:
        return None

    # Inventory base address ends in B8
    byte_index = ram_offset - 0xB8
    if byte_index < 0:
        return None

    base_disk = byte_index * 4

    bit_to_offset = {
        0x01: 0,
        0x02: 1,
        0x04: 2,
        0x08: 3,
    }

    if value not in bit_to_offset:
        return None

    return base_disk + bit_to_offset[value] + 1




item_update = b'\x01\x19'
print (parse_item_update(item_update))