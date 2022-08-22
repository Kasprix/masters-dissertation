# ------------------- GETTERS -----------------------

from msilib.schema import ListBox
import string
from tkinter import Listbox
from tkinter.messagebox import showinfo


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

def get_all_arguments():
    selection = int(ListBox.get(Listbox.curselection()))

    arguments_to_take = list(string.ascii_lowercase[:selection])

    arguments_to_take = sorted(arguments_to_take)


    count = 1

    initial_argument_listbox.delete(0,'end')

    for x in arguments_to_take:
        initial_argument_listbox.insert(count, x)


    count += 1
