import tkinter.filedialog
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps

import stego
import unstego


def pick_cover(event: Event = Event()):
    file_name = tkinter.filedialog.askopenfilename(initialdir="./test_images", filetypes=[("image files", ".png")])
    if not file_name:
        return
    cover_str.set(file_name)
    cover_img = Image.open(cover_str.get())
    cover_img = ImageOps.contain(cover_img, (140, 140))
    cover_img = ImageTk.PhotoImage(cover_img)
    cover_preview.configure(image=cover_img)
    cover_preview.image = cover_img


def pick_hidden(event: Event = Event()):
    hidden_str.set(tkinter.filedialog.askopenfilename(initialdir="./test_images", filetypes=[]))
    hidden_image = Image.open(hidden_str.get())
    hidden_image = ImageOps.contain(hidden_image, (140, 140))
    hidden_img = ImageTk.PhotoImage(hidden_image)
    hidden_preview.configure(image=hidden_img)
    hidden_preview.image = hidden_img


def perform_stego():
    cover = cover_str.get()
    hidden = hidden_str.get()
    bit_planes = get_bit_planes()
    output_filename = tkinter.filedialog.asksaveasfilename(initialdir="./output_files",
                                                           filetypes=[("image files", ".png")])
    save_stego_lbl.config(text="Hiding Bits . . .")
    stego.stego(cover, hidden, bit_planes, output_filename)
    output_filename_str.set(output_filename)

def pick_stego():
    # choose stego file to decode
    stego_str.set(tkinter.filedialog.askopenfilename(initialdir="./output_files",
                                                     filetypes=[("image files", ".png .jpg .jpeg .gif .bmp")]))
    stego_image = Image.open(stego_str.get())
    stego_image = ImageOps.contain(stego_image, (140, 140))
    stego_img = ImageTk.PhotoImage(stego_image)
    stego_lbl.configure(image=stego_img)
    stego_lbl.image = stego_img
    results = unstego.unstego(stego_str.get(), get_bit_planes())
    file_found_lbl.configure(text=results)


def print_bit_planes():
    print(a7.get(), a6.get(), a5.get(), a4.get(), a3.get(), a2.get(), a1.get(), a0.get())
    print(r7.get(), r6.get(), r5.get(), r4.get(), r3.get(), r2.get(), r1.get(), r0.get())
    print(g7.get(), g6.get(), g5.get(), g4.get(), g3.get(), g2.get(), g1.get(), g0.get())
    print(b7.get(), b6.get(), b5.get(), b4.get(), b3.get(), b2.get(), b1.get(), b0.get())


def get_bit_planes():
    red = stego.to_int(r7.get(), r6.get(), r5.get(), r4.get(), r3.get(), r2.get(), r1.get(), r0.get())
    green = stego.to_int(g7.get(), g6.get(), g5.get(), g4.get(), g3.get(), g2.get(), g1.get(), g0.get())
    blue = stego.to_int(b7.get(), b6.get(), b5.get(), b4.get(), b3.get(), b2.get(), b1.get(), b0.get())
    alpha = stego.to_int(a7.get(), a6.get(), a5.get(), a4.get(), a3.get(), a2.get(), a1.get(), a0.get())

    return [red, green, blue, alpha]





def perform_unstego():
    pass


root = Tk()
root.title("Any bit you want Steganography")
# window.geometry("500x500")
notebook = ttk.Notebook(root)
notebook.pack(expand=True)

# stego screen
main_screen = Frame(notebook)
top_frame = Frame(main_screen)
middle_frame = Frame(main_screen)
bottom_frame = Frame(main_screen)

# unstego screen
unstego_screen = Frame(notebook)
unstego_top_frame = Frame(unstego_screen)

# setting screen
setting_screen = Frame(notebook)
bit_planes_frame = Frame(setting_screen)

# main screen variables
cover_str = StringVar()
cover_str.set("Cover Image")
hidden_str = StringVar()
hidden_str.set("Hidden File")
output_filename_str = StringVar()
output_filename_str.set("File name")

# setting screen variables (bit plane checkboxes)
a7, a6, a5, a4, a3, a2, a1, a0 = IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()
r7, r6, r5, r4, r3, r2, r1, r0 = IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()
g7, g6, g5, g4, g3, g2, g1, g0 = IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()
b7, b6, b5, b4, b3, b2, b1, b0 = IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()

# unstego screen variables
stego_str = StringVar()
stego_str.set("File name")
file_found = StringVar()

# Main screen widgets
cover_lbl = ttk.Label(top_frame, textvariable=cover_str, wraplength=250)
cover_btn = Button(top_frame, text="Choose Image", command=pick_cover)
hidden_lbl = ttk.Label(top_frame, textvariable=hidden_str, wraplength=250)
hidden_btn = Button(top_frame, text="Choose File", command=pick_hidden)
cover_preview_label = ttk.Label(middle_frame, text="Cover Image")
placeholder = ImageTk.PhotoImage(Image.open("placeholder.png"))
cover_preview = Label(middle_frame, bd=2, relief="groove", image=placeholder)
cover_preview.bind("<Button-1>", pick_cover)
hidden_preview_label = ttk.Label(middle_frame, text="Hidden File")
hidden_preview = Label(middle_frame, bd=2, relief="ridge", image=placeholder)
hidden_preview.bind("<Button-1>", pick_hidden)
arrow_lbl = Label(middle_frame, text="<-")
save_stego_lbl = ttk.Label(bottom_frame, textvariable=output_filename_str, wraplength=250)
save_stego_btn = Button(bottom_frame, text="Save Stego Image", command=perform_stego)

#  main screen Frame Layout
top_frame.grid(padx=20, pady=20, sticky="E,W")
top_frame.columnconfigure(0, minsize=250)
top_frame.columnconfigure(1, minsize=100)

middle_frame.grid(padx=20, pady=20, sticky="E,W")
middle_frame.columnconfigure(0, minsize=150)
middle_frame.columnconfigure(1, minsize=50)
middle_frame.columnconfigure(2, minsize=150)

bottom_frame.grid(padx=20, pady=20, sticky="E,W")
bottom_frame.columnconfigure(0, minsize=250)
bottom_frame.columnconfigure(1, minsize=100)

#  Top Frame
cover_lbl.grid(column=0, row=0, padx=4, pady=6)
hidden_lbl.grid(column=0, row=1, padx=4, pady=6)
cover_btn.grid(column=1, row=0, sticky="E,W", padx=4, pady=6)
hidden_btn.grid(column=1, row=1, sticky="E,W", padx=4, pady=6)

# Middle Frame
cover_preview_label.grid(column=0, row=0)
cover_preview.grid(column=0, row=1)
arrow_lbl.grid(column=1, row=1)
hidden_preview_label.grid(column=2, row=0)
hidden_preview.grid(column=2, row=1)

# bottom Frame
save_stego_lbl.grid(column=0, row=0, padx=4, pady=6)
save_stego_btn.grid(column=1, row=0, sticky="W", padx=4, pady=6)

# setting screen widgets
alpha_lbl = Label(bit_planes_frame, text="Alpha")
red_lbl = Label(bit_planes_frame, text="Red")
green_lbl = Label(bit_planes_frame, text="Green")
blue_lbl = Label(bit_planes_frame, text="Blue")
alpha_7_chk = Checkbutton(bit_planes_frame, text="7", variable=a7)
alpha_6_chk = Checkbutton(bit_planes_frame, text="6", variable=a6)
alpha_5_chk = Checkbutton(bit_planes_frame, text="5", variable=a5)
alpha_4_chk = Checkbutton(bit_planes_frame, text="4", variable=a4)
alpha_3_chk = Checkbutton(bit_planes_frame, text="3", variable=a3)
alpha_2_chk = Checkbutton(bit_planes_frame, text="2", variable=a2)
alpha_1_chk = Checkbutton(bit_planes_frame, text="1", variable=a1)
alpha_0_chk = Checkbutton(bit_planes_frame, text="0", variable=a0)
red_7_chk = Checkbutton(bit_planes_frame, text="7", variable=r7)
red_6_chk = Checkbutton(bit_planes_frame, text="6", variable=r6)
red_5_chk = Checkbutton(bit_planes_frame, text="5", variable=r5)
red_4_chk = Checkbutton(bit_planes_frame, text="4", variable=r4)
red_3_chk = Checkbutton(bit_planes_frame, text="3", variable=r3)
red_2_chk = Checkbutton(bit_planes_frame, text="2", variable=r2)
red_1_chk = Checkbutton(bit_planes_frame, text="1", variable=r1)
red_0_chk = Checkbutton(bit_planes_frame, text="0", variable=r0)
green_7_chk = Checkbutton(bit_planes_frame, text="7", variable=g7)
green_6_chk = Checkbutton(bit_planes_frame, text="6", variable=g6)
green_5_chk = Checkbutton(bit_planes_frame, text="5", variable=g5)
green_4_chk = Checkbutton(bit_planes_frame, text="4", variable=g4)
green_3_chk = Checkbutton(bit_planes_frame, text="3", variable=g3)
green_2_chk = Checkbutton(bit_planes_frame, text="2", variable=g2)
green_1_chk = Checkbutton(bit_planes_frame, text="1", variable=g1)
green_0_chk = Checkbutton(bit_planes_frame, text="0", variable=g0)
blue_7_chk = Checkbutton(bit_planes_frame, text="7", variable=b7)
blue_6_chk = Checkbutton(bit_planes_frame, text="6", variable=b6)
blue_5_chk = Checkbutton(bit_planes_frame, text="5", variable=b5)
blue_4_chk = Checkbutton(bit_planes_frame, text="4", variable=b4)
blue_3_chk = Checkbutton(bit_planes_frame, text="3", variable=b3)
blue_2_chk = Checkbutton(bit_planes_frame, text="2", variable=b2)
blue_1_chk = Checkbutton(bit_planes_frame, text="1", variable=b1)
blue_0_chk = Checkbutton(bit_planes_frame, text="0", variable=b0)

# bit plane frame
bit_planes_frame.grid(padx=20, pady=20, sticky="E,W")
alpha_lbl.grid(column=0, row=5)
alpha_7_chk.grid(column=1, row=5)
alpha_6_chk.grid(column=2, row=5)
alpha_5_chk.grid(column=3, row=5)
alpha_4_chk.grid(column=4, row=5)
alpha_3_chk.grid(column=5, row=5)
alpha_2_chk.grid(column=6, row=5)
alpha_1_chk.grid(column=7, row=5)
alpha_0_chk.grid(column=8, row=5)
red_lbl.grid(column=0, row=2)
red_7_chk.grid(column=1, row=2)
red_6_chk.grid(column=2, row=2)
red_5_chk.grid(column=3, row=2)
red_4_chk.grid(column=4, row=2)
red_3_chk.grid(column=5, row=2)
red_2_chk.grid(column=6, row=2)
red_1_chk.grid(column=7, row=2)
red_0_chk.grid(column=8, row=2)
green_lbl.grid(column=0, row=3)
green_7_chk.grid(column=1, row=3)
green_6_chk.grid(column=2, row=3)
green_5_chk.grid(column=3, row=3)
green_4_chk.grid(column=4, row=3)
green_3_chk.grid(column=5, row=3)
green_2_chk.grid(column=6, row=3)
green_1_chk.grid(column=7, row=3)
green_0_chk.grid(column=8, row=3)
blue_lbl.grid(column=0, row=4)
blue_7_chk.grid(column=1, row=4)
blue_6_chk.grid(column=2, row=4)
blue_5_chk.grid(column=3, row=4)
blue_4_chk.grid(column=4, row=4)
blue_3_chk.grid(column=5, row=4)
blue_2_chk.grid(column=6, row=4)
blue_1_chk.grid(column=7, row=4)
blue_0_chk.grid(column=8, row=4)

# unstego screen widgets
stego_lbl = Label(unstego_top_frame, textvariable=stego_str, wraplength=250, bd=1, relief="ridge", image=placeholder)
file_found_lbl = Label(unstego_top_frame, textvariable=file_found, wraplength=250, bd=1, relief="ridge", )
load_stego_btn = Button(unstego_top_frame, text="Load Stego", command=pick_stego)
save_output_btn = Button(unstego_top_frame, text="Save Output", state="disabled")

# unstego frame layout
unstego_top_frame.grid(padx=90, pady=20, sticky="E,W")
load_stego_btn.grid(column=0, row=0, sticky="E,W", padx=4, pady=6)
save_output_btn.grid(column=1, row=0, padx=4, pady=6)
stego_lbl.grid(column=0, columnspan=2, row=1, sticky="E,W", padx=4, pady=6)
file_found_lbl.grid(column=0, columnspan=2, row=2, sticky="E,W", padx=4, pady=6)

# notebook tabs
notebook.add(main_screen, text="Stego")
notebook.add(unstego_screen, text="UnStego")
notebook.add(setting_screen, text="Settings")

# default settings
# alpha_7_chk.select()
red_7_chk.select()
green_7_chk.select()
blue_7_chk.select()

root.mainloop()
