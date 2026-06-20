import tkinter

import vgkit as vgk

vgk.set_appearance_mode("System")  # Other: "Dark", "Light"


class TestApp(vgk.Window):
    def __init__(self):
        super().__init__()
        self.geometry(f"{1400}x{700}")
        self.title("vgkit complete test")

        self.create_widgets_on_tk()
        self.create_widgets_on_ctk_frame()
        self.create_widgets_on_ctk_frame_customized()
        self.create_widgets_on_tk_frame_customized()

    def change_appearance_mode(self, value):
        """gets called by self.slider_1"""

        if value == 0:
            self.label_1.configure(text="mode: Light")
            vgk.set_appearance_mode("Light")
        elif value == 1:
            self.label_1.configure(text="mode: Dark")
            vgk.set_appearance_mode("Dark")
        else:
            self.label_1.configure(text="mode: System")
            vgk.set_appearance_mode("System")

    def create_widgets_on_tk(self):
        x, y = 150, 80

        self.label_1 = vgk.Label(
            master=self,
            text="widgets_on_tk",
        )
        self.label_1.place(x=x, y=y, anchor=tkinter.CENTER)

        self.frame_1 = vgk.Container(master=self, width=200, height=60)
        self.frame_1.place(x=x, y=y + 80, anchor=tkinter.CENTER)

        self.button_1 = vgk.Button(master=self)
        self.button_1.place(x=x, y=y + 160, anchor=tkinter.CENTER)

        self.entry_1 = vgk.Entry(master=self)
        self.entry_1.place(x=x, y=y + 240, anchor=tkinter.CENTER)

        self.progress_bar_1 = vgk.ProgressBar(master=self)
        self.progress_bar_1.place(x=x, y=y + 320, anchor=tkinter.CENTER)

        self.slider_1 = vgk.Slider(
            master=self,
            command=self.change_appearance_mode,
            from_=0,
            to=2,
            number_of_steps=2,
        )
        self.slider_1.place(x=x, y=y + 400, anchor=tkinter.CENTER)

        self.check_box_1 = vgk.CheckBox(master=self)
        self.check_box_1.place(x=x, y=y + 480, anchor=tkinter.CENTER)

    def create_widgets_on_ctk_frame(self):
        x, y = 450, 40

        self.ctk_frame = vgk.Container(master=self, width=300, height=600)
        self.ctk_frame.place(x=x, y=y, anchor=tkinter.N)

        self.label_2 = vgk.Label(
            master=self.ctk_frame, text="create_widgets_on_ctk_frame", width=200
        )
        self.label_2.place(relx=0.5, y=y, anchor=tkinter.CENTER)

        self.frame_2 = vgk.Container(master=self.ctk_frame, width=200, height=60)
        self.frame_2.place(relx=0.5, y=y + 80, anchor=tkinter.CENTER)

        self.button_2 = vgk.Button(master=self.ctk_frame)
        self.button_2.place(relx=0.5, y=y + 160, anchor=tkinter.CENTER)

        self.entry_2 = vgk.Entry(master=self.ctk_frame)
        self.entry_2.place(relx=0.5, y=y + 240, anchor=tkinter.CENTER)

        self.progress_bar_2 = vgk.ProgressBar(master=self.ctk_frame)
        self.progress_bar_2.place(relx=0.5, y=y + 320, anchor=tkinter.CENTER)

        self.slider_2 = vgk.Slider(
            master=self.ctk_frame,
            command=lambda v: self.label_2.configure(text=str(round(v, 5))),
        )
        self.slider_2.place(relx=0.5, y=y + 400, anchor=tkinter.CENTER)

        self.check_box_2 = vgk.CheckBox(master=self.ctk_frame)
        self.check_box_2.place(relx=0.5, y=y + 480, anchor=tkinter.CENTER)

    def change_frame_color(self, value):
        """gets called by self.slider_3"""

        def rgb2hex(rgb_color: tuple) -> str:
            return f"#{round(rgb_color[0]):02x}{round(rgb_color[1]):02x}{round(rgb_color[2]):02x}"

        col_1 = rgb2hex((100, 50, value * 250))
        col_2 = rgb2hex((20, value * 250, 50))

        self.tk_frame_customized.configure(bg=col_1)
        self.configure(bg=col_2)
        self.progress_bar_3.set(value)

    def create_widgets_on_ctk_frame_customized(self):
        x, y = 800, 40

        self.ctk_frame_customized = vgk.Container(master=self, width=300, height=600)
        self.ctk_frame_customized.place(x=x, y=y, anchor=tkinter.N)

        self.label_3 = vgk.Label(
            master=self.ctk_frame_customized,
            text="customized",
            font=("times", 16),
        )
        self.label_3.place(relx=0.5, y=y, anchor=tkinter.CENTER)
        self.label_3.configure(text_color=("#373E57", "#7992C1"))

        self.frame_3 = vgk.Container(master=self.ctk_frame_customized, width=200, height=60)
        self.frame_3.place(relx=0.5, y=y + 80, anchor=tkinter.CENTER)

        self.button_3 = vgk.Button(
            master=self.ctk_frame_customized,
            command=lambda: None,
            mode="round",
            font=("times", 16),
        )
        self.button_3.place(relx=0.5, y=y + 160, anchor=tkinter.CENTER)
        self.button_3.configure(hover_color=("#3A65E8", "#4376EE"))

        self.entry_3 = vgk.Entry(master=self.ctk_frame_customized, font=("times", 16))
        self.entry_3.place(relx=0.5, y=y + 240, anchor=tkinter.CENTER)
        self.entry_3.configure(corner_radius=20)
        self.entry_3.insert(0, "1234567890")
        self.entry_3.focus_set()

        self.progress_bar_3 = vgk.ProgressBar(master=self.ctk_frame_customized, height=16)
        self.progress_bar_3.place(relx=0.5, y=y + 320, anchor=tkinter.CENTER)
        self.progress_bar_3.configure(
            progress_color="#8AE0C3",
        )

        self.slider_3 = vgk.Slider(
            master=self.ctk_frame_customized,
            command=self.change_frame_color,
            from_=0,
            to=10,
        )
        self.slider_3.place(relx=0.5, y=y + 400, anchor=tkinter.CENTER)
        self.slider_3.configure(
            button_color="#8AE0C3",
            progress_color=("gray30", "gray10"),
        )
        self.slider_3.configure(from_=0, to=1)

        self.check_box_3 = vgk.CheckBox(
            master=self.ctk_frame_customized, corner_radius=50, font=("times", 16)
        )
        self.check_box_3.place(relx=0.5, y=y + 480, anchor=tkinter.CENTER)

    def create_widgets_on_tk_frame_customized(self):
        x, y = 1150, 40

        self.tk_frame_customized = tkinter.Frame(master=self, width=300, height=600, bg="darkred")
        self.tk_frame_customized.place(x=x, y=y, anchor=tkinter.N)

        self.label_4 = vgk.Label(master=self.tk_frame_customized, text="customized")
        self.label_4.place(relx=0.5, y=y, anchor=tkinter.CENTER)
        self.label_4.configure(text_color=("#373E57", "#7992C1"))

        self.frame_4 = vgk.Container(master=self.tk_frame_customized, width=200, height=60)
        self.frame_4.place(relx=0.5, y=y + 80, anchor=tkinter.CENTER)

        self.button_4 = vgk.Button(master=self.tk_frame_customized, command=lambda: x, mode="round")
        self.button_4.place(relx=0.5, y=y + 160, anchor=tkinter.CENTER)
        self.button_4.configure(hover_color=("#3A65E8", "#4376EE"))

        self.entry_4 = vgk.Entry(master=self.tk_frame_customized)
        self.entry_4.place(relx=0.5, y=y + 240, anchor=tkinter.CENTER)
        self.entry_4.insert(0, "1234567890")
        self.entry_4.focus_set()

        self.progress_bar_4 = vgk.ProgressBar(
            master=self.tk_frame_customized,
            height=16,
        )
        self.progress_bar_4.place(relx=0.5, y=y + 320, anchor=tkinter.CENTER)
        self.progress_bar_4.configure(progress_color="#8AE0C3")

        self.slider_4 = vgk.Slider(
            master=self.tk_frame_customized,
            command=self.change_frame_color,
            from_=0,
            to=10,
        )
        self.slider_4.place(relx=0.5, y=y + 400, anchor=tkinter.CENTER)
        self.slider_4.configure(
            button_color="#8AE0C3",
            progress_color=("gray30", "gray10"),
        )
        self.slider_4.configure(from_=0, to=1)

        self.check_box_4 = vgk.CheckBox(master=self.tk_frame_customized)
        self.check_box_4.place(relx=0.5, y=y + 480, anchor=tkinter.CENTER)


if __name__ == "__main__":
    test_app = TestApp()
    test_app.mainloop()
