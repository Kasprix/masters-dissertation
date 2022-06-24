import sys

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


states = ["In", "Out", "Undecided"]


class Agent:
  def __init__(self, name):
    self.name = name
    self.state = states[0]
    self.attacking = []
    self.attacked = []

  def myfunc(agent):
    print("Hello my name is", agent.name, "& my state is", agent.state)

  def attack(agent, obj_name, victim):

    if hasattr(str_to_class(obj_name), "name"):


        agent.attacking.append(victim)

        print(agent.name, "is now hurling rocks at a", victim)

        victim_object = str_to_class(obj_name)
        victim_object.attacked.append(agent.name)
        
    else:
        print("shit")

p1 = Agent("Reece")
p1.myfunc()
p1.attack("p1", p1.name)


p2 = Agent("Carly")
p2.myfunc()
p2.attack("p1", p1.name)

print(p2.attacking)
print(p1.attacked)