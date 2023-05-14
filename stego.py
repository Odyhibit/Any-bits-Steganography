from PIL import Image


def to_int(seven: int, six: int, five: int, four: int, three: int, two: int, one: int, zero: int) -> int:
    return (seven << 7) + (six << 6) + (five << 5) + (four << 4) + (three << 3) + (two << 2) + (one << 1) + int(zero)


def bits_per_pixel(bit_planes: []) -> int:
    return bit_planes[0].bit_count() + bit_planes[1].bit_count() + bit_planes[2].bit_count() + bit_planes[3].bit_count()


def hide_bit(power_of_two: int, channel: int, bit: int) -> int:
    zero_bit_mask = 255 - (2 ** power_of_two)
    channel = channel & zero_bit_mask
    if bit:
        channel = channel + (2 ** power_of_two)
    return channel


def image_to_list_of_tuples(cover_image: Image) -> []:
    return list(cover_image.convert("RGBA").getdata())


def file_to_bin_str(hidden_file: str) -> []:
    # Changes hidden file into a binary string
    bin_str_of_file = ""
    with open(hidden_file, "rb") as hidden:
        while hex_of_byte := hidden.read(1).hex():
            if hex_of_byte:
                bin_str_of_file += bin(int(hex_of_byte, 16))[2:].zfill(8)
    return bin_str_of_file


def hide_in_channel(channel: int, bit_mask: int, bin_str: str) -> (int, str):
    # process all 4 channels for 1 pixel
    for i in range(8):
        if bit_mask & (2 ** i) and bin_str:
            channel = hide_bit(i, channel, int(bin_str[0]))
            bin_str = bin_str[1:]
    return channel, bin_str


def save_stego_file(pixels: [], size, filename: str):
    output_img = Image.new("RGBA", size)
    output_img.putdata(pixels)
    output_img.save(filename)


def stego(cover_file: str, hidden_file: str, bit_planes: []):
    cover_image = Image.open(cover_file)
    size = (cover_image.width, cover_image.height)
    cover_pixels = image_to_list_of_tuples(cover_image)
    bin_str = file_to_bin_str(hidden_file)
    px_idx = 0

    while bin_str:
        new_px = [0, 0, 0, 0]
        for chn in range(4):
            new_px[chn], bin_str = hide_in_channel(cover_pixels[px_idx][chn], bit_planes[chn], bin_str)
        cover_pixels[px_idx] = (new_px[0], new_px[1], new_px[2], new_px[3])
        px_idx += 1

    save_stego_file(cover_pixels, size, "output_files/output.png")
