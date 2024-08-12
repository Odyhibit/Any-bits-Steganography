from PIL import Image
import numpy as np
import pandas as pd


def get_image_data_bool(filename: str):
    """
    :param filename: path to the image
    :return: a numpy array of bits, with 24 individual bits per row.
            color channel bits are concatenated together.
    """
    img = Image.open(filename)
    img_array = np.array(img.getdata(), dtype="uint8")
    img_bool = np.unpackbits(img_array, axis=1)
    return img_bool.T


cover_image = "../test_images/test.png"
lsb_checkboxes = [False, False, False, False, False, False, False, True,
                  False, False, False, False, False, False, False, True,
                  False, False, False, False, False, False, False, True]
cover_img = get_image_data_bool(cover_image)
print(cover_img)

pd_idea = pd.DataFrame(cover_img)
lsb = pd_idea.loc[lsb_checkboxes]
lots_o_ones = np.ones((3, 100800), dtype="uint8")
pd_idea.loc[lsb_checkboxes] = lots_o_ones

print("The lsb ")
print(lsb)
print("With all values replaced with ones")
np_answer = np.packbits(pd_idea.T, axis=1)

print(pd_idea)
print(lots_o_ones.shape)
print(np_answer)
