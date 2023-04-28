from PIL import Image


def hide_bit(original: int, bit: int) -> int:
    striped = original & 0b01111111
    hidden_bit = bit << 7
    return striped + hidden_bit


def stego(cover_file: str, hidden_file: str):
    with Image.open(cover_file) as img, open(hidden_file, "rb") as hidden:
        px = img.load()
        b_message = ""
        while hex_of_byte := hidden.read(1).hex():
            if hex_of_byte:
                b_message += bin(int(hex_of_byte, 16))[2:].zfill(8)

        print("STEGO")
        print(b_message[0:64])
        width, height = img.width, img.height

        for y in range(height):
            for x in range(width):
                if len(b_message) > 0:
                    bit_to_hide = b_message[0:1]
                    image_byte = px[x, y]
                    px[x, y] = hide_bit(image_byte, int(bit_to_hide))
                    b_message = b_message[1:]
        img.save("test.png")


def unhide_byte(eight_bytes: [int]) -> int:
    byte_string = ""
    for byte in eight_bytes:
        high_bit = byte & 0b10000000
        bit = high_bit >> 7
        byte_string += str(bit)
    return int(byte_string, 2)


def unstego():
    with Image.open("test2.png") as img, open("output.png", "wb") as output:
        raw_bytes = bytearray()
        px = img.load()
        width, height = img.width, img.height
        data = []
        for y in range(height):
            for x in range(width):
                data.append(px[x, y])
        for i in range(0, len(data), 8):
            raw_bytes.append(unhide_byte(data[i:i + 8]))
        print(hex(unhide_byte(data[0:8])), hex(unhide_byte(data[8:16])))
        output.write(raw_bytes)
