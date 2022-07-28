import random
import string
import itertools

from argument_functions import prefered_initial_labellings
from framework_and_tree import create_framework, create_game_tree
from test import alternative_options


player_winning_tree = []
cpu_winning_tree = []

# init game
active_game = True



while True:
    number_of_arguments = int(input("Select number of arguments to play with (Max 20):"))
    if number_of_arguments > 20:
      print("Not an appropriate choice.")
    else:
      break
        
# Initialises Framework with variable of arguments set by user
list_of_objects = create_framework(int(number_of_arguments))
grounded_framework = prefered_initial_labellings(list_of_objects)


options = list(string.ascii_lowercase[:int(number_of_arguments)])
print("Argument options to start with:", str(options), "\n")


# Ensures user picks valid option
while True:
    starting_argument = input("Input argument to play with: ")
    if starting_argument.lower() not in options:
        print("Not an appropriate choice.")
    else:
        break


listed = create_game_tree(grounded_framework, starting_argument)


for x in listed:
  if len(x) % 2 == 0: cpu_winning_tree.append(x)
  elif len(x) % 2 == 1: player_winning_tree.append(x) 


print("\nPLAYER WIN ROUTES: ", len(player_winning_tree) ,player_winning_tree)
print("CPU WIN ROUTES: ", len(cpu_winning_tree) , cpu_winning_tree, "\n")

print(listed)


# --------------------BEGIN GAME----------------------


move_count = 0
game_path = []
player_moves = []
cpu_moves = []
player_move = False
current_argument = starting_argument
active_game = True
grounded = True
prefered = False

path_counters = []

# TODO remove all played moves, keep remaining moves for each player, CAN, get all other users moves to see if there's an additional move to make
# GET ALL PLAYER AND CPU PATHS, IF LISTED STILL EXISTS, REMOVE ALL DUPLICATES FROM LIST

while(active_game):

  try:
    possible_moves = [x for x in listed if x[move_count] == current_argument]

  except IndexError:
    print("High Level No More Moves")
    break

  # Adds starting argument to game path
  if move_count == 0:
    game_path.append(current_argument)
    player_moves.append(current_argument)
    print("\nFirst Selection:", current_argument)
  else:
    print("\nLast Selection:", current_argument)


  while player_move is False:

    print("CPU TURN:\n")

    try:
      possible_moves = [x for x in listed if x[move_count] == current_argument and move_count < len(x) and x[-1] != current_argument]

    except IndexError:
      print("CPU Moves indent break")
      break

    next_move_options = []    

    # List of winning strategies for the CPU
    prefered_cpu_options = [x for x in cpu_winning_tree if x[move_count] == current_argument and move_count < len(x)]

    # print("Winning Options", prefered_cpu_options)
    # print("Possible Options", possible_moves)

    # Follows the inverse of the rule for the CPU (function is from the perspective of player so cpu will do opposite of grounded and prefered rules)
    # alternative_path = alternative_options(alternative_path, game_path, cpu_moves, not grounded, not prefered)


    if len(prefered_cpu_options) > 0:
      # print("Prefered choice")
      best_move = min(prefered_cpu_options, key=len)
      current_argument = best_move[move_count+1]

    elif len(possible_moves) > 0:
      # print("Possible moves > 0: ", possible_moves)
      for x in possible_moves:
        current_index = x.index(current_argument)
        try:

          # Gets next argument that comes after current argument
          next_move_options.append(x[current_index+1]) 

        except IndexError:
          print("Next Argument doesn't exist for this option", current_argument)
          continue

      if len(next_move_options) != 0:
        # print("Next move options", next_move_options)
        # print("Random choice type")
        current_argument = random.choice(next_move_options)

      else: active_game = False

    else:
      print("CPU ENDED")
      print("No more moves")
      active_game = False
      break


    print("CPU MOVES:", current_argument)
    game_path.append(current_argument)


    if game_path in listed:
      listed.remove(game_path)
      print(game_path, "Game path", "is in listed")
      print("Paths remaining", listed)

    cpu_moves.append(current_argument)

    move_count += 1
    player_move = True



  while player_move is True:


    print("\nPLAYER TURN:\n")

    next_move_options = []

    print("Current Move", current_argument)

    try:
      possible_moves = [x for x in listed if x[move_count] == current_argument and move_count < len(x)]


    except IndexError:
      # print("No more possible moves for player")
      active_game = False
      break

    print("Possible moves:", possible_moves)


    print("Game Path:", game_path,)


    # Go possible moves fist then elif for other options then else no more moves
    if len(possible_moves) > 0:

      for x in possible_moves:
        current_index = x.index(current_argument)
        try:
          next_move = x[current_index+1]
          if next_move not in next_move_options:
            next_move_options.append(next_move)
        except IndexError:
          print("Last Option for this one")
          continue

      print("Next move options", next_move_options)

      if len(next_move_options) != 0:
        while True:

            current_argument = input("Player, select your next move: ")

            if current_argument.lower() not in next_move_options:
                print("Not an appropriate choice.")
            else:
                game_path.append(current_argument)
                player_moves.append(current_argument)

                print("Player has chosen:", current_argument)
                player_move = False
                break
      else: 
        print("Next Move Break")


    else:
      print("All Moves:", alternative_path)
      print("No poss moves")
      active_game = False
      
    if game_path in listed:
      listed.remove(game_path)
      print(game_path, "Game path", "is in listed")

    move_count +=1
    player_move = False


if len(game_path) % 2 == 0: print("\nCPU Wins the argument game!")
elif len(game_path) % 2 == 1: print("\nPLAYER Wins the argument game")

print("\nGame Path:", game_path)
print("Listed:", listed)
print("Player Path:", player_moves)
print("CPU Path:", cpu_moves)


'''
TODO Go over the rules and function to ensure logic makes sense

TODO Function that finds and saves the winning strategy
'''