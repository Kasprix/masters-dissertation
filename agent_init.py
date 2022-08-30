import sys

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

# Checks the arguments that attack a given agent
  def argument_state(agent):
    for x in agent.attacked_by:
      print(str_to_class(x))

# Sets up Realtionships between agents
  def attack_agent(agent, victim):

        agent.attacking.append(victim)
        victim.attacked_by.append(agent)  

# Creates the agent object by passing through the name (allows to incrementally create objects and name them from the alphabet)
def create_agent(agent_name):
  
  agent_object = Agent(agent_name)
  return agent_object
