import copy
import random
import tkinter
from framework_and_tree import create_framework, create_game_tree
import os
import string
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

from save_load import load_frameowrk, save_framework




# ------------------- GETTERS -----------------------

def get_game_type():

    print("Value is", game_type.get())

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
    selection = int(listbox.get(listbox.curselection()))

    arguments_to_take = list(string.ascii_lowercase[:selection])

    arguments_to_take = sorted(arguments_to_take)


    count = 1

    initial_argument_listbox.delete(0,'end')

    for x in arguments_to_take:
        initial_argument_listbox.insert(count, x)


    count += 1


# -------------------- GAME FUNCTION ------------------------



def play_game(framework, initial_argument, game_type):

    global next_move_options
    global alternative_options 


    framework = load_frameowrk(framework)


    # init gamE

    print("Framework", framework)

    active_game = True

    listed = create_game_tree(framework, initial_argument, game_type)

    print(listed)


    # --------------------BEGIN GAME----------------------

    move_count = 0
    game_path = []
    player_moves = []
    cpu_moves = []
    player_move = False
    current_argument = initial_argument
    active_game = True

    PLAYER_WIN = False
    CPU_WIN = False


    paths = []




    # GET ALL PLAYER AND CPU PATHS, IF LISTED STILL EXISTS, REMOVE ALL DUPLICATES FROM LIST

    while (active_game):

        # Adds starting argument to game path
        if move_count == 0:
            game_path.append(current_argument)
            player_moves.append(current_argument)
            print("\nFirst Selection:", current_argument)
        else:
            print("\nLast Selection:", current_argument)


        error_message.set('')
        hint_message.set('')



        while player_move is False:

            print("CPU TURN:\n")


            next_move_options = []

            if move_count == 0:
                possible_moves = [x for x in listed if x[move_count] == current_argument]
            else:
                possible_moves = [x for x in listed if x[0:len(game_path)] == game_path]

            print("POSS MOVES", possible_moves)



            if game_path in listed:
                print(game_path, "Game path", "is in listed")

                paths.append(copy.deepcopy(game_path))
                listed.remove(copy.deepcopy(game_path))

                game_path.pop()
                game_path.pop()


                iterable_search_list = []

                for x in listed:
                    if x[0:len(game_path)] == game_path and (len(x) % 2 == 0) and len(game_path) > 3: 
                        print("iterable success", x[0:len(game_path)])
                        print("Appending", x)
                        iterable_search_list.append(x)


                # makes checking for alternatives on the list at point [0] for player as that's next move
                # move_count = 0

                # Does this to find next argument for player
                # Dictionary to store alternatives
                alternative_options = []
                temp_move_count = move_count


                for list in iterable_search_list:

                    try:
                        alternative_options.append(list[len(game_path)+1])
                        temp_move_count = len(game_path)+1
                        print("success")
                        print(list[len(game_path)+1])
                    except IndexError:
                        print("FAAAAILLL", list[:len(game_path)])


                if len(alternative_options) == 0:
                    print("No Options At All, CPU loses")
                    active_game = False
                    PLAYER_WIN = True
                    break
                else:
                    new_argument = random.choice(alternative_options)	
                    current_argument = new_argument
                    move_count = temp_move_count

            elif len(possible_moves) > 0:
                # print("Possible moves > 0: ", possible_moves)
                for x in possible_moves:
                    # reverse
                    current_index = len(game_path)
                    try:

                        if x[len(game_path)] == x[current_index]:

                            # Gets next argument that comes after current argument
                            print("CURRENT INDEX", current_index)
                            print("CPU NEXT MOVE OPTIONS", x[current_index])
                            next_move_options.append(x[current_index])
                        else: print("wahah")

                    except IndexError:
                        print("Next Argument doesn't exist for this option",
                            current_argument)
                        continue

                if len(next_move_options) != 0:
                    # print("Next move options", next_move_options)
                    print("Random choice type")
                    current_argument = random.choice(next_move_options)
                    cpu_moves.append(current_argument)
                    move_count += 1

                else:
                    active_game = False
            else:
                print("CPU LOSES")
                print("No more moves")

                game_path_label.set(update_game_path(paths, game_path))
                active_game = False
                PLAYER_WIN = True

                break

            print("CPU MOVES:", current_argument)
            game_path.append(current_argument)
            print("GAME PATH:", game_path)

            player_move = True
            game_path_label.set(update_game_path(paths, game_path))



        while player_move is True:

            print("\nPLAYER TURN (Move Count):", move_count, "\n")


            alternative_options = []



            if game_path in listed:
                print(game_path, "Game path", "is in listed")

                paths.append(copy.deepcopy(game_path))
                listed.remove(copy.deepcopy(game_path))

                game_path.pop()
                game_path.pop()


                print("SEARCH LIST: ", game_path)

                iterable_search_list = []

                for x in listed:
                    # reverse
                    current_index = len(game_path)-1
                    try:

                        if x[len(game_path)] == x[current_index]:

                            # Gets next argument that comes after current argument
                            print("CURRENT INDEX", current_index)
                            print("CPU NEXT MOVE OPTIONS", x[current_index])
                            alternative_options.append(x[current_index])
                        else: print("wahah")

                    except IndexError:
                        print("Next Argument doesn't exist for this option", current_argument)
                        continue     


                if len(alternative_options) == 0:
                    print("No Options At All, PLAYER loses")

                    game_path_label.set(update_game_path(paths, game_path))
                    active_game = False
                    CPU_WIN = True

                    break


            next_move_options = []

            print("Current Move", current_argument)



            try:
                possible_moves = [x for x in listed if x[0:len(game_path)] == game_path]

            except IndexError:
                print("No more possible moves for player in this line of arguing")
        

            print("Possible moves:", possible_moves)
            print("GAME PATH:", game_path)



            # Go possible moves fist then elif for other options then else no more moves
            if len(possible_moves) > 0:

                for x in possible_moves:
                    current_index = x[::-1].index(current_argument)
                    try:
                        next_move = x[len(game_path)]
                        if next_move not in next_move_options:
                            print(next_move)
                            next_move_options.append(next_move)
                    except IndexError:
                        print("Last Option for this one")
                        continue

                print("Next move options", next_move_options)

                if len(next_move_options) != 0:
                    while True:


                        print("waiting...")
                        move_button.wait_variable(var)
                        print("done waiting.")


                        current_argument = var.get()
                        current_argument = str(current_argument).lower()


                        if current_argument.lower() not in next_move_options:
                            error_message.set("Invalid Move, Try again")
                        else:
                            game_path.append(current_argument)
                            player_moves.append(current_argument)
                            error_message.set("Correct Argument!")

                            print("Player has chosen:", current_argument)
                            move_count += 1
                            player_move = False
                            break
                else:
                    print("Next Move Break")
            
            elif len(alternative_options) != 0:

                while True:
                        print("ALT ROUTE")


                        print("waiting...")
                        move_button.wait_variable(var)
                        print("done waiting.")


                        current_argument = var.get()
                        current_argument = str(current_argument).lower()

                        if current_argument.lower() is not alternative_options:
                            error_message.set("Invalid Move, Try again")

                        if game_type == 'g' and current_argument.lower() in player_moves:
                            error_message.set("Can't repeat arguments in grounded semantics")
                        else:
                            player_moves.append(current_argument)

                            error_message.set("Correct Argument!")

                            print("Player has chosen:", current_argument)
                            print("New Move Count is :", temp_move_count)
                            

                            move_count = temp_move_count + 1 
                            game_path.append(current_argument)
                            player_move = False

                            print("New game path is :", temp_move_count)
                            break


            else:
                print("No poss moves")
                game_path_label.set(update_game_path(paths, game_path))
                CPU_WIN = True

                active_game = False

      


            player_move = False

    if PLAYER_WIN == True: error_message.set("CONGRATULATIONS, PLAYER WINS")
    if CPU_WIN == True: error_message.set("PLAYER LOSES")
    game_path_label.set(update_game_path(paths, game_path))


    print("All Paths:", paths)



# ------------------- OTHER FUNCTIONS -----------------------

def populate_listbox():
    # iterate over files in
    # that directory
    listbox.delete(0,'end')
    for filename in os.listdir("pickles"):
        count = 0
        f = os.path.join("pickles", filename)
        # checking if it is a file
        if os.path.isfile(f):
            print(filename.rsplit( ".", 1 )[ 0 ])# Inserting the listbox items
            listbox.insert(count, filename.rsplit( ".", 1 )[ 0 ])

        count += 1


def display_hints():
    hint = 'Next move options: '
    if len(next_move_options) > 0:
        for values in next_move_options:
            hint = hint + ' ' + values
    elif len(alternative_options) > 0:
        for values in alternative_options:
            hint = hint + ' ' + values
    print(hint)

    hint_message.set(hint)



def update_game_path(paths, game_path):
    display_path = 'GAME PATH: \n'

    for path in paths:
        path = ""
        for values in path:
            path = path + str(values) + '-'

        display_path = path + "\n"

    game_path_string = ''
    for values in game_path:
        game_path_string = game_path_string + str(values) + '-'

    display_path = display_path + '\n' + game_path_string




    return display_path



def remove_argument():
    f = os.path.join("pickles", listbox.get(listbox.curselection()))
    os.remove("pickles/" + listbox.get(listbox.curselection()) + ".pickle")
    populate_listbox()

def load_argument():
    print("tee")
    selection = listbox.get(listbox.curselection())

    update = load_frameowrk(selection)
    display_framework_tree(update)
    img2 = ImageTk.PhotoImage(Image.open("graphs\Graph.png"),  master=LEFT_LEFT)
    image_label.config(image=img2)
    image_label.image = img2

    get_all_arguments()

def clear_all_arguments():

    for filename in os.listdir("pickles"):
        count = 0
        f = os.path.join("pickles", filename)
        # checking if it is a file
        if os.path.isfile(f):
            print(filename.rsplit( ".", 1 )[ 0 ])# Inserting the listbox items
            os.remove(f)

    populate_listbox()

def create_new_framework():
    # add length of pickle list to know what to save filename
    value = get_framework_size()
    print(int(value))
    current_framework = create_framework(int(value))

    display_framework_tree(current_framework)

    save_framework(value, current_framework)

    img2 = ImageTk.PhotoImage(Image.open("graphs\Graph.png"),  master=LEFT_LEFT)
    image_label.config(image=img2)
    image_label.image = img2
    populate_listbox()



current_framework = create_framework(7)

window = tk.Tk()

window.grid_columnconfigure(0, weight=1)

# window.geometry('500x500')
var = tkinter.StringVar()


# first level, window as parent
tk.Button(window, text='Browse ...').grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
tk.Label(window, text='Choose file:').grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

LEFT_LEFT = tk.Frame(window)

LEFT_LEFT.grid(row=2, column=0, sticky="nsew")


window.grid_columnconfigure(0, weight=0)
window.grid_columnconfigure(1, weight=1)

# LEFT LEFT SIDE 
tk.Label(LEFT_LEFT, text="Create an argument framework").grid(column=0, sticky="nsew", padx=5, pady=5)
tk.Label(LEFT_LEFT, text="Enter Number of Arguments to take (MAX 20):").grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

framework_amount_entry = tk.Entry(LEFT_LEFT)
framework_amount_entry.grid(column=0, sticky="nsew", padx=5, pady=5)

tk.Button(LEFT_LEFT, text='CREATE & SAVE NEW FRAMEWORK', command=create_new_framework).grid(column=0, sticky="nsew", padx=5, pady=5)


# LEFT RIGHT SIDE 
tk.Label(LEFT_LEFT, text="Load an argument framework").grid(sticky=tk.NW, padx=5, pady=5)


# Create a listbox
listbox = Listbox(LEFT_LEFT, selectmode="SINGLE", exportselection=0)
 

populate_listbox()
        

listbox.grid(sticky="nsew", padx=5, pady=5)

tk.Button(LEFT_LEFT, text='LOAD FRAMEWORK', command=load_argument).grid(sticky="nsew", padx=5, pady=5)
tk.Button(LEFT_LEFT, text='DELETE FRAMEWORK', command=remove_argument).grid(sticky="nsew", padx=5, pady=5)
tk.Button(LEFT_LEFT, text='CLEAR ALL SAVED FRAMEWORKS', command=clear_all_arguments).grid(sticky="nsew", padx=5, pady=5)


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
initial_argument_listbox = Listbox(RIGHT_LEFT, selectmode="SINGLE", exportselection=0)

initial_argument_listbox.grid(column=3, padx=5, pady=5)

# button
button = tk.Button(
    RIGHT_LEFT,
    text="PLAY",
    command= lambda: play_game(listbox.get(listbox.curselection()), get_initial_argument(), get_game_type()))

button.grid(column=3, sticky="nsew")

error_message = tk.StringVar()
hint_message = tk.StringVar()

# SECTION FOR USER TO MAKE NEXT MOVE
tk.Label(RIGHT_LEFT, text="ENTER NEXT MOVE:").grid(column=3, sticky="nsew", padx=5, pady=5)

next_move_entry = tk.Entry(RIGHT_LEFT)
next_move_entry.grid(column=3, sticky="nsew", padx=5, pady=5)

move_button = tk.Button(RIGHT_LEFT, text='MAKE MOVE', command=lambda: var.set(get_next_move_entry()))
move_button.grid(column=3, sticky="nsew", padx=5, pady=5)

game_path_label = tk.StringVar()
game_path_label.set("GAME PATH:")

tk.Label(RIGHT_LEFT, textvariable=game_path_label).grid(column=3, sticky="nsew", padx=5, pady=5)


hint_button = tk.Button(RIGHT_LEFT, text='HINT', command=display_hints)
hint_button.grid(column=3, sticky="nsew", padx=5, pady=5)

tk.Label(RIGHT_LEFT, textvariable=hint_message).grid(column=3, sticky="nsew", padx=5, pady=5)


tk.Label(RIGHT_LEFT, textvariable=error_message).grid(column=3, sticky="nsew", padx=5, pady=20)





tk.mainloop()


