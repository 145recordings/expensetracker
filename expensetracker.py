import tkinter as tk
from gui import Gui

#version 1.0.0
#created by Franklin
#12-25-2022

root = tk.Tk()
gui = Gui(root)
root.resizable(False,False)
root.geometry("500x400")
root.title("Expense Tracker v1.0.0")
root.mainloop()