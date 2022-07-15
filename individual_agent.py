import sys
import string
import random


# get the object from the object name
def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


class Agent:
  def __init__(self, name):
    self.name = name

    # 0,1,2 in,out,undec
    self.state = "Out"
    self.attacking = []
    self.attacked_by = []

  def myfunc(agent):
    print("Hello my name is", agent.name, "& my state is", agent.state)

  # Checks if argument is in or out
  def get_argument_state(agent):
    if len(agent.attacked_by) > 0:
      agent.state = "Out"
      return "Out"
    elif len(agent.attacked_by) == 0:
      return "In"
    else:
      return "Error"

  def argument_state(agent):
    for x in agent.attacked_by:
      print(str_to_class(x))

  def attack(agent, obj_name, victim):

    if hasattr(str_to_class(obj_name), "name"):

        agent.attacking.append(victim)

        print(agent.name, "is now hurling rocks at a", victim)

        victim_object = str_to_class(obj_name)
        victim_object.attacked_by.append(agent.name)  
    else:
        print("shit")


  def attack_agent(agent, victim):

        agent.attacking.append(victim)

        print(agent.name, "is now hurling rocks at", victim.name)

        victim.attacked_by.append(agent)  


def create_agent(agent_name):
  agent_object = Agent(agent_name)
  return agent_object


p1 = create_agent("Reece")
p2 = create_agent("Carly")

p2.attack("p1", p1.name)



# Makes List of Agents to create based on variable input by the user
def create_framework(variable):
  arguments_to_take = list(string.ascii_lowercase[:variable])
  agent_list = []

  for v in arguments_to_take:
    v = create_agent(v)
    agent_list.append(v)

  for names in agent_list:
    print(names.name)

    random_value = random.randint(0,9)
    random_threshhold = random.randint(0,9)
    arguments_excluding_value = [x for x in agent_list if x != names]

    # If the value is below the generated threshold, then the agent will attack a random agent
    if random_value < random_threshhold:
      victim = random.choice(arguments_excluding_value)
      print(str(names.name), "Attacks", victim.name)
      names.attack_agent(victim)
      # Checks and gives 30% odds of the argument choosing to attack yet another argument
      if random.randint(0,9) < 3:
        arguments_excluding_value = [x for x in arguments_excluding_value if x != victim]
        otherVictim = random.choice(arguments_excluding_value)
        names.attack_agent(otherVictim)
    else:
      print(names.name, "Leaves", random.choice(arguments_excluding_value).name)


    print(names.attacking)
    print(names.attacked_by)

  return agent_list

# Initialises Framework with variable of arguments set by user
list_of_objects = create_framework(20)

def grounded_initial_labellings(framework):
  for v in framework:
    if len(v.attacked_by) == 0:
      v.state = "In"
    for x in v.attacked_by:
      print(v.name, 'is attacked by', x.name)

    print(v.name, "Current state is ", v.state)


  for v in framework:
    for x in v.attacked_by:
      # TODO find out if Out is called if it's being attacked by one or more arguments, for now it's coded on the assumption it means one attacker
      if x.state == "In" and len(v.attacked_by) == 1 :
        v.state == "Out"
        print(v.name, "Changed to", v.state)

  return framework


grounded_framework = grounded_initial_labellings(list_of_objects)

# TODO Make a class possibly for the two users (Pro & Opp)

'''
TODO Grounded Rules
IN For all unattacked arguments
OUT to any argument that is attacked and just made IN
IN to all who are attacked by only OUTS
ANY Remaining arguments are deemed UNDEC

TODO Game tree function that constructs the gametree for all possible outcomes from playing that game
The OPP can reference the gametree to decide its next move

TODO Function that finds and saves the winning strategy

'''
