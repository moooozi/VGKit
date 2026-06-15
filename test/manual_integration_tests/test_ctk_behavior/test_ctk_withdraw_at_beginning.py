import vgkit as vgk

app = vgk.Window()
app.geometry("400x240")

app.withdraw()
app.after(2000, app.deiconify)

app.mainloop()
