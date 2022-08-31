import random
import time
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

from save_load import load_frameowrk, save_framework

# ---------------------- WINNING STRATEGIES -------------------------

def remove_duplicates(list):
    # To remove duplicates
    all_opps_individuals = []   

    for l in list:
        if l not in all_opps_individuals:
            all_opps_individuals.append(l)

    return all_opps_individuals

# Function to find the paths that provide the winning strategy for the player
def find_winning_strategy(framework):


    # Filters through all the pa
    winning_paths = [x for x in framework if len(x) % 2 == 1]

    all_opp_args = []
    
    # Finda all the opponents moves that are made through the game tree
    for x in winning_paths:
        temp = x[1::2]
        all_opp_args.append(temp)

    # All the opponents moves within the game tree
    all_opp_args = [j for i in all_opp_args for j in i]
    # Prevents repatition of arguments
    all_opp_args = remove_duplicates(all_opp_args)


    winning_strategies = []

    # If there's a path that responds to all the OPP moves made within the tree, this is the winning strategy the user can implement
    for x in winning_paths:
        # Get all opp moves (even elements)
        opp_moves = x[1::2]

        # Checks if all the opp moves are in the path, if so return true
        result =  all(elem in opp_moves  for elem in all_opp_args)

        # Add winning strategies to list to return from function
        if result:
            print("Match")
            print("Winning strategy path", x)
            print("All OPP Moves", all_opp_args)
            winning_strategies.append(x)
        
    return winning_strategies




# ------------------- GETTERS -----------------------

def get_game_type():

    print("Value is", game_type.get())

    return game_type.get()

def get_next_move_entry():

   print(next_move_entry.get())

   return next_move_entry.get()

def list_match(list1, list2):
    match = False
    matches = []

    for x in list1:
        for y in list2:
            if x == y:
                matches.append(x)

    return matches

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
        game_path_label.set(update_game_path(paths, game_path, active_game))

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

            # Delay CPU response by 1 second
            time.sleep(1)

            print("CPU TURN:\n")


            try:
                if game_type == 'g':
                    possible_moves = []
                    print(listed)
                    for x in listed:
                        if x[0:move_count+1] == game_path:
                            possible_moves.append(x)

                if game_type == 'p':
                    possible_moves = []
                    print(listed)
                    for x in listed:
                        if x[0:move_count+1] == game_path:
                            possible_moves.append(x)

            except IndexError:
                print("CPU Moves indent break")
                break

            next_move_options = []

            print("POSS MOVES", possible_moves)



            

            if len(possible_moves) > 0:
                # print("Possible moves > 0: ", possible_moves)
                for x in possible_moves:

                    if x[0:move_count+1] == game_path:
                        next_move_options.append(x[move_count+1])

                    current_index = x.index(current_argument)
                    print("POSSIBLE MOVES")
                    print("Current Index", current_index)
                    print("Current Argument", current_argument)

                if len(next_move_options) != 0:
                    # print("Next move options", next_move_options)
                    print("CPU Options:", next_move_options)
                    print("Random choice type")
                    current_argument = random.choice(next_move_options)
                    cpu_moves.append(current_argument)
                    move_count += 1

                else:
                    active_game = False
            else:
                print("CPU LOSES")
                print("No more moves")

                active_game = False
                PLAYER_WIN = True
                game_path_label.set(update_game_path(paths, game_path, active_game))

                break


            

            print("CPU MOVES:", current_argument)
            game_path.append(current_argument)
            print("GAME PATH:", game_path)


            if game_path in listed:
                print(game_path, "Game path", "is in listed")
                print("CPU  Moves:", player_moves)
                paths.append(game_path)
                listed.remove(game_path)


                path_search = len(game_path)-2

                found_alterative = False
                list_of_alternatives = []

                while path_search >= 0 or found_alterative == True:

                    for list in listed:
                        print("Search")
                        if game_path[0:path_search] == list[0:path_search]:
                            print("MATCH")
                            list_of_alternatives.append(list[0:path_search])
                            print("New path", list[0:path_search])
                            found_alterative == True

                    path_search -= 2


                chosen_path = max(list_of_alternatives, key=len)


                if not chosen_path:
                    active_game = False
                    CPU_WIN = True
                    game_path_label.set(update_game_path(paths, game_path, active_game))
                    break
                else:


                    current_argument = chosen_path[-1]
                    move_count = len(chosen_path)-1

                    game_path = game_path[:move_count+1]

                    print("Selected Move:", current_argument)
                    print("Selected Point:", move_count)
                    print("Game Path", game_path)

                # makes checking for alternatives on the list at point [1] for CPU as that's next move, issue cause current argument isn't changed
                # Take opps args, find if there is argument next to it
                # move_count = 1

            player_move = True
            game_path_label.set(update_game_path(paths, game_path, active_game))







        while player_move is True and active_game is True:

            print("\nPLAYER TURN (Move Count):", move_count, "\n")


            alternative_options = []

            next_move_options = []



            print("Current Move", current_argument)




            try:
                if game_type == 'p':
                    possible_moves = []
                    print(listed)
                    for x in listed:
                        if x[0:move_count+1] == game_path:
                            possible_moves.append(x)

                if game_type == 'g':
                    possible_moves = []
                    print(listed)
                    for x in listed:
                        if x[0:move_count+1] == game_path and x[move_count+1] not in player_moves:
                            possible_moves.append(x)

            except IndexError:
                    print("No more possible moves for player")
                    active_game = False
                    CPU_WIN = True

                    break


            print("Listed:", listed)
            print("Possible moves:", possible_moves)

            print("Game Path:", game_path)



            # Go possible moves fist then elif for other options then else no more moves
            if len(possible_moves) > 0 and active_game is True:

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
            else:
                print("No poss moves")
                game_path_label.set(update_game_path(paths, game_path, active_game))
                CPU_WIN = True
                active_game = False


            if game_path in listed:
                print(game_path, "Game path", "is in listed")
                print("Player Moves:", player_moves)
                paths.append(game_path)
                listed.remove(game_path)

                path_search = len(game_path)-2

                found_alterative = False
                list_of_alternatives = []

                while path_search >= 0 or found_alterative == True:

                    for list in listed:
                        print("Search")
                        if game_path[0:path_search] == list[0:path_search]:
                            print("MATCH")
                            list_of_alternatives.append(list[0:path_search])
                            print("New path", list[0:path_search])
                            found_alterative == True

                    path_search -= 2

                chosen_path = max(list_of_alternatives, key=len)

                current_argument = chosen_path[-1]
                move_count = len(chosen_path)-1

                game_path = game_path[:move_count+1]

            player_move = False

    if PLAYER_WIN == True: error_message.set("CONGRATULATIONS, PLAYER WINS")
    if CPU_WIN == True: error_message.set("PLAYER LOSES")

    # Checks for winning path and if it has been apart of the paths played
    winners = find_winning_strategy(listed)
    matches = list_match(paths,winners)

    if matches:
        if PLAYER_WIN == True and len(list_match(paths,winners) > 0) : error_message.set("CONGRATULATIONS, PLAYER WINS WITH A WINNING STRATEGY INCLUDED: \n PATH:", matches)

    game_path_label.set(update_game_path(paths, game_path, active_game))

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

def checker(lst):

    if len(lst) > 0:  
        ele = lst[0]
        chk = True
        
        # Comparing each element with first item 
        for item in lst:
            if ele != item:
                chk = False
                break;
                
        if (chk == True): print("Equal")
        else: print("Not equal")  

    return chk          
  
def update_game_path(paths, game_path, active_game):

    game_path_string = str(game_path)
    display_path = 'GAME PATH: \n'

    previous_paths = ''

    for path in paths:
        previous_paths = previous_paths + str(path) + "\n"

    display_path = 'GAME PATH: \n' + previous_paths

    # Stops issue of a repeating character at the end of the game
    
    if len(game_path) > 0:
        if checker(game_path) == False:
            display_path = display_path + game_path_string


    if active_game is False:
        display_path = ''
        previous_paths = ''
        for path in paths:
            previous_paths = previous_paths + str(path) + "\n"

        display_path = 'GAME PATH: \n' + previous_paths




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


# --------------------- GUI -----------------------

# Initialises Tkinter window to add widgets in
window = tk.Tk()

window.grid_columnconfigure(0, weight=1)

# window.geometry('500x500')
var = tkinter.StringVar()

# Left side of the window
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

# Allows for labels text to change 
error_message = tk.StringVar()
hint_message = tk.StringVar()

# SECTION FOR USER TO MAKE NEXT MOVE
tk.Label(RIGHT_LEFT, text="ENTER NEXT MOVE:").grid(column=3, sticky="nsew", padx=5, pady=5)


next_move_entry = tk.Entry(RIGHT_LEFT)
next_move_entry.grid(column=3, sticky="nsew", padx=5, pady=5)

move_button = tk.Button(RIGHT_LEFT, text='MAKE MOVE', command=lambda: [var.set(get_next_move_entry())])
move_button.grid(column=3, sticky="nsew", padx=5, pady=5)

game_path_label = tk.StringVar()
game_path_label.set("GAME PATH:")

tk.Label(RIGHT_LEFT, textvariable=game_path_label).grid(column=3, sticky="nsew", padx=5, pady=5)


hint_button = tk.Button(RIGHT_LEFT, text='HINT', command=display_hints)
hint_button.grid(column=3, sticky="nsew", padx=5, pady=5)

tk.Label(RIGHT_LEFT, textvariable=hint_message).grid(column=3, sticky="nsew", padx=5, pady=5)


tk.Label(RIGHT_LEFT, textvariable=error_message).grid(column=3, sticky="nsew", padx=5, pady=20)

tk.mainloop()


