import os

from PIL import Image
import numpy as np


def byte_to_bin_str(hex_of_byte: int) -> str:
    return str(bin(hex_of_byte))[2:].zfill(8)


def get_bit(test_byte: int, index: int) -> bool:
    mask = 1 << index
    test_byte &= ~mask
    return test_byte != 0


def get_channel_bits(bit_int: int) -> []:
    output = []
    for bit in range(7, -1, -1):
        if bool((bit_int >> bit) & 1):
            output.append(bit)
    return output


def set_bit(original_byte: int, index: int, hide_bit: bool) -> int:
    """Clear the indicated bit in original_byte leaving others intact, then
        Set the index bit of original_byte to 1 if bit_to_hide is truthy,
        else leave it 0, and return the new value."""
    mask = 1 << index
    original_byte &= ~mask  # Clear the bit indicated by the mask (if x is False)
    if hide_bit:
        original_byte |= mask  # If x was True, set the bit indicated by the mask.
    return original_byte  # Return the result, we're done.


def build_hiding_spots(planes: [], channels: str) -> []:
    hiding_bits = []
    color_channels = "RGBA"
    for letter in channels:
        channel_index = color_channels.index(letter)
        bits = get_channel_bits(planes[channel_index])
        # print(letter, channel_index, bits)
        for bit_num in bits:
            hiding_bits.append((channel_index, bit_num))
    return hiding_bits


def build_header(hidden_file: str) -> []:
    file_size = os.path.getsize(hidden_file)
    #print(file_size)
    file_header = b"STEGO"
    file_name = os.path.basename(hidden_file)
    file_header += bytes(file_name, "ascii") + b'\x00'
    file_header += bytes(file_size.to_bytes(4, byteorder='little'))
    return bytearray(file_header)


def main():
    #
    #  ******** example values   **********
    bit_planes = [0b11111111, 0b11111111, 0b11111111, 0b11]  # always RGBA
    stego("test.png", "xkcd.png", bit_planes, "test_output.png", 0)


def stego(cover_file: str, hidden_file: str, bit_planes: [], output_filename: str, offset: int = 0):
    channel_order = "ARGB"
    cover_image = Image.open(cover_file)
    image = cover_image.convert("RGBA").getdata()

    header = build_header(hidden_file)
    secret_file = open(hidden_file, "rb")

    numpy_array = np.array(image)
    hide_bits = build_hiding_spots(bit_planes, channel_order)
    current_pixel = offset
    hide_bit_index = 0
    for byte in header:
        byte = byte
        for bit in range(7, -1, -1):
            bit_to_hide = bool((byte >> bit) & 1)
            channel, bit_position = hide_bits[hide_bit_index]
            cover_val = numpy_array[current_pixel][channel]
            new_val = set_bit(cover_val, bit_position, bit_to_hide)
            numpy_array[current_pixel][channel] = new_val
            hide_bit_index += 1
            if hide_bit_index >= len(hide_bits):
                current_pixel += 1
                hide_bit_index = hide_bit_index % len(hide_bits)

    byte = secret_file.read(1)
    while byte:
        byte = int.from_bytes(byte, "little")
        for bit in range(7, -1, -1):
            bit_to_hide = bool((byte >> bit) & 1)
            channel, bit_position = hide_bits[hide_bit_index]
            cover_val = numpy_array[current_pixel][channel]
            new_val = set_bit(cover_val, bit_position, bit_to_hide)
            numpy_array[current_pixel][channel] = new_val
            hide_bit_index += 1
            if hide_bit_index >= len(hide_bits):
                current_pixel += 1
                hide_bit_index = hide_bit_index % len(hide_bits)
        byte = secret_file.read(1)

    output_img = Image.new("RGBA", (cover_image.width, cover_image.height))
    numpy_array = [tuple(l) for l in numpy_array]
    output_img.putdata(numpy_array)
    with open(output_filename, "wb") as file_out:
        output_img.save(file_out)


if __name__ == "__main__":
    main()
