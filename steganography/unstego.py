from PIL import Image
from steganography import stego


def unhide_bit(power_of_two: int, channel: int) -> str:
    single_bit_mask = 2 ** power_of_two
    if (channel & single_bit_mask) > 0:
        return "1"
    else:
        return "0"


def unhide_from_pixel(pixel: (), bit_mask: [], bin_str: str) -> str:
    msb_first = (7, -1, -1)
    lsb_first = 8
    channels = 3 + bool(bit_mask[3])
    for chn in range(channels):
        this_chn = pixel[chn]
        for i in range(*msb_first):
            if bit_mask[chn] & (int(2) ** i):
                recovered_bits = unhide_bit(i, this_chn)
                bin_str += str(recovered_bits)
    return bin_str


def parse_header(bin_file: []) -> (str, int, int):
    end_filename = bin_file.index(0)
    filename = bin_file[5:end_filename]
    file_size = int.from_bytes(bin_file[end_filename + 1: end_filename + 5], "little")
    data_index = end_filename + 5
    return str(filename)[2:-1], data_index, file_size


def is_stego(first_five_bytes: str) -> bool:
    expected = "0101001101010100010001010100011101001111"  # STEGO in binary
    if first_five_bytes == expected:
        return True
    return False


def bin_str_to_file(bin_str: str):
    new_file = []
    for index in range(0, len(bin_str), 8):
        new_file.append(int(bin_str[index:index + 8], 2))
    filename, data_start, file_size = parse_header(bytes(new_file))
    return filename, new_file[data_start:data_start + file_size]


def unstego(stego_file: str, bit_planes: [], offset: int = 0) -> str:
    stego_image = Image.open(stego_file)
    with_alpha = bit_planes[3]
    cover_pixels = stego.image_to_list_of_tuples(stego_image, with_alpha)
    hidden_bin_str = ""
    for pixel in cover_pixels[offset:]:
        hidden_bin_str = unhide_from_pixel(pixel, bit_planes, hidden_bin_str)
    if is_stego(hidden_bin_str[:5 * 8]):
        filename, potential_file = bin_str_to_file(hidden_bin_str)
        filename = "output_files/" + filename
        with open(filename, 'wb') as output:
            output.write(bytes(potential_file))
            return str(filename) + "\nwritten to disk"
    else:
        return "These settings do not produce recognizable content"
