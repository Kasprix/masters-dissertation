import sys

# get the object from the object name
def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


states = ["In", "Out", "Undecided"]


class Agent:
  def __init__(self, name, state):
    self.name = name

    # 0,1,2 in,out,undec
    self.state = states[state]
    self.attacking = []
    self.attacked_by = []

  def myfunc(agent):
    print("Hello my name is", agent.name, "& my state is", agent.state)

  # Checks if argument is in or out
  def get_argument_state(agent):
    if len(agent.attacked_by) > 0:
      return "Out"
    elif len(agent.attacked_by) == 0:
      return "In"
    else:
      return "Error"

  def attack(agent, obj_name, victim):

    if hasattr(str_to_class(obj_name), "name"):


        agent.attacking.append(victim)

        print(agent.name, "is now hurling rocks at a", victim)

        victim_object = str_to_class(obj_name)
        victim_object.attacked_by.append(agent.name)  
    else:
        print("shit")

def create_agent(agent_name, state):
  agent_object = Agent(agent_name, state)
  return agent_object


p1 = create_agent("Reece", 0)
p1.myfunc()


p2 = create_agent("Carly", 0)
p2.myfunc()
p2.attack("p1", p1.name)

print("\nAttacking:")
print(p1.attacking)
print(p2.attacking)

print("\nAttacked By:")
print(p1.attacked_by)
print(p2.attacked_by)
