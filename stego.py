from PIL import Image


def to_int(seven: int, six: int, five: int, four: int, three: int, two: int, one: int, zero: int) -> int:
    return (seven << 7) + (six << 6) + (five << 5) + (four << 4) + (three << 3) + (two << 2) + (one << 1) + int(zero)


def bits_per_pixel(bit_planes: []) -> int:
    return bit_planes[0] + bit_planes[1] + bit_planes[2] + bit_planes[3]


def hide_bit(power_of_two: int, channel: int, bit: int) -> int:
    zero_bit_mask = 255 - (2 ** power_of_two)
    channel = channel & zero_bit_mask
    if bit:
        channel = channel + (2 ** power_of_two)
    return channel


def bit_pool_idea(alpha: int):
    for i in range(8):
        if alpha & (2 ** i):
            print("1", end="")
        else:
            print("0", end="")
    print("")


def image_to_bin_str(cover_file: str) -> []:
    return list(Image.open(cover_file).convert("RGBA").getdata())


def file_to_bin_str(hidden_file: str) -> []:
    bin_str_of_file = ""
    with open(hidden_file, "rb") as hidden:
        while hex_of_byte := hidden.read(1).hex():
            if hex_of_byte:
                bin_str_of_file += bin(int(hex_of_byte, 16))[2:].zfill(8)
    return bin_str_of_file


def stego(cover_file: str, hidden_file: str, bit_planes: []):
    cover_pixels = image_to_bin_str(cover_file)
    bin_str_to_hide = file_to_bin_str(hidden_file)

