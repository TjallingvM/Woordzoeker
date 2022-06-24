# Woordzoeker Solver by Tjalling
from tkinter import ttk
from tkinter import *
import puzzleEngine as pe

def createGui():
    """"
    create a GUI to show the grid/words and solution
    """

    root = Tk()
    root.title("Woordzoeker 1.0")
    root.config(bg="grey")

    window_width = 1000
    window_height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    # root.resizable(False, False)
    root.iconbitmap('./media/icon1.ico')


    """
    For showing the letter and words grid, all labels inside a grid
    """
    master_frame = ttk.Frame(root)
    puzzle_frame = ttk.Frame(master_frame, borderwidth=5)
    controls_frame = ttk.Frame(master_frame, borderwidth=5)
    grid_frame = ttk.Frame(puzzle_frame, relief="ridge", width=300, height=450, borderwidth=5)
    words_frame = ttk.Frame(puzzle_frame,relief="ridge", width=200, height=450, borderwidth=5)
    new_btn = ttk.Button(controls_frame,text="New",width=5)
    quit_btn = ttk.Button(controls_frame, text="QUIT", width=5, command=root.destroy)
    strt_btn = ttk.Button(controls_frame, text="Start Solution", width=12)
    animation_btn = ttk.Checkbutton(controls_frame, text="Show Animation")

    labellist = []
    for x in range(5):
        for y in range(5):
            labelname = str(x) + str(y)
            labelname = ttk.Label(grid_frame,text=labelname)
            labellist.append(labelname)
            labelname.grid(row=y,column=x)


    master_frame.grid(row=0,column=0)
    puzzle_frame.grid(row=0,column=0,rowspan=2,columnspan=2,padx=15,pady=15)
    controls_frame.grid(row=0,column=3,rowspan=2,columnspan=2,padx=2,pady=2)
    grid_frame.grid(row=0, column=0,columnspan=1,rowspan=2,padx=8, pady=8)
    words_frame.grid(row=0, column=1,columnspan=1,rowspan=2,padx=8, pady=8)
    new_btn.grid(row=0,column=0,columnspan=1,rowspan=1,padx=2,pady=5,sticky=("W","N"))
    quit_btn.grid(row=0, column=1, columnspan=1, rowspan=1, padx=2, pady=5, sticky=("E","N"))
    strt_btn.grid(row=2, column=0, columnspan=1, rowspan=1, padx=2, pady=5, sticky=("N","E"))
    animation_btn.grid(row=1,column=0, columnspan=2, rowspan=1)

    
    
    
    
    root.mainloop()


if __name__ == '__main__':

    createGui()
