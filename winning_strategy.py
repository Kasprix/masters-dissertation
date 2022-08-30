import string
from framework_and_tree import create_game_tree
from save_load import load_frameowrk
import itertools


def remove_duplicates(list):
    # To remove duplicates
    all_opps_individuals = []   

    for l in list:
        if l not in all_opps_individuals:
            all_opps_individuals.append(l)

    return all_opps_individuals

def find_winning_strategy(pro_winning_paths, all_opp_moves):
    winning_strategies = []

    for x in pro_winning_paths:
        # Get all pro moves (even elements)
        player_moves = x[0::2]

        result =  all(elem in player_moves  for elem in all_opp_moves)

        if result:
            print("Match")
            winning_strategies.append(x)
        
    return winning_strategies

def scan_entire_framework(initial_argument, framework, semantic):

    listed = create_game_tree(framework, initial_argument, semantic)

    winning_paths = [x for x in listed if len(x) % 2 == 1]

    all_opp_args = []

    for x in listed:
        temp = x[1::2]
        all_opp_args.append(temp)


    all_opp_args = [j for i in all_opp_args for j in i]
    all_opp_args = remove_duplicates(all_opp_args)


    winners = find_winning_strategy(winning_paths, all_opp_args)

    if len(winners) > 0:
        print("Winner found")


    return winners


FRAMEWORK_NAME = "5"
SEMANTIC = 'p'
framework = load_frameowrk(FRAMEWORK_NAME)
letters_to_search = string.ascii_lowercase[:int(FRAMEWORK_NAME)]
checker = False

accrued_winners = []

for x in letters_to_search:
    scanner = scan_entire_framework(x, framework, SEMANTIC)
    accrued_winners.append(scanner)

    if len(scanner) > 0: checker = True

print(checker)
print(accrued_winners)


'''
print("Wiinning Paths:", winning_paths)
print("All Cpu Args", all_opp_args)
'''