import copy
from functools import reduce
import random


from argument_functions import prefered_initial_labellings
from framework_and_tree import create_framework, create_game_tree


player_winning_tree = []
cpu_winning_tree = []
grounded = False
prefered = False

# init game
active_game = True


starting_argument = 'b'



# Ensures user picks valid option
while True:
    game_type = input("Prefered or Grounded game? (P/G): ")
    if game_type.lower() == "g":
      grounded = True
      break
    if game_type.lower() == "p":
      prefered = True
      break
    else: print("Not an appropriate choice.")


listed = create_game_tree(create_framework(7), starting_argument, game_type)

print(listed)


for x in listed:
  if len(x) % 2 == 0: cpu_winning_tree.append(x)
  elif len(x) % 2 == 1: player_winning_tree.append(x) 


print("\nPLAYER WIN ROUTES: ", len(player_winning_tree) ,player_winning_tree)
print("CPU WIN ROUTES: ", len(cpu_winning_tree) , cpu_winning_tree, "\n")


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

while(active_game):


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
      if prefered:
        possible_moves = [x for x in listed if x[move_count] == current_argument and move_count < len(x) and x[move_count+1] not in cpu_moves]
      if grounded:
        possible_moves = [x for x in listed if x[move_count] == current_argument and move_count < len(x)]


    except IndexError:
      print("CPU Moves indent break")
      break

    next_move_options = []    


    print("Possible moves:", possible_moves)


    # List of winning strategies for the CPU
    prefered_cpu_options = [x for x in cpu_winning_tree if x[move_count] == current_argument and move_count < len(x)]


    if len(prefered_cpu_options) > 0:
      # print("Prefered choice")
      best_move = min(prefered_cpu_options, key=len)
      current_argument = best_move[move_count+1]
      cpu_moves.append(current_argument)
      move_count += 1

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
        print("Random choice type")
        current_argument = random.choice(next_move_options)
        cpu_moves.append(current_argument)
        move_count += 1

      else: active_game = False

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
              print("Found alternative at point", move_count, "for argument:", current_argument)

              game_path = game_path[:move_count+1]
              break

    
    player_move = True



  while player_move is True:


    print("\nPLAYER TURN (Move Count):", move_count, "\n")

    next_move_options = []

    print("Current Move", current_argument)

    try:
      if prefered:
        possible_moves = [x for x in listed if x[move_count] == current_argument and move_count < len(x)]
      if grounded:
        possible_moves = [x for x in listed if x[move_count] == current_argument and move_count < len(x) and x[move_count+1] not in player_moves]


    except IndexError:
      print("No more possible moves for player")
      active_game = False
      break

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
                move_count +=1
                player_move = False
                break
      else: 
        print("Next Move Break")
    else:
      print("No poss moves")
      active_game = False

    if game_path in listed:
      print(game_path, "Game path", "is in listed")
      paths.append(game_path)
      listed.remove(game_path)

      game_path = []

      # Does this to find next argument for player
      first_arg_trunc = copy.deepcopy(player_moves)
      first_arg_trunc.remove(starting_argument)

      for i in reversed(first_arg_trunc):
        for list in listed:
          if i in list and len(list):
            index = list.index(i)
            if index % 2 == 0:
              current_argument = i
              move_count = index
              print("Found alternative at point", move_count, "for argument:", current_argument)
              game_path = game_path[:move_count+1]
              break


      # makes checking for alternatives on the list at point [1] for CPU as that's next move, issue cause current argument isn't changed
      # Take opps args, find if there is argument next to it
      # move_count = 1

    
    player_move = False


# if len(reduce(lambda count, l: count + len(l), paths, 0)) % 2 == 0: print("\nCPU Wins the argument game!")
# elif len(reduce(lambda count, l: count + len(l), paths, 0)) % 2 == 1: print("\nPLAYER Wins the argument game")

print("\nGame Path:", game_path)
print("Listed:", listed)
print("Player Path:", player_moves)
print("CPU Path:", cpu_moves)
print("All Paths:", paths)


'''
TODO Go over the rules and function to ensure logic makes sense

TODO Function that finds and saves the winning strategy
'''