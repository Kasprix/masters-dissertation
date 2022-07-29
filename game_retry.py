import string
from framework_and_tree import create_framework, create_game_tree

while True:
    number_of_arguments = int(input("Select number of arguments to play with (Max 20):"))
    if number_of_arguments > 20:
      print("Not an appropriate choice.")
    else:
      break
        
# Initialises Framework with variable of arguments set by user
list_of_objects = create_framework(int(number_of_arguments))

print("---------------------------------------------")


options = list(string.ascii_lowercase[:int(number_of_arguments)])
print("Argument options to start with:", str(options), "\n")

print("---------------------------------------------")

# Ensures user picks valid option
while True:
    starting_argument = input("Input argument to play with: ")
    if starting_argument.lower() not in options:
        print("Not an appropriate choice.")
    else:
        break


listed = create_game_tree(list_of_objects, starting_argument)

print(listed)