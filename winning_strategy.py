from framework_and_tree import create_game_tree
from save_load import load_frameowrk



def remove_duplicates(list):
    # To remove duplicates
    all_opps_individuals = []   

    for l in list:
        if l not in all_opps_individuals:
            all_opps_individuals.append(l)

    return all_opps_individuals

# Function to find the paths that provide the winning strategy for the player
def find_winning_strategy(framework):


    # Filters through all the pa
    winning_paths = [x for x in framework if len(x) % 2 == 1]

    all_opp_args = []
    
    # Finda all the opponents moves that are made through the game tree
    for x in winning_paths:
        temp = x[1::2]
        all_opp_args.append(temp)

    # All the opponents moves within the game tree
    all_opp_args = [j for i in all_opp_args for j in i]
    # Prevents repatition of arguments
    all_opp_args = remove_duplicates(all_opp_args)


    winning_strategies = []

    # If there's a path that responds to all the OPP moves made within the tree, this is the winning strategy the user can implement
    for x in winning_paths:
        # Get all opp moves (even elements)
        opp_moves = x[1::2]

        # Checks if all the opp moves are in the path, if so return true
        result =  all(elem in opp_moves  for elem in all_opp_args)

        # Add winning strategies to list to return from function
        if result:
            print("Match")
            print("Winning strategy path", x)
            print("All OPP Moves", all_opp_args)
            winning_strategies.append(x)
        
    return winning_strategies




FRAMEWORK_NAME = "5"
SEMANTIC = 'p'
initial_argument = 'b'
framework = load_frameowrk(FRAMEWORK_NAME)

listed = create_game_tree(framework, initial_argument, SEMANTIC)


winners = find_winning_strategy(listed)



