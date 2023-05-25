from PIL import Image
import stego


def unhide_bit(power_of_two: int, channel: int) -> str:
    single_bit_mask = 2 ** power_of_two
    if (channel & single_bit_mask) > 0:
        return "1"
    else:
        return "0"



def unhide_from_pixel(pixel: (), bit_mask: [], bin_str: str) -> str:
    for chn in range(4):
        this_chn = pixel[chn]
        for i in range(8):
            if bit_mask[chn] & (int(2) ** i):
                recovered_bits = unhide_bit(i, this_chn)
                bin_str += str(recovered_bits)
    return bin_str


def parse_header(bin_file: []) -> (str, int, int):
    print(bin_file[:64])
    print(f"bin_file is {type(bin_file)}")
    end_filename = bin_file.index(0)
    filename = bin_file[5:end_filename]
    print("filename is", str(filename)[2:-1])
    file_size = int.from_bytes(bin_file[end_filename + 1: end_filename + 5], "little")
    print("Filesize", bin_file[end_filename + 1: end_filename + 5], file_size)
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


def is_known_stego():
    pass


def unstego(stego_file: str, bit_planes: []):
    stego_image = Image.open(stego_file)
    cover_pixels = stego.image_to_list_of_tuples(stego_image)
    hidden_bin_str = ""
    for pixel in cover_pixels:
        hidden_bin_str = unhide_from_pixel(pixel, bit_planes, hidden_bin_str)
    if is_stego(hidden_bin_str[:5 * 8]):
        print("string binary", hidden_bin_str[0:64])
        filename, potential_file = bin_str_to_file(hidden_bin_str)
        filename = "output_files/" + filename
        with open(filename, 'wb') as output:
            output.write(bytes(potential_file))
            return str(filename) + "\nwritten to disk"
    else:
        return "These settings do not produce recognizable content"
