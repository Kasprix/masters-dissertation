import sys
import string
import random
import pickle


# get the object from the object name
def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)

# creates the argument agents
class Agent:
  def __init__(self, name):
    self.name = name

    self.state = "Not Declared"
    self.attacking = []
    self.attacked_by = []


  # TODO see if this will allow easier viewing of attacked agents
  def argument_state(agent):
    for x in agent.attacked_by:
      print(str_to_class(x))

  def attack_agent(agent, victim):

        agent.attacking.append(victim)
        victim.attacked_by.append(agent)  

# Creates the agent object by passing through the name (allows to incrementally create objects and name them from the alphabet)
def create_agent(agent_name):
  agent_object = Agent(agent_name)
  return agent_object

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

# Checks to see if argumement's state is considered legal via the constraints the labelling system applies to it.
def check_legal_state(label):
  # Assume legal until proven otherwise
  illegal = False

  if label.state == "In":
    for x in label.attacked_by: 
      # If there is is any argument attacking the argument then it can't be considered in
      if x.state != "Out": illegal == True
    if illegal == True: print(label.name, "is illegally IN")
    elif illegal == False: print(label.name, "is legally IN")
    else: next

  if label.state == "Out":
    # create list of argument states the current argument is being attacked by
    temp_state_list = []
    for x in label.attacked_by:
      temp_state_list.append(x)
    # if there isn't one instance of IN in the attacked by list, then the argument would be illegally OUT
    if "In" not in temp_state_list: illegal == True
    if illegal == True: print(label.name, "is illegally OUT")
    elif illegal == False: print(label.name, "is legally OUT")


  # If theres an IN state in attacked by, Undec is Illegal, if there isn't one of both OUT and UNDEC attacking the argument, then it is illegally UNDEC
  if label.state == "Undec":
    temp_out_list = []
    temp_undec_list = []
    for x in label.attacked_by: 
      # Checks if an IN attacks and counts the OUTS and UNDEC that Attack
      if x.state == "In": illegal == True
      if x.state == "Out": temp_out_list.append(x)
      if x.state == "Undec": temp_undec_list.append(x)
    # If illegal is still false and and an OUT and UNDEC is attacking 
    if illegal == False and not temp_out_list and not temp_undec_list: print(label.name, "is legally UNDEC")
    elif illegal == True: print(label.name, "is illegally UNDEC")
    else: 
      illegal ==  True
      print(label.name, "is illegally UNDEC")

  return illegal
  
def grounded_initial_labellings(framework):

  list_of_states = ["Some Things"]
  temp_list_of_states = ["Should be seperate"]
  # Finds all arguments attacked by nothing and declares their state as in 

  while list_of_states != temp_list_of_states:

    list_of_states.clear()
    for v in framework:
      list_of_states.append(v.state)

    for v in framework:
        if len(v.attacked_by) == 0:
            v.state = "In"
            for x in v.attacked_by:
                print(v.name, 'is attacked by', x.name)
                print(v.name, "Current state is ", v.state)

    # All arguments that are ONLY attacked by an argument who's state is declared in, are altered to state OUT
    for v in framework:
        for x in v.attacked_by:
        # TODO find out if Out is called if it's being attacked by one or more arguments, for now it's coded on the assumption it means one attacker
            if x.state == "In" and len(v.attacked_by) == 1 :
                v.state = "Out"
                print(v.name, "Changed to", v.state)

    # Now we change the state of all arguments who are only attacked by OUTs to IN
    for v in framework:
        all_attacks_are_out = True
        for x in v.attacked_by:
            if x.state != "Out":
                all_attacks_are_out = False
            else: next
            if all_attacks_are_out == True:
                v.state = "In"

    # Change remaining to UNDECIDED
    for v in framework:
        if v.state == "Not Declared":
          v.state = "Undec" 

    temp_list_of_states.clear()
    for v in framework:
      temp_list_of_states.append(v.state)

    # print("Updated List: ")
    # print(list_of_states)
    # print("\n", temp_list_of_states)
    # for v in framework: print("The state of", v.name, "is", v.state)


  print("Matched")

  return framework

def prefered_initial_labellings(framework):


  list_of_states = ["Some Things"]
  temp_list_of_states = ["Should be seperate"]


  # Finds all arguments attacked by nothing and declares their state as in 
  while list_of_states != temp_list_of_states:

    list_of_states.clear()
    temp_list_of_states.clear()

    for v in framework:
      list_of_states.append(v.state)

    # Finds all arguments and declares them in
    for v in framework:
      v.state = "In"

    
      
    # Now we change the state of all arguments who are only attacked by Ins to OUT
    for v in framework:
      all_attacks_are_out = True
      for x in v.attacked_by:
        if x.state == "In":
          all_attacks_are_out = False
        else: next
      if all_attacks_are_out == False:
        v.state = "Out"
      if len(v.attacked_by) == 0:
        v.state = "In"

    for v in framework:
      state_list = []
      for x in v.attacked_by:
        state_list.append(x.state)
      # Checks if argument is illegally Out and is being attacked and none of the attackers are In
      if "In" not in state_list and len(state_list) > 0 and v.state == "Out":
        v.state = "Undec"
        print(v.name, "is Fake News")
        print(v.name, "current state is:", v.state)
        print(state_list)

    # TODO Super Illegal IN and Illegal in, Super Illegal if attacked by legally IN 
    
    for v in framework:
      temp_list_of_states.append(v.state)

  legal_game = True
  for v in framework:
    if check_legal_state(v) == False: legal_game = False

  if legal_game == True: print("Legal to play")
  elif legal_game == False: print("Illegal you tithead")

  return framework

# Saves Pickles to the pickle folder
def save_framework(name, framework):
  with open("pickles/" + name + '.pickle', 'wb') as handle:
    pickle.dump(framework, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Loads Pickles to the argument game
def load_frameowrk(name): 
  with open("pickles/" + name + '.pickle', 'rb') as handle:
    b = pickle.load(handle)
  return b 


# TODO Make a class possibly for the two users (Pro & Opp), have round system, even rounds PRO, odd rounds OPP

# Gametree logic
def deploy_gametree(framework, selected_argument):
  for x in framework:
    starting_argument = None
    if x.name == selected_argument:
        print("\n\nNew Section")
        print("i found it!")
        starting_argument = x
        break
    
  return starting_argument


def search_tree(framework, starting_argument):

  list_of_pairs = []

  print("Beginning argument", starting_argument.name)

  if len(starting_argument.attacked_by) > 0:
    print("\nLayer 1: ")
    for x in starting_argument.attacked_by:
      print(starting_argument.name, "is attacked by", x.name)
      # Lists pairs together to then ensure repeats don't occur
      list_of_pairs.append([x.name, starting_argument.name])

      if len(x.attacked_by) > 0:

        print("\nLayer 2:")
        for y in x.attacked_by:

          if [y.name ,x.name] not in list_of_pairs:
            print(x.name, "is attacked by", y.name)
            list_of_pairs.append([y.name, x.name])
          else: print("Duplicate")

          if len(y.attacked_by) > 0:
            print("\nLayer 3:")
            for z in y.attacked_by:
              if [z.name ,y.name] not in list_of_pairs:
                print(y.name, "is attacked by", z.name)
                #print("Layer 3, selected argument:", z.name)
                list_of_pairs.append([z.name, y.name])
              else: break

              if len(z.attacked_by) > 0:
                print("\nLayer 4:")
                for a in z.attacked_by:
                  if [a.name ,z.name] not in list_of_pairs:
                    print(z.name, "is attacked by", a.name)
                    list_of_pairs.append([a.name, z.name])
                
                if len(a.attacked_by) > 0:
                  print("\nLayer 5:")
                  # print("Layer 4, selected argument:", a.name)
                  for b in a.attacked_by:
                    if [b.name ,a.name] not in list_of_pairs:
                      print(a.name, "is attacked by", b.name)
                      list_of_pairs.append([b.name, a.name])
                else: break
          else: print("Terminate")      
  else: print("Terminate")
  print(list_of_pairs)


def create_game_tree(framework, initial_argument):

  attack_list = []

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
  print("New Attack List:", attack_list, "\n")


  # Stores the incremental new arguments that are found
  new_argument = []
  list_of_lists = []

  # Adds first value to the search tree for the list of lists
  list_of_lists.append([initial_argument])

  for x in matches:
    # Appends second value in pair
    new_argument.append(x[1])

  print("New Arguments:", new_argument)

  new_list = []

  # Takes the values from the new argument list, 
  for x in new_argument:
    # If a blank value "", means nothing attaccks the argument so just leave the argument as last value in that specific list
    if x == "": 
      # Takes the values from the last iteration of list of lists and appends the new value (in this case there isnt one)
      next

      #add_new_arg = list_of_lists[0]
      #new_list.append(add_new_arg)

      # Takes the values from the last iteration of list of lists and appends the new value [x]
    else:
      add_new_arg = list_of_lists[0]
      new_list_item = add_new_arg + [x]
      new_list.append(new_list_item)

  # Updates new list
  list_of_lists = new_list

  print("Updated List of Lists:", list_of_lists)

  # ------------------------------------------------------------------------

  while len(new_argument) != 0:
    count = 1
    for x in new_argument:
      print("\nITERATION", count)
      print("Name", x)
      matches = [y for y in attack_list if y[0] == x]
      attack_list = [x for x in attack_list if x not in matches]

      # Print all matches that start with initial argument
      print("Matches:", matches, "\n")
      print("New Attack List:", attack_list, "\n")


      for match in matches:
        print("Individual match", match)
      count += 1

      test_search = [g for g in list_of_lists if g[-1] == x]

      replacement_appendment = []

      for i in range(len(matches)):
        tempy = []
        tempy.append(test_search[0])
        tempy[0].insert(len(test_search[0]), matches[i][1])
        print("Tempy:", tempy)

      print(replacement_appendment)

      

      test_search[0].insert(len(test_search[0]), matches[0][1])

      print("Test Search", test_search)

      print(list_of_lists)

      
      
      
        


    new_argument = []
  



'''
  while len(attack_list) > 0:
    next_search = [x for x in attack_list if x[0] == initial_argument]
    for x in next_search:
 '''     

'''
  for x in matches:
    layer2 = [y for y in attack_list if y[0] == x[1]]
    attack_list = [x for x in attack_list if x not in layer2]
    print("Layer 2:", layer2)
    print("Attack List:", attack_list)

  print("\n")

  for x in layer2:
    layer3 = [y for y in attack_list if y[0] == x[1]]
    attack_list = [x for x in attack_list if x not in layer3]
    print("Layer 3:", layer3)
    print("Attack List:", attack_list)
    if not layer3: break

  print("\n")

  
  for x in layer3:
    layer4 = [y for y in attack_list if y[0] == x[1]]
    attack_list = [x for x in attack_list if x not in layer4]
    print("Layer 4:", layer4)
    print("Attack List:", attack_list)
    if not layer4: break
'''
# Initialises Framework with variable of arguments set by user
list_of_objects = create_framework(6)
grounded_framework = prefered_initial_labellings(list_of_objects)
create_game_tree(grounded_framework, "a")



# search_tree(grounded_framework, bangbang)

'''
TODO Go over the rules and function to ensure logic makes sense

TODO Game tree function that constructs the gametree for all possible outcomes from playing that game
The OPP can reference the gametree to decide its next move

TODO Function that finds and saves the winning strategy
'''