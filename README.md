# Any bits you want
Installation

Requires Python 

you will also need the Pillow library

    pip install --upgrade Pillow
    
download the files, or clone this repository

    git clone https://github.com/Odyhibit/Any-bits-Steganography
    
then run main.py 

    cd Any-bits-Steganography
    
    Python main.py
    
 
 For Windows a binary version that requires no installation, or setup is available under releases. Just unzip, and run the executable.



So if you have a need to hide some stuff in an image, and you want to hide it in specific bits in specific color channels.



![stego](https://github.com/Odyhibit/Any-bits-you-want-Steganography/assets/1384102/1b2dbf7e-6d26-4889-8988-8faa8bb254d4)


The stego tab allows you to pick a cover image, and a hidden file.
The cover image will be changed to a .PNG file with 4 channels. If the file to hide is not an image the preview will remain blank.

![stego_settings](https://github.com/Odyhibit/Any-bits-you-want-Steganography/assets/1384102/a0a5fee2-e51a-4ade-87d0-49ae74f54c49)


The settings tab is important, you can pick which bits you want to hide the hidden file in.
The filename will be stored as well, and used during file recovery.

![unstego](https://github.com/Odyhibit/Any-bits-you-want-Steganography/assets/1384102/1b643b0e-bdb3-44d8-91e3-7e86a885ed6d)


The unstego tab will recover a hidden file, and put it in the output folder. The file can be recovered only if the settings match the ones used to hide the file.


