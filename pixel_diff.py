import numpy as np
from PIL import Image

#  open images
image_1 = Image.open("test_images/rgb_test_image.png")
image_2 = Image.open("test_images/rgb_test_matrix_stego.png")
width = image_1.width
height = image_1.height
labels = ["red", "green", "blue"]

# Convert the images to a NumPy arrays
image_array_1 = np.array(image_1.getdata())
pixels, color_channels = image_array_1.shape
image_array_2 = np.array(image_2.getdata())
print(f"{width}, {height}  {pixels} - {color_channels}  {image_array_2.shape}")

for pixel in range(len(image_array_1)):
    for color_channel in range(color_channels):
        if image_array_1[pixel][color_channel] != image_array_2[pixel][color_channel]:
            print(f"{str(pixel // width).rjust(3)}, {str(pixel % width).rjust(3)}", end=" ")
            print(f"{str(labels[color_channel]).rjust(5)}", end=" ")
            print(f"({str(image_array_1[pixel][0]).rjust(3)},{str(image_array_1[pixel][1]).rjust(3)},{str(image_array_1[pixel][2]).rjust(3)})", end = "")
            print(f" - ({str(image_array_2[pixel][0]).rjust(3)},{str(image_array_2[pixel][1]).rjust(3)},{str(image_array_2[pixel][2]).rjust(3)})")


