import random
import string

from agent_init import create_agent

# Makes List of Agents to create based on variable input by the user
def create_framework(variable):
  # list of alphabet that ends at the char number passed through the def
  arguments_to_take = list(string.ascii_lowercase[:variable])
  agent_list = []

  # Creates the agents and names them a letter
  for v in arguments_to_take:
    v = create_agent(v)
    agent_list.append(v)

  for names in agent_list:
    # First Random Value
    random_value = random.randint(0,9)
    # Second Random Value (Considering whether this is better than an arbitary number)
    random_threshhold = random.randint(0,9)
    # Excludes the current argument in question to prevent arguing against itself 
    arguments_excluding_value = [x for x in agent_list if x != names]

    # If the value is below the generated threshold, then the agent will attack a random agent
    # TODO rather than using random_threshold, allow user to enter the odds of attack to determine the game

    # if value less than 8 then attack a random argument
    if random_value < 8:
      victim = random.choice(arguments_excluding_value)
      print(str(names.name), "Attacks", victim.name)
      names.attack_agent(victim)

      # Checks and gives 60% odds of the argument choosing to attack yet another argument
      if random.randint(0,9) < 6:
        arguments_excluding_value = [x for x in arguments_excluding_value if x != victim]
        otherVictim = random.choice(arguments_excluding_value)
        names.attack_agent(otherVictim)
    else:
      # No attacks are made
      print(names.name, "Leaves", random.choice(arguments_excluding_value).name)

  return agent_list

# TODO Make a class possibly for the two users (Pro & Opp), have round system, even rounds PRO, odd rounds OPP

def create_game_tree(framework, initial_argument):

  # Stores the incremental new arguments that are found
  new_argument = []
  list_of_lists = []
  attack_list = []
  new_list = []

  # Gathers all the pairs of attacks and if attacked by none then returns a "" pair
  for x in framework:
    if len(x.attacked_by) == 0:
      attack_list.append([x.name, ""])
    else:
      for y in x.attacked_by:
        attack_list.append([x.name, y.name])
        print (x.name, "is attacked by", y.name)
  print(attack_list, "\n")

  # Matches are the pairs in attack list that have the same first value as initial argument
  # E.g. if a is initial argument and there was a pair [a,b] it would extract that pair and remove from the attack list so it can't be used again
  matches = [x for x in attack_list if x[0] == initial_argument]
  attack_list = [x for x in attack_list if x not in matches]

  # Print all matches that start with initial argument
  print("Matches:", matches, "\n")

  # print("New Attack List:", attack_list, "\n")

  # Adds first value to the search tree for the list of lists
  list_of_lists.append([initial_argument])

  for x in matches:
    # Appends second value in pair
    new_argument.append(x[1])

  print("New Arguments:", new_argument)

  # Takes the values from the new argument list, 
  for x in new_argument:
    add_new_arg = list_of_lists[0]
    new_list_item = add_new_arg + [x]
    new_list.append(new_list_item)

  # Updates new list
  list_of_lists = new_list

  print("Updated List of Lists:", list_of_lists)

  # ------------------------------------------------------------------------

  round_count = 1
  while len(new_argument) != 0:

    new_argues = []
    count = 1

    print("\nROUND COUNT:", round_count)
    
    for x in new_argument:

      print("\nITERATION", count, "\n")
      print("Name", x)

      matches = [y for y in attack_list if y[0] == x]
      attack_list = [x for x in attack_list if x not in matches]

      if not matches:
        print("Skipped, no match")
        print("List of lists:", list_of_lists)
        count += 1
      else:

        listy = []

        # Print all matches that start with initial argument
        print("Matches:", matches, "\n")
        print("New Attack List:", attack_list, "\n")

        for match in matches:
          print("Individual match", match)
      
        test_search = [g for g in list_of_lists if g[-1] == x]

        value = test_search.copy()

        first_val = value[0]

        for i in range(len(matches)):
          listy.append(value[0])
          new_argues.append(matches[i][1])

        for i in range(len(matches)):
          # print("Test", value)
          temp_list = value
          temp_list[0].insert(len(first_val), matches[i][1])
          # print("Checker", temp_list[0])
          listy.append(temp_list[0].copy())
          # Removes the new entry to allow for the next entry to enter
          temp_list[0].pop()

        pruned = [h for h in listy if h[-2] == x]
        
        print("Pruned", pruned)
        list_of_lists = list_of_lists + pruned
        list_of_lists.remove(test_search[0])
        print("List of lists:", list_of_lists)

        count += 1

      new_argument = new_argues
    round_count += 1

    print("NEXT ROUND OF ARGUES", new_argument)
    print("Remaining Arguments:", attack_list)

# Removes '' at end of list
  for x in list_of_lists:
    if x[-1] == '':
      x.remove('')
  return list_of_lists
