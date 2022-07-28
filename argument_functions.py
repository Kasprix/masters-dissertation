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
