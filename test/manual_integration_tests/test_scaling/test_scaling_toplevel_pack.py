import tkinter

import vgkit as vgk  # <- import the vgkit module

vgk.ScalingTracker.set_window_scaling(0.5)

vgk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
vgk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = (
    vgk.Window()
)  # create CTk window like you do with the Tk window (you can also use normal tkinter.Tk window)
app.geometry("400x480")
app.title("vgkit manual scaling test")

top_tk = vgk.Toplevel(app)
top_tk.geometry("500x500")

# app.minsize(200, 200)
# app.maxsize(520, 520)
# app.resizable(True, False)


def button_function():
    app.geometry(f"{200}x{200}")
    print("Button click", label_1.cget("text"))


def slider_function(value):
    vgk.set_widget_scaling(value * 2)
    vgk.set_window_scaling(value * 2)
    progressbar_1.set(value)


y_padding = 13

frame_1 = vgk.Container(master=app)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)
label_1 = vgk.Label(master=frame_1, justify=tkinter.LEFT)
label_1.pack(pady=y_padding, padx=10)
progressbar_1 = vgk.ProgressBar(master=frame_1)
progressbar_1.pack(pady=y_padding, padx=10)
button_1 = vgk.Button(master=frame_1, corner_radius=8, command=button_function)
button_1.pack(pady=y_padding, padx=10)
slider_1 = vgk.Slider(master=frame_1, command=slider_function, from_=0, to=1)
slider_1.pack(pady=y_padding, padx=10)
slider_1.set(0.5)
entry_1 = vgk.Entry(master=frame_1, placeholder_text="CTkEntry")
entry_1.pack(pady=y_padding, padx=10)
checkbox_1 = vgk.CheckBox(master=frame_1)
checkbox_1.pack(pady=y_padding, padx=10)
radiobutton_var = tkinter.IntVar(value=1)
radiobutton_1 = vgk.RadioButton(master=frame_1, variable=radiobutton_var, value=1)
radiobutton_1.pack(pady=y_padding, padx=10)
radiobutton_2 = vgk.RadioButton(master=frame_1, variable=radiobutton_var, value=2)
radiobutton_2.pack(pady=y_padding, padx=10)
s_var = tkinter.StringVar(value="on")
switch_1 = vgk.Switch(master=frame_1)
switch_1.pack(pady=y_padding, padx=10)


label_1 = vgk.Label(master=top_tk, justify=tkinter.LEFT)
label_1.pack(pady=y_padding, padx=10)
progressbar_1 = vgk.ProgressBar(master=top_tk)
progressbar_1.pack(pady=y_padding, padx=10)
button_1 = vgk.Button(master=top_tk, corner_radius=8, command=button_function)
button_1.pack(pady=y_padding, padx=10)
slider_1 = vgk.Slider(master=top_tk, command=slider_function, from_=0, to=1)
slider_1.pack(pady=y_padding, padx=10)
slider_1.set(0.5)
entry_1 = vgk.Entry(master=top_tk, placeholder_text="CTkEntry")
entry_1.pack(pady=y_padding, padx=10)
checkbox_1 = vgk.CheckBox(master=top_tk)
checkbox_1.pack(pady=y_padding, padx=10)
radiobutton_var = tkinter.IntVar(value=1)
radiobutton_1 = vgk.RadioButton(master=top_tk, variable=radiobutton_var, value=1)
radiobutton_1.pack(pady=y_padding, padx=10)
radiobutton_2 = vgk.RadioButton(master=top_tk, variable=radiobutton_var, value=2)
radiobutton_2.pack(pady=y_padding, padx=10)
switch_1 = vgk.Switch(master=top_tk)
switch_1.pack(pady=y_padding, padx=10)

app.mainloop()
