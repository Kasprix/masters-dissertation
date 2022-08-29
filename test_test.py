import copy
from functools import reduce
import random
import string
import itertools
from operator import itemgetter


from argument_functions import prefered_initial_labellings
from framework_and_tree import create_framework, create_game_tree
from save_load import load_frameowrk


player_winning_tree = []
cpu_winning_tree = []


# FOR TESTING
grounded = False
prefered = True


# init game
active_game = True

starting_argument = 'b'

framework = load_frameowrk('5')

listed = create_game_tree(framework, starting_argument, "p")


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

    try:
      if grounded:
        possible_moves = []
        print(listed)
        for x in listed:
            if x[0:move_count+1] == game_path:
                possible_moves.append(x)

      if prefered:
        possible_moves = []
        print(listed)
        for x in listed:
            if x[0:move_count+1] == game_path and x[move_count+1] not in player_moves:
                possible_moves.append(x)

    except IndexError:
      print("CPU Moves indent break")
      break

    next_move_options = []

    print("Possible moves:", possible_moves)

    # List of winning strategies for the CPU
    prefered_cpu_options = [
        x for x in cpu_winning_tree if x[move_count] == current_argument and move_count < len(x)]

    if len(prefered_cpu_options) > 0:
      # print("Prefered choice")
      best_move = min(prefered_cpu_options, key=len)
      current_argument = best_move[move_count+1]
      cpu_moves.append(current_argument)
      move_count += 1

    elif len(possible_moves) > 0:
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
      break

    print("CPU MOVES:", current_argument)
    game_path.append(current_argument)

    if game_path in listed:
      print(game_path, "Game path", "is in listed")
      paths.append(game_path)
      listed.remove(game_path)

      # makes checking for alternatives on the list at point [0] for player as that's next move
      # move_count = 0

      # Does this to find next argument for player

      for i in reversed(copy.deepcopy(cpu_moves)):

        for list in listed:
          if i in list and len(list):
            index = list.index(i)
            if index % 2 == 1:
              current_argument = i
              move_count = index
              print("Found alternative at point", move_count,
                    "for argument:", current_argument)

              game_path = game_path[:move_count+1]
              break

    player_move = True

    print("New Path", game_path)





    

  while player_move is True:

    print("\nPLAYER TURN (Move Count):", move_count, "\n")

    next_move_options = []

    print("Current Move", current_argument)

    print("Move Count:", move_count)
    print("Current Argument", current_argument)

    try:
      if prefered:
        possible_moves = []
        print(listed)
        for x in listed:
            if x[0:move_count+1] == game_path:
                possible_moves.append(x)

      if grounded:
        possible_moves = []
        print(listed)
        for x in listed:
            if x[0:move_count+1] == game_path and x[move_count+1] not in player_moves:
                possible_moves.append(x)

    except IndexError:
      print("No more possible moves for player")
      active_game = False
      break

    print("Listed:", listed)
    print("Possible moves:", possible_moves)

    print("Game Path:", game_path)

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
                move_count += 1
                player_move = False
                break
      else:
        print("Next Move Break")
    else:
      print("No poss moves")
      active_game = False

    if game_path in listed:
      print(game_path, "Game path", "is in listed")
      print("Player Moves:", player_moves)
      paths.append(game_path)
      listed.remove(game_path)

      # Does this to find next argument for player
      first_arg_trunc = [i for i, j in zip(player_moves, game_path) if i == j]
      alt_moves_list = {}

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

      print("Selected Move:", current_argument)
      print("Selected Point:", move_count)
      print("Game Path", game_path)

      # makes checking for alternatives on the list at point [1] for CPU as that's next move, issue cause current argument isn't changed
      # Take opps args, find if there is argument next to it
      # move_count = 1

    print("All Paths:", paths)

    player_move = False


# if len(reduce(lambda count, l: count + len(l), paths, 0)) % 2 == 0: print("\nCPU Wins the argument game!")
# elif len(reduce(lambda count, l: count + len(l), paths, 0)) % 2 == 1: print("\nPLAYER Wins the argument game")

print("\nGame Path:", game_path)
print("Listed:", listed)
print("Player Path:", player_moves)
print("CPU Path:", cpu_moves)
print("All Paths:", paths)
