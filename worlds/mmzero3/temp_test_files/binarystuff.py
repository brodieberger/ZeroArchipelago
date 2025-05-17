def hex_to_dec(address):
    scale = 16  # hexadecimal base
    num_of_bits = 4  # each hex character represents 4 bits

    # Extract only the second character, which represents the "found" status
    target_char = address[1]

    # Convert the character to a binary string
    byte = bin(int(target_char, scale))[2:].zfill(num_of_bits)
    print(byte)

    # Iterate over the bits from least significant to most significant
    for index, bit in enumerate(reversed(byte), start=1):
        print(f"Item {index}: Status: {bit}")

# Example usage
hex_to_dec("FF")
