import tkinter.filedialog
from tkinter import *
from tkinter import ttk


class MainWindow:

    def __init__(self, root):
        def pick_cover():
            cover_str.set(tkinter.filedialog.askopenfilename(filetypes=[("image files", ".png")]))

        def pick_stego():
            cover_str.set(tkinter.filedialog.askopenfilename(filetypes=[("image files", ".png")]))

        def pick_hidden():
            hidden_str.set(tkinter.filedialog.askopenfilename(filetypes=[]))

        root.title("Rubbish Steganography")
        # window.geometry("500x500")
        notebook = ttk.Notebook(root)
        notebook.pack(expand=True)

        # main screen
        main_screen = Frame(notebook)
        top_frame = Frame(main_screen)
        middle_frame = Frame(main_screen)
        bottom_frame = Frame(main_screen)

        # setting screen
        setting_screen = Frame(notebook)
        bit_planes_frame = Frame(setting_screen)

        # main screen variables
        cover_str = StringVar()
        cover_str.set("Cover Image")
        hidden_str = StringVar()
        hidden_str.set("Hidden File")
        stego_str = StringVar()

        # setting screen variables (bit plane checkboxes)
        a7, a6, a5, a4, a3, a2, a1, a0 = IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()
        r7, r6, r5, r4, r3, r2, r1, r0 = IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()
        g7, g6, g5, g4, g3, g2, g1, g0 = IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()
        b7, b6, b5, b4, b3, b2, b1, b0 = IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()

        # Main screen widgets
        cover_lbl = ttk.Label(top_frame, textvariable=cover_str, wraplength=250)
        cover_btn = Button(top_frame, text="Choose Image", command=pick_cover)
        hidden_lbl = ttk.Label(top_frame, textvariable=hidden_str, wraplength=250)
        hidden_btn = Button(top_frame, text="Choose File", command=pick_hidden)

        cover_canvas_label = ttk.Label(middle_frame, text="Cover Image")
        cover_canvas = Canvas(middle_frame, bd=2, width=150, height=150, relief="groove")
        hidden_canvas_label = ttk.Label(middle_frame, text="Hidden File")
        hidden_canvas = Canvas(middle_frame, bd=2, width=150, height=150, relief="ridge")
        arrow_lbl = Label(middle_frame, text="<-")

        load_stego_btn = Button(bottom_frame, text="Load Stego", command=pick_stego)
        save_output_btn = Button(bottom_frame, text="Save Output", state="disabled")
        save_stego_btn = Button(bottom_frame, text="Save Stego Image", state="disabled")
        stego_lbl = Label(bottom_frame, textvariable=stego_str, wraplength=250, bd=1, relief="ridge")

        # setting screen widgets
        alpha_lbl = ttk.Label(bit_planes_frame, text="Alpha")
        red_lbl = ttk.Label(bit_planes_frame, text="Red")
        green_lbl = ttk.Label(bit_planes_frame, text="Green")
        blue_lbl = ttk.Label(bit_planes_frame, text="Blue")
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

        #  main screen Frame Layout
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
        cover_canvas_label.grid(column=0, row=0)
        cover_canvas.grid(column=0, row=1)
        arrow_lbl.grid(column=1, row=1)
        hidden_canvas_label.grid(column=2, row=0)
        hidden_canvas.grid(column=2, row=1)

        # bottom Frame
        load_stego_btn.grid(column=0, row=0, sticky="E", padx=4, pady=6)
        save_output_btn.grid(column=1, row=0, padx=4, pady=6)
        save_stego_btn.grid(column=2, row=0, sticky="W", padx=4, pady=6)
        stego_lbl.grid(columnspan=3, row=1, sticky="E,W", padx=4, pady=6)

        # bit plane frame
        bit_planes_frame.grid(padx=20, pady=20, sticky="E,W")
        alpha_lbl.grid(column=0, row=1)
        alpha_7_chk.grid(column=1, row=1)
        alpha_6_chk.grid(column=2, row=1)
        alpha_5_chk.grid(column=3, row=1)
        alpha_4_chk.grid(column=4, row=1)
        alpha_3_chk.grid(column=5, row=1)
        alpha_2_chk.grid(column=6, row=1)
        alpha_1_chk.grid(column=7, row=1)
        alpha_0_chk.grid(column=8, row=1)
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
        blue_lbl.grid(column=0, rowspan=4)

        # notebook tabs
        notebook.add(main_screen, text="Files")
        notebook.add(setting_screen, text="Settings")

        # default settings
        alpha_7_chk.select()
        red_7_chk.select()
        green_7_chk.select()
        blue_7_chk.select()

if __name__ == '__main__':
    window = Tk()
    MainWindow(window)
    window.mainloop()
