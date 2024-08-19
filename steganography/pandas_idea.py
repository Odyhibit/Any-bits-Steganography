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
    #  print(f"Initial np array shape {img_array.shape}")
    img_bool = np.unpackbits(img_array, axis=1, bitorder="big")
    return img.width, img.height, img_bool.T


cover_image = "../test_images/test.png"
lsb_checkboxes = [False, False, False, False, False, False, False, True,
                  False, False, False, False, False, False, False, True,
                  False, False, False, False, False, False, False, True]
width, height, cover_img = get_image_data_bool(cover_image)


pd_idea = pd.DataFrame(cover_img)
lsb = pd_idea.loc[lsb_checkboxes]
lots_o_ones = np.ones((3, 100800), dtype="uint8")
pd_idea.loc[lsb_checkboxes] = lots_o_ones

np_answer = np.packbits(pd_idea.T, axis=1)


# This reshapes the array, and saves the image.
stego_image2 = Image.fromarray(np_answer.reshape((width, height, 3)).astype("uint8"))
stego_image2.save("test_panda_2.png")

# ************  test  *****************
print("Checking first 10 pixels of new stego file . . .")
img_stego = Image.open("test_panda_1.png")
stego_array = np.array(img_stego.getdata())
print(stego_array.shape)
print(stego_array[0:10, 0:3])

"""
with open("test_panda_1.png", "wb") as output_file:
    output_img = Image.new("RGB", (width, height))
    output_array = [tuple(i) for i in np_answer]
    output_img.putdata(output_array)
    output_img.save(output_file)


print(pd_idea)
print(lots_o_ones.shape)
print(np_answer.shape)

print(cover_img.T.shape)
print(cover_img.T[0:8, 0:24])

print("The lsb ", len(lsb))
print(lsb)
print("With all values replaced with ones")



"""




