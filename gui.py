import tkinter as tk
from tkinter import Listbox
from tkinter import ttk
from tkinter.messagebox import showinfo
from PIL import ImageTk, Image
from framework_and_tree import create_framework
from display_framework_tree import display_framework_tree

import matplotlib.pyplot as plt
from  matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np


def get_game_type():

    print("Value is", game_type.get())
    showinfo(title='Result', message=game_type.get())

    return game_type.get()

def get_next_move_entry():

   print(next_move_entry.get())

   return next_move_entry.get()

def get_framework_size():

   print(framework_amount_entry.get())

   return framework_amount_entry.get()

def get_initial_argument():

   print(initial_argument_listbox.get(initial_argument_listbox.curselection()))

   return initial_argument_listbox.get(initial_argument_listbox.curselection())


def create_new_framework():
    # add length of pickle list to know what to save filename
    value = get_framework_size()
    print(int(value))
    new_frame = create_framework(int(value))

    display_framework_tree(new_frame)

    img2 = ImageTk.PhotoImage(Image.open("graphs\Graph.png"),  master=LEFT_LEFT)
    image_label.config(image=img2)
    image_label.image = img2




test_framework = create_framework(7)

window = tk.Tk()

window.grid_columnconfigure(0, weight=1)

# window.geometry('500x500')

# first level, window as parent
tk.Button(window, text='Browse ...').grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
tk.Label(window, text='Choose file:').grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

LEFT_LEFT = tk.Frame(window)

LEFT_LEFT.grid(row=2, column=0, sticky="nsew")


window.grid_columnconfigure(0, weight=0)
window.grid_columnconfigure(1, weight=1)

# LEFT LEFT SIDE 
tk.Label(LEFT_LEFT, text="Create an argument framework").grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
tk.Label(LEFT_LEFT, text="Enter Number of Arguments to take (MAX 20):").grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

framework_amount_entry = tk.Entry(LEFT_LEFT)
framework_amount_entry.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

tk.Button(LEFT_LEFT, text='CREATE FRAMEWORK', command=create_new_framework).grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
tk.Button(LEFT_LEFT, text='SAVE FRAMEWORK').grid(row=3, column=0, sticky="nsew", padx=5, pady=5)


# LEFT RIGHT SIDE 
tk.Label(LEFT_LEFT, text="Load an argument framework").grid(sticky=tk.NW, padx=5, pady=5)


# Create a listbox
listbox = Listbox(LEFT_LEFT, selectmode="SINGLE")
 
# Inserting the listbox items
listbox.insert(1, "Data Structure")
listbox.insert(2, "Algorithm")
listbox.insert(3, "Data Science")
listbox.insert(4, "Machine Learning")
listbox.insert(5, "Blockchain")

listbox.grid(sticky="nsew", padx=5, pady=5)

tk.Button(LEFT_LEFT, text='LOAD FRAMEWORK').grid(sticky="nsew", padx=5, pady=5)
tk.Button(LEFT_LEFT, text='DELETE FRAMEWORK').grid(sticky="nsew", padx=5, pady=5)
tk.Button(LEFT_LEFT, text='CLEAR ALL SAVED FRAMEWORKS').grid(sticky="nsew", padx=5, pady=5)


# RIGHT LEFT SIDE 
RIGHT_LEFT = tk.Frame(window)
RIGHT_LEFT.grid(row=2, column=2, sticky=tk.N)

# Create a Label Widget to display the text or Image

img = ImageTk.PhotoImage(Image.open("graphs\Graph.png"),  master=LEFT_LEFT)
image_label = tk.Label(LEFT_LEFT, image = img)
image_label.grid(sticky="nsew",padx=5, pady=5)


game_type = tk.StringVar(window)

sizes = (('Grounded', 'g'),
         ('Prefered', 'p'))

# label
label = tk.Label(RIGHT_LEFT, text="SELECT GAME TYPE").grid(sticky="nsew",row=3, column=3,padx=5, pady=5)

# radio buttons
for size in sizes:
    r = tk.Radiobutton(
        RIGHT_LEFT,
        text=size[0],
        value=size[1],
        variable=game_type
    )
    r.grid(column=3, sticky="nsew", padx=5, pady=5)


label = tk.Label(RIGHT_LEFT, text="SELECT INITIAL ARGUMENT: ").grid(sticky="nsew",row=3, column=3,padx=5, pady=5)

# Create a listbox
initial_argument_listbox = Listbox(RIGHT_LEFT, selectmode="SINGLE")


# Inserting the listbox items
initial_argument_listbox.insert(1, "Data Structure")
initial_argument_listbox.insert(2, "Algorithm")
initial_argument_listbox.insert(3, "Data Science")
initial_argument_listbox.insert(4, "Machine Learning")
initial_argument_listbox.insert(5, "Blockchain")

initial_argument_listbox.grid(column=3, padx=5, pady=5)

# button
button = tk.Button(
    RIGHT_LEFT,
    text="PLAY",
    command=get_initial_argument).grid(column=3, sticky="nsew")




# SECTION FOR USER TO MAKE NEXT MOVE
tk.Label(RIGHT_LEFT, text="ENTER NEXT MOVE:").grid(column=3, sticky="nsew", padx=5, pady=5)

next_move_entry = tk.Entry(RIGHT_LEFT)
next_move_entry.grid(column=3, sticky="nsew", padx=5, pady=5)

tk.Button(RIGHT_LEFT, text='MAKE MOVE', command=get_next_move_entry).grid(column=3, sticky="nsew", padx=5, pady=5)


tk.mainloop()