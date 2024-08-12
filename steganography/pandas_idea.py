from PIL import Image
import numpy as np
import pandas as pd



def load_image(filename: str):
    img = Image.open(filename)
    img_array = np.array(img.getdata(), dtype="uint8")
    print("img array.shape", img_array.shape)
    img_bool = np.unpackbits(img_array, axis=1)
    print("unpacked", img_bool.shape)
    return img_bool.T


cover_image = "../test_images/test.png"
lsb_checkboxes = [False, False, False, False, False, False, False, True,
                  False, False, False, False, False, False, False, True,
                  False, False, False, False, False, False, False, True]
cover_img = load_image(cover_image)
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

