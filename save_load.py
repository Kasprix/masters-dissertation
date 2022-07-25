import pickle

# Saves Pickles to the pickle folder
def save_framework(name, framework):
  with open("pickles/" + name + '.pickle', 'wb') as handle:
    pickle.dump(framework, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Loads Pickles to the argument game
def load_frameowrk(name): 
  with open("pickles/" + name + '.pickle', 'rb') as handle:
    b = pickle.load(handle)
  return b 
