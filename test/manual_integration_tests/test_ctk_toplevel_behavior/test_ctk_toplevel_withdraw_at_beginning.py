import vgkit as vgk

app = vgk.Window()
app.geometry("400x400+300+300")

toplevel = vgk.Toplevel(app)
toplevel.geometry("350x240+800+300")

toplevel.withdraw()
toplevel.after(2000, toplevel.deiconify)

app.mainloop()
