import tkinter as tk
from tkinter import ttk



root = tk.Tk()
root.title("venstertitel")

window_width = 300
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
# root.resizable(False, False)
root.iconbitmap('./media/icon1.ico')





message = tk.Label(root,text = "Hallo Yfke!")
message.pack()

tk.Label(root, text='Classic Label').pack()
ttk.Label(root, text='Themed Label').pack()



root.mainloop()

