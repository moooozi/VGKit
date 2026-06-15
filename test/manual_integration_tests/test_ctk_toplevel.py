import vgkit as vgk

vgk.set_appearance_mode("dark")


class ToplevelWindow(vgk.Toplevel):
    def __init__(self, *args, closing_event=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.protocol("WM_DELETE_WINDOW", self.closing)
        self.geometry("500x300")
        self.resizable(False, False)
        self.closing_event = closing_event

        self.label = vgk.Label(self, text="ToplevelWindow")
        self.label.pack(padx=20, pady=20)

        self.button_1 = vgk.Button(
            self, text="set dark", command=lambda: vgk.set_appearance_mode("dark")
        )
        self.button_1.pack(side="top", padx=40, pady=40)

    def closing(self):
        self.destroy()
        if self.closing_event is not None:
            self.closing_event()


class App(vgk.Window):
    def __init__(self):
        super().__init__()
        self.geometry("500x400")
        self.resizable(False, False)

        self.button_1 = vgk.Button(self, text="Open CTkToplevel", command=self.open_toplevel)
        self.button_1.pack(side="top", padx=40, pady=40)
        self.button_2 = vgk.Button(
            self,
            text="iconify toplevel",
            command=lambda: self.toplevel_window.iconify(),
        )
        self.button_2.pack(side="top", padx=40, pady=40)
        self.button_3 = vgk.Button(
            self, text="set light", command=lambda: vgk.set_appearance_mode("light")
        )
        self.button_3.pack(side="top", padx=40, pady=40)

        self.toplevel_window = None

    def open_toplevel(self):
        if self.toplevel_window is None:  # create toplevel window only if not already open
            self.toplevel_window = ToplevelWindow(self, closing_event=self.toplevel_close_event)

    def toplevel_close_event(self):
        self.toplevel_window = None


if __name__ == "__main__":
    app = App()
    app.mainloop()
