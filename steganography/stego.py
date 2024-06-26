import os.path
from PIL import Image
import numpy as np


def to_int(seven: int, six: int, five: int, four: int, three: int, two: int, one: int, zero: int) -> int:
    return (seven << 7) + (six << 6) + (five << 5) + (four << 4) + (three << 3) + (two << 2) + (one << 1) + int(zero)


def bits_per_pixel(bit_planes: []) -> int:
    return bit_planes[0].bit_count() + bit_planes[1].bit_count() + bit_planes[2].bit_count() + bit_planes[3].bit_count()


def image_to_list_of_tuples(cover_image: Image, with_alpha: int) -> []:
    if with_alpha or 'A' in cover_image.getbands():
        image = cover_image.convert("RGBA").getdata()
        return list(image)
    else:
        image = cover_image.convert("RGB").getdata()
        return list(image)


def build_header(hidden_file: str, file_size: int) -> []:
    file_header = b"STEGO"
    file_name = os.path.basename(hidden_file)
    file_header += bytes(file_name, "ascii") + b'\x00'
    file_header += bytes(file_size.to_bytes(4, byteorder='little'))
    header_bin_str = ""
    for byte in file_header:
        header_bin_str += hex_to_bin_str(hex(byte))
    return header_bin_str


def hex_to_bin_str(hex_of_byte: str) -> str:
    return bin(int(hex_of_byte, 16))[2:].zfill(8)


def file_to_bin_str(hidden_file: str) -> []:
    # Changes hidden file into a binary string
    with open(hidden_file, "rb") as hidden:
        file_size = os.path.getsize(hidden_file)
        bin_str_of_file = build_header(hidden_file, file_size)
        while hex_of_byte := hidden.read(1).hex():
            if hex_of_byte:
                bin_str_of_file += hex_to_bin_str(hex_of_byte)
    return bin_str_of_file


def hide_bit(power_of_two: int, channel: int, bit: int) -> int:
    zero_target_bit = 255 - (2 ** power_of_two)
    channel = channel & zero_target_bit
    if bit:
        channel = channel | (2 ** power_of_two)
    return channel


def hide_in_channel(channel: int, bit_mask: int, bin_str: str) -> (int, str):
    for i in range(8):
        if bit_mask & (2 ** i) and len(bin_str) > 0:
            channel = hide_bit(i, channel, int(bin_str[0]))
            bin_str = bin_str[1:]
    return channel, bin_str


def save_stego_file(pixels: [], size: (), filename: str, bit_planes: []):
    if bit_planes[3]:
        output_img = Image.new("RGBA", size)
    else:
        output_img = Image.new("RGB", size)

    #print(pixels.shape, pixels.dtype)
    output_img.putdata(pixels)
    with open(filename, "wb") as file_out:
        output_img.save(file_out)


def stego(cover_file: str, hidden_file: str, bit_planes: [], output_filename: str, offset: int = 0):
    cover_image = Image.open(cover_file)
    size = (cover_image.width, cover_image.height)
    with_alpha = bit_planes[3]
    cover_pixels = image_to_list_of_tuples(cover_image, with_alpha)
    bin_str = file_to_bin_str(hidden_file)
    px_idx = offset
    num_channels = 3
    if with_alpha:
        num_channels = 4
    while bin_str:
        new_px = [0, 0, 0, 0]
        for chn in range(num_channels):
            new_px[chn], bin_str = hide_in_channel(cover_pixels[px_idx][chn], bit_planes[chn], bin_str)
        cover_pixels[px_idx] = (new_px[0], new_px[1], new_px[2], new_px[3])
        px_idx += 1
    save_stego_file(cover_pixels, size, output_filename, bit_planes)
    Image.open(output_filename, "r").show()
