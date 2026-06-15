import tkinter.messagebox

import vgkit as vgk

vgk.set_appearance_mode("dark")


class App(vgk.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("test filedialog")

        self.button_1 = vgk.Button(
            master=self,
            text="askopenfile",
            command=lambda: print(vgk.filedialog.askopenfile()),
        )
        self.button_1.pack(pady=10)
        self.button_2 = vgk.Button(
            master=self,
            text="askopenfiles",
            command=lambda: print(vgk.filedialog.askopenfiles()),
        )
        self.button_2.pack(pady=10)
        self.button_3 = vgk.Button(
            master=self,
            text="askdirectory",
            command=lambda: print(vgk.filedialog.askdirectory()),
        )
        self.button_3.pack(pady=10)
        self.button_4 = vgk.Button(
            master=self,
            text="asksaveasfile",
            command=lambda: print(vgk.filedialog.asksaveasfile()),
        )
        self.button_4.pack(pady=10)
        self.button_5 = vgk.Button(
            master=self,
            text="askopenfilename",
            command=lambda: print(vgk.filedialog.askopenfilename()),
        )
        self.button_5.pack(pady=10)
        self.button_6 = vgk.Button(
            master=self,
            text="askopenfilenames",
            command=lambda: print(vgk.filedialog.askopenfilenames()),
        )
        self.button_6.pack(pady=10)
        self.button_7 = vgk.Button(
            master=self,
            text="asksaveasfilename",
            command=lambda: print(vgk.filedialog.asksaveasfilename()),
        )
        self.button_7.pack(pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
