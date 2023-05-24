from PIL import Image
import stego


def unhide_bit(power_of_two: int, channel: int) -> int:
    single_bit_mask = 2 ** power_of_two
    return (channel & single_bit_mask) >> power_of_two # this needs to return {0,1}


def unhide_from_pixel(pixel: (), bit_mask: int, bin_str: str) -> str:
    for chn in range(4):
        this_chn = pixel[chn]
        for i in range(8):
            if bit_mask & (2 ** i):
                recovered_bits = unhide_bit(i, this_chn)
                bin_str += recovered_bits
    return bin_str


def parse_header(bin_file: bytes) -> (str, int, int):
    end_filename = bin_file.find(b'\x00')
    filename = bin_file[5:end_filename]
    file_size = int(bin_file[end_filename + 1: end_filename + 5])
    data_index = end_filename + 5
    return filename, data_index, file_size


def is_stego(first_five_bytes: str) -> bool:
    expected = "0101001101010100010001010100011101001111"  # STEGO in binary
    if first_five_bytes == expected:
        return True
    return False


def unstego(stego_file: str, bit_planes: []):
    stego_image = Image.open(stego_file)
    cover_pixels = stego.image_to_list_of_tuples(stego_image)
    hidden_bin_str = ""
    for pixel in cover_pixels:
        hidden_bin_str += unhide_from_pixel(pixel, bit_planes, hidden_bin_str)
    if is_stego(hidden_bin_str[:5 * 8]):
        potential_file = bin_str_to_file(hidden_bin_str)
        filename, data_index, file_size = parse_header(potential_file)
        with open(filename, 'wb') as output:
            output.write(potential_file[data_index: data_index + file_size])
    else:
        print("These settings do not produce recognizable content")


'''
def bin_str_to_file(bin_str: str):
    new_file = bytearray()
    for index in range(0, len(bin_str), 8):
        new_file.extend(bytes(int(bin_str[index:index + 8], 2)))
    filename, data_start, file_size = parse_header(new_file)
    with open(filename, "wb") as output:
        output.write(new_file[data_start:data_start + file_size])
    return new_file
'''
