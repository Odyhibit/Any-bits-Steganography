#!/usr/bin/env python
import math
import sys

import click
import numpy as np
from PIL import Image


@click.command()
@click.version_option(version="0.1", prog_name="neo_hide")
@click.option('-t', '--text', help='Text enclosed in single quotes.')
@click.option('-c', '--cover', type=click.Path(exists=True), help='filename of Cover image.')
@click.option('-s', '--stego', type=click.Path(), help='filename of Stego image.')
@click.option('-b', '--bits', type=int, default=7, show_default=True, help='The number of bits to hide per block.')
@click.option('-m', '--max', is_flag=True,help="use the Max block size possible.")
@click.option('--embed', '-e', is_flag=True,  help="Embed a message requires a cover file.")
@click.option('--extract', '-x', is_flag=True,  help="eXtract a message requires a stego file.")
# @click.option('-i', '--info', type=bool, default=False)
@click.option('-d', '--diff', is_flag=True, help="Count the number of bits that are different between two images.")
def main(text, cover, stego, bits, embed,extract, diff):
    # print(text, cover, stego, bits, embed)
    if embed and cover and text and stego:
        print(f"Embedding text into {stego}.")
        stego_image(cover, text, stego, bits)
    if extract and stego != "" and bits > 0:
        print("decoding the stego image.")
        print()
        results = unstego_image(stego, bits)
        print(results)
        print()
    if diff and cover and stego:
        print(compare_pixels(cover, stego))

    if not stego:
        print("nothing to do")


def compare_pixels(cover, stego):
    #  open images
    image_1 = Image.open(cover)
    image_2 = Image.open(stego)
    count = 0

    # Convert the images to a NumPy arrays
    image_array_1 = np.array(image_1.getdata())
    image_array_2 = np.array(image_2.getdata())
    if image_array_1.shape == image_array_2.shape:
        pixels, color_channels = image_array_1.shape
        for pixel in range(len(image_array_1)):
            for color_channel in range(color_channels):
                bit_1 = image_array_1[pixel][color_channel]
                bit_2 = image_array_2[pixel][color_channel]
                if bit_1 != bit_2:
                    count += (bit_1 ^ bit_2).bit_count()

        return f"Summary: {count} bits are different in these image pixels."
    return f"The images sizes do not match. "


def check_size(total_bits_to_hide: int, bits_per_block: int, width: int, height: int, color_channels: int = 3) -> bool:
    lsb_bits_available = width * height * color_channels
    block_size = 2 ** bits_per_block - 1
    if block_size != 0 and bits_per_block != 0:
        max_blocks_this_image = math.floor(lsb_bits_available / block_size)
        blocks_required = math.ceil(total_bits_to_hide / bits_per_block)

        if max_blocks_this_image >= blocks_required:
            # print(f"lsb bit count {lsb_bits_available} block size {block_size}")
            # print(f"max blocks this image {max_blocks_this_image} >= blocks required {blocks_required}")
            return True
    return False


def next_higher_power_of_two(target_num: int) -> int:
    target_num -= 1
    target_num |= target_num >> 1
    target_num |= target_num >> 2
    target_num |= target_num >> 4
    target_num |= target_num >> 5
    target_num |= target_num >> 6
    target_num |= target_num >> 7
    target_num += 1
    return target_num


def find_largest_block_size(total_bits_to_hide: int,
                            width: int,
                            height: int,
                            color_channels: int = 3) -> int:

    lsb_bits_available = width * height * color_channels
    lsb_next_power_of_two = next_higher_power_of_two(lsb_bits_available) - 1
    max_bits_per_block = lsb_next_power_of_two.bit_count()
    while not check_size(total_bits_to_hide, max_bits_per_block, width, height, color_channels):
        max_bits_per_block -= 1
        if max_bits_per_block <= 0:
            return 0
    return max_bits_per_block


def prepare_matrix(num_bits: int):
    """"""
    matrix = []
    size = 2 ** num_bits - 1
    for i in range(1, size + 1):
        string = bin(i)[2:].zfill(num_bits)
        vector = []
        for c in string:
            vector.append(int(c))
        matrix.append(vector)
    matrix = np.array(matrix).T
    return matrix


def hide_block(matrix, current_code, message):
    target_column = (message - matrix.dot(current_code)) % 2
    idx = 0
    found = False
    for i in matrix.T:
        if np.array_equal(i, target_column):
            found = True
            break
        idx += 1
    if not found:  # no modification needed
        return current_code
    stego = np.array(current_code)
    stego[idx] = (stego[idx] - 1) % 2
    return stego


def replace_block(img_list: [], stego_block: [], index: int):
    for offset in range(len(stego_block)):
        img_list[0][index + offset] = stego_block[offset]


def decode_blocks(img_lsb: [], block_size: int, matrix: []) -> []:
    unstego_bits = []
    for i in range(0, len(img_lsb[0]), block_size):
        offset = i
        stego_block = img_lsb[0][offset:offset + block_size]
        if len(stego_block) == block_size:
            discovered_bits = unhide_block(matrix, stego_block)
            for bit in discovered_bits:
                unstego_bits.append(bit)
    return unstego_bits


def unhide_block(matrix, stego):
    message = matrix.dot(stego)
    message = message % 2
    return message


def load_image(filename: str):
    img = Image.open(filename)
    width, height = img.width, img.height
    img_array = np.array(img.getdata())
    x, y = img_array.shape
    one_d_image = img_array.reshape(1, x * y)
    lsb = one_d_image & 0b1
    return width, height, lsb


def save_file(filename: str, width: int, height: int, stego_file: []):
    output_img = Image.new("RGB", (width, height))
    array_of_tuples = [tuple(pixel) for pixel in stego_file]
    output_img.putdata(array_of_tuples)
    with open(filename, "wb") as file_out:
        output_img.save(file_out)


def binary_string_to_ascii(unstego_bits: [], bits_per_letter: int = 7) -> str:
    # turn binary string list into ascii
    output = ""
    for i in range(0, len(unstego_bits), bits_per_letter):
        letter_bin_str = unstego_bits[i:i + 7]
        letter_bin = "".join(str(i) for i in letter_bin_str)
        letter_int = int(letter_bin, 2)
        if 31 < letter_int < 128:
            output += chr(int(letter_bin, 2))
        if letter_int == 0:
            return output
    return output


def ascii_to_binary_string(plain_text: str, bits_per_letter: int = 7) -> str:
    # turn 7 bit ascii into list of binary string

    return "".join([bin(i)[2:].zfill(bits_per_letter) for i in plain_text.encode("ascii")])


def unstego_image(stego_img, bits_per_block) -> str:
    width, height, stego_lsb = load_image(stego_img)
    block_size = 2 ** bits_per_block - 1
    matrix = prepare_matrix(bits_per_block)
    unstego_bits = decode_blocks(stego_lsb, block_size, matrix)
    decoded_bits = binary_string_to_ascii(unstego_bits)
    message = decoded_bits.split("\0x00")
    return message[0]


def stego_image(cover_image_filename: str,
                plain_text: str,
                stego_image_filename: str,
                bits_per_block,
                color_channels: int = 3):
    matrix = prepare_matrix(bits_per_block)
    block_size = 2 ** bits_per_block - 1
    binary_str = ascii_to_binary_string(plain_text)

    img = Image.open(cover_image_filename)
    width, height = img.width, img.height
    img_array = np.array(img.getdata())
    x, y = img_array.shape
    one_d_image = img_array.reshape(1, x * y)
    cover_lsb = one_d_image & 0b1

    print(f"max block size should be {find_largest_block_size(len(binary_str), width, height, color_channels)}")

    if not check_size(len(binary_str), bits_per_block, width, height, color_channels):
        print(f"Not enough room in this image for that message with that block size. Reduce one or the other. ")
        exit()
    encode_blocks(binary_str, block_size, matrix, bits_per_block, cover_lsb)
    message_mask = np.full((1, (x * y)), 254, dtype="uint8")
    stego_one_d = one_d_image[0] & message_mask
    stego_one_d += cover_lsb
    rows, cols = stego_one_d.shape
    stego_file = stego_one_d.reshape(cols // color_channels, color_channels)

    save_file(stego_image_filename, width, height, stego_file)


def encode_blocks(binary_list: [],
                  block_size: int,
                  matrix: [],
                  bits_per_block: int,
                  cover_lsb: []):
    for i, letter in enumerate(binary_list):
        cover_offset = i * block_size
        cover_block = cover_lsb[0][cover_offset:cover_offset + block_size]
        message_offset = i * bits_per_block
        message_bits = binary_list[message_offset:message_offset + bits_per_block]
        message_bits = np.array([int(i) for i in message_bits])

        if 0 != len(message_bits) < bits_per_block:  # pad the message bits to match block size.
            required_padding = bits_per_block - len(message_bits)
            message_bits = np.pad(message_bits, pad_width=(0, required_padding), mode='constant', constant_values=0)

        if len(message_bits) == bits_per_block:
            stego_block = hide_block(matrix, cover_block, message_bits)
            inx = i * block_size
            replace_block(cover_lsb, stego_block, inx)


if __name__ == "__main__":
    # stego_image("test_images/rgb_test_image.png","This is a test message","test_images/matrix_test_2.png", 14)
    # print(unstego_image("test_images/matrix_test_2.png", 14))
    # print(unstego_image("test_images/rgb_test_matrix_stego.png", 14))
    if len(sys.argv) == 1:
        main(['--help'])
    else:
        main()
