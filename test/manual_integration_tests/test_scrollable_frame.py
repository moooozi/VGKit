import vgkit as vgk

vgk.set_default_color_theme("dark-blue")


app = vgk.Window()
app.grid_columnconfigure(2, weight=1)
app.grid_rowconfigure(1, weight=1)

toplevel = vgk.Toplevel()
switch = vgk.Switch(
    toplevel,
    text="Mode",
    command=lambda: vgk.set_appearance_mode("dark" if switch.get() == 1 else "light"),
)
switch.grid(row=0, column=0, padx=50, pady=50)

frame_1 = vgk.ScrollableFrame(
    app, orientation="vertical", label_text="should not appear", fg_color="transparent"
)
frame_1.grid(row=0, column=0, padx=20, pady=20)
frame_1.configure(label_text=None)

frame_2 = vgk.ScrollableFrame(app, orientation="vertical", label_text="CTkScrollableFrame")
frame_2.grid(row=1, column=0, padx=20, pady=20)

frame_3 = vgk.ScrollableFrame(app, orientation="horizontal")
frame_3.grid(row=0, column=1, padx=20, pady=20)

frame_4 = vgk.ScrollableFrame(app, orientation="horizontal", label_fg_color="transparent")
frame_4.grid(row=1, column=1, padx=20, pady=20)
frame_4.configure(label_text="CTkScrollableFrame")

frame_5 = vgk.ScrollableFrame(
    app, orientation="vertical", label_text="CTkScrollableFrame", corner_radius=0
)
frame_5.grid(row=0, column=2, rowspan=2, sticky="nsew")

for i in range(100):
    vgk.CheckBox(frame_1).grid(row=i, padx=10, pady=10)
    vgk.CheckBox(frame_2).grid(row=i, padx=10, pady=10)
    vgk.CheckBox(frame_3).grid(row=0, column=i, padx=10, pady=10)
    vgk.CheckBox(frame_4).grid(row=0, column=i, padx=10, pady=10)
    vgk.CheckBox(frame_5).grid(row=i, padx=10, pady=10)


app.mainloop()
