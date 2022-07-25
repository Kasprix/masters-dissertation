import string

from argument_functions import prefered_initial_labellings
from framework_and_tree import create_framework, create_game_tree



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

print(listed)


for x in listed:
  if len(x) % 2 == 0: cpu_winning_tree.append(x)
  elif len(x) % 2 == 1: player_winning_tree.append(x) 

print("\nPLAYER WIN ROUTES: ", len(player_winning_tree) ,player_winning_tree)
print("CPU WIN ROUTES: ", len(cpu_winning_tree) , cpu_winning_tree)

move_count = 0
game_path = []
player_moves = []
cpu_moves = []
first_player_move = True

while(active_game):
  possible_moves = [x for x in listed if x[move_count] == starting_argument]
  game_path.append(starting_argument)
  print("Possible Moves", possible_moves)


  while first_player_move is True:
       # Your stuff here
    first_player_move = False

  while first_player_move is False:
    first_player_move = True
       # More of your stuff
  
  # Follows path the game takes
  #if move_count % 2 == 0:

  active_game = False


'''
TODO Go over the rules and function to ensure logic makes sense

TODO Game tree function that constructs the gametree for all possible outcomes from playing that game
The OPP can reference the gametree to decide its next move

TODO Function that finds and saves the winning strategy
'''