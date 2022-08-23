import copy
from functools import reduce
import random
import string
import itertools

from argument_functions import prefered_initial_labellings
from framework_and_tree import create_framework, create_game_tree


player_winning_tree = []
cpu_winning_tree = []


# FOR TESTING
grounded = False
prefered = True


# init game
active_game = True

starting_argument = 'b'


listed = create_game_tree(create_framework(7), starting_argument, "p")

print(listed)


for x in listed:
    if len(x) % 2 == 0:
        cpu_winning_tree.append(x)
    elif len(x) % 2 == 1:
        player_winning_tree.append(x)


print("\nPLAYER WIN ROUTES: ", len(player_winning_tree), player_winning_tree)
print("CPU WIN ROUTES: ", len(cpu_winning_tree), cpu_winning_tree, "\n")


# --------------------BEGIN GAME----------------------


move_count = 0
game_path = []
player_moves = []
cpu_moves = []
player_move = False
current_argument = starting_argument
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



    while player_move is False:

        print("CPU TURN:\n")
        print("CURRENT MOVE COUNT:\n", move_count)


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

            print("SEARCH LIST: ", game_path)

            iterable_search_list = []

            for x in listed:
                if x[0:len(game_path)] == game_path and (len(x) % 2 == 0): 
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
                    print(list[len(game_path)])
                except IndexError:
                    print("FAAAAILLL", list[:len(game_path)])
                    gotdata = 'null'


            if len(alternative_options) == 0:
                print("No Options At All, CPU loses")
                active_game = False
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
            active_game = False
            break

        print("CPU MOVES:", current_argument)
        game_path.append(current_argument)
        print("GAME PATH:", game_path)






        player_move = True




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
                current_index = len(game_path)
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
                active_game = False
                break


        next_move_options = []

        print("Current Move", current_argument)



        try:
            possible_moves = [x for x in listed if x[0:len(game_path)] == game_path]

        except IndexError:
            print("No more possible moves for player in this line of arguing")
    

        print("Possible moves:", possible_moves)
        print("Listed:", listed)
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

                    current_argument = input("Player, select your next move: ").lower()

                    if current_argument.lower() not in next_move_options:
                        print("Not an appropriate choice.")
                    else:
                        game_path.append(current_argument)
                        player_moves.append(current_argument)

                        print("Player has chosen:", current_argument)
                        move_count += 1
                        player_move = False
                        break
            else:
                print("Next Move Break")
        
        elif len(alternative_options) != 0:

            while True:
                    print("ALT ROUTE")

                    current_argument = input("Player, select your next move: ").lower()

                    if current_argument.lower() is not alternative_options:
                        print("Not an appropriate choice.")
                    else:
                        player_moves.append(current_argument)

                        print("Player has chosen:", current_argument)
                        print("New Move Count is :", temp_move_count)
                        

                        move_count = temp_move_count + 1 
                        game_path.append(current_argument)

                        player_move = False

                        print("New game path is :", temp_move_count)
                        break


        else:
            print("No poss moves")
            active_game = False


        player_move = False


# if len(reduce(lambda count, l: count + len(l), paths, 0)) % 2 == 0: print("\nCPU Wins the argument game!")
# elif len(reduce(lambda count, l: count + len(l), paths, 0)) % 2 == 1: print("\nPLAYER Wins the argument game")

print("\nGame Path:", game_path)
print("Listed:", listed)
print("Player Path:", player_moves)
print("CPU Path:", cpu_moves)
print("All Paths:", paths)

