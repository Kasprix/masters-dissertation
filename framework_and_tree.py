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
    # Excludes the current argument in question to prevent arguing against itself 
    arguments_excluding_value = [x for x in agent_list if x != names]


    # if value less than 8 then attack a random argument
    if random_value < 8:
      victim = random.choice(arguments_excluding_value)
      print(str(names.name), "Attacks", victim.name)
      names.attack_agent(victim)

      # Checks and gives 60% odds of the argument choosing to attack yet another argument
      if random.randint(0,9) < 6:
        arguments_excluding_value = [x for x in arguments_excluding_value if x != victim]
        otherVictim = random.choice(arguments_excluding_value)
        print(str(names.name), "Attacks", otherVictim.name)
        names.attack_agent(otherVictim)
    else:
      # No attacks are made
      print(names.name, "Leaves", random.choice(arguments_excluding_value).name)

  return agent_list

# Creates the game tree for the given argument that has been selected as the initial
def create_game_tree(framework, initial_argument, semantic):

  # Checks the semantic the game is to be played in, so it can create the correct possible paths
  if semantic == 'p':
    print("Prefered Game Type")
    prefered = True
  elif semantic =='g':
    print("Grounded Game Type")
    grounded = True


  # Stores the incremental new arguments that are found
  new_argument = []
  list_of_lists = []
  attack_list = []
  new_list = []

  # Gathers all the pairs of attacks and if attacked by none then returns a "" pair
  for x in framework:
    if len(x.attacked_by) == 0:
      attack_list.append([x.name])
    else:
      for y in x.attacked_by:
        attack_list.append([x.name, y.name])
        print (x.name, "is attacked by", y.name)
  print("\n", attack_list, "\n")

  # Matches are the pairs in attack list that have the same first value as initial argument
  # E.g. if a is initial argument and there was a pair [a,b] it would extract that pair and remove from the attack list so it can't be used again
  matches = [x for x in attack_list if x[0] == initial_argument and len(x) > 1]

  # Print all matches that start with initial argument
  print("Matches:", matches, "\n")


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

        # All argument pairs that start with selected argument
        matches = [y for y in attack_list if y[0] == x and len(y) > 1]
        
        # Temp comment to allow for using same argument multiple times
        # attack_list = [x for x in attack_list if x not in matches]

        if not matches:
          print("Skipped, no match")
          print("List of lists:", list_of_lists)
          count += 1
        else:

          # List of new pairs
          listy = []

          # Print all matches that start with initial argument
          print("Matches:", matches, "\n")

          '''
          for match in matches:
            print("Individual match", match)
          '''

          # Searches list of lists for arguments that attack x (If x is first in pair it means it is attacked by the second value ['a'],['b'] == A is attacked by B)    
          
          advance_path = [g for g in list_of_lists if g[-1] == x]

          if len(advance_path) > 0:
            print("ADV PATH", advance_path) 
            print("TEST SEARCH:", advance_path[0])

            for i in range(len(matches)):

              # print("Test", value)
              print("Before", advance_path[0])
              advance_path[0].insert(len(advance_path[0]), matches[i][1])
              print("After", advance_path[0])


              # Looks at value to see if it would be valid under the selected semantics
              # odd values, player moves. even values, CPU moves
              if grounded:
                valid_move = True
                list_odd = advance_path[0][::2] # Elements from list1 starting from 0 iterating by 2
                for x in list_odd:
                  if list_odd.count(x) > 1:
                    valid_move = False
                    break

                if valid_move:
                  # print("Checker", advance_path[0])
                  print("Before 1", listy)
                  # Adds to new list before popping entry
                  listy.append(advance_path[0].copy())
                  print("After 1", listy)

                  # Removes the new entry to allow for the next entry to enter
                  advance_path[0].pop()

                  if matches[i][1] != '':
                    new_argues.append(matches[i][1])
                  
                else: 
                  advance_path[0].pop()
                  print("Incorrect path found")
                  next

                
              
              elif prefered:
                valid_move = True
                list_odd = advance_path[0][1::2] # Elements from list1 starting from 0 iterating by 2
                for x in list_odd:
                  if list_odd.count(x) > 1:
                    valid_move = False
                    break
                  
                if valid_move:
                  # print("Checker", advance_path[0])
                  print("Before 1", listy)
                  listy.append(advance_path[0].copy())
                  print("After 1", listy)

                  # Removes the new entry to allow for the next entry to enter
                  advance_path[0].pop()
                  
                  if matches[i][1] != '':
                    new_argues.append(matches[i][1])
                else: 
                  advance_path[0].pop()
                  print("Incorrect path found")
                  next



            pruned = [h for h in listy if h[-2] == x]
          
          print("Pruned", pruned)

          if len(listy) > 0:
            list_of_lists = list_of_lists + listy
            list_of_lists.remove(advance_path[0])
          print("List of lists:", list_of_lists)

          count += 1

        new_argument = [x for x in new_argues if x != '']
      round_count += 1

      print("NEXT ROUND OF ARGUES", new_argument)
      print("Remaining Arguments:", attack_list)
      print("Current Tree:", list_of_lists)



# Removes '' at end of list
  for x in list_of_lists:
    if x[-1] == '':
      x.remove('')
  return list_of_lists