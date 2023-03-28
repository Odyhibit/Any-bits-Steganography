import tkinter.filedialog
from tkinter import *
import sys
from tkinter import ttk


class MainWindow:

    def __init__(self, root):
        root.title("Rubbish Steganography")
        window.geometry("420x440")
        top_frame = Frame(root)
        middle_frame = Frame(root)
        bottom_frame = Frame(root)

        cover_str = StringVar()
        cover_str.set("Cover Image")
        hidden_str = StringVar()
        hidden_str.set("Hidden File")
        stego_str = StringVar()

        def pick_cover():
            cover_str.set(tkinter.filedialog.askopenfilename(filetypes=[("image files", ".png")]))

        def pick_stego():
            cover_str.set(tkinter.filedialog.askopenfilename(filetypes=[("image files", ".png")]))

        def pick_hidden():
            hidden_str.set(tkinter.filedialog.askopenfilename(filetypes=[]))

        #  Create controls
        cover_lbl = ttk.Label(top_frame, textvariable=cover_str, wraplength=250)
        cover_btn = Button(top_frame, text="Choose Image", command=pick_cover)
        hidden_lbl = ttk.Label(top_frame, textvariable=hidden_str, wraplength=250)
        hidden_btn = Button(top_frame, text="Choose File", command=pick_hidden)
        cover_canvas = Canvas(middle_frame, bd=2,  width=150, height=150, relief="groove")
        hidden_canvas = Canvas(middle_frame, bd=2, width=150, height=150, relief="ridge")
        arrow_lbl = Label(middle_frame, text="<-")
        load_stego_btn = Button(bottom_frame, text="Load Stego", command=pick_stego)
        save_output_btn = Button(bottom_frame, text="Save Output", state="disabled")
        save_stego_btn = Button(bottom_frame, text="Save Stego Image", state="disabled")
        stego_lbl = Label(bottom_frame, textvariable=stego_str, wraplength=250, bd=1, relief="ridge")


        #  Frame Layout
        top_frame.grid(padx=20, pady=20, sticky="E,W")
        top_frame.columnconfigure(0, minsize=250)
        top_frame.columnconfigure(1, minsize=100)

        middle_frame.grid(padx=20, pady=20, sticky="E,W")
        middle_frame.columnconfigure(0, minsize=150)
        middle_frame.columnconfigure(1, minsize=50)
        middle_frame.columnconfigure(2, minsize=150)

        bottom_frame.grid(padx=20, pady=20, sticky="E,W")
        bottom_frame.columnconfigure(0, minsize=100)
        bottom_frame.columnconfigure(1, minsize=100)
        bottom_frame.columnconfigure(2, minsize=100)


        #  Top Frame
        cover_lbl.grid(column=0, row=0, padx=4, pady=6)
        hidden_lbl.grid(column=0, row=1, padx=4, pady=6)
        cover_btn.grid(column=1, row=0, sticky="E,W", padx=4, pady=6)
        hidden_btn.grid(column=1, row=1, sticky="E,W", padx=4, pady=6)

        #  Middle Frame
        cover_canvas.grid(column=0, row=0)
        arrow_lbl.grid(column=1, row=0)
        hidden_canvas.grid(column=2, row=0)

        #bottom Frame
        load_stego_btn.grid(column=0, row=0, sticky="E", padx=4, pady=6)
        save_output_btn.grid(column=1, row=0, padx=4, pady=6)
        save_stego_btn.grid(column=2, row=0, sticky="W", padx=4, pady=6)
        stego_lbl.grid(columnspan=3, row=1, sticky="E,W", padx=4, pady=6)



if __name__ == '__main__':
    window = Tk()
    MainWindow(window)
    window.mainloop()
