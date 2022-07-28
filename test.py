

prefered = False
grounded = True




def alternative_options(list_of_list_of_moves, game_path, path, grounded, prefered):

    # Inverse would work for the CPU

    if grounded:
        # Checks PLAYER or CPU path to remove duplicate options depending if prefered or grounded
        for x in path:
            for y in list_of_list_of_moves:
                if y.count(x) > 1:
                    list_of_list_of_moves.remove(y)

        # Removes the game path thats been used so far to show the possible future paths
        for x in game_path:
            for y in list_of_list_of_moves:
                if x in y:
                    y.remove(x)


    if prefered:
        # Removes the game path thats been used so far to show the possible future paths
        for x in game_path:
            for y in list_of_list_of_moves:
                if x in y:
                    y.remove(x)

    print(list_of_list_of_moves)

    return list_of_list_of_moves


'''
list_of_list_of_moves = [['b', 'd', 'i', 'k', 'a', 'j', 'i'],
['b', 'd', 'i', 'k', 'a', 'j', 'g'], 
['b', 'd', 'i', 'k', 'a', 's', 'h', 'n', 'g'], 
['b', 'd', 'i', 'k', 'a', 's', 'h', 'n', 'k'], 
['b', 'd', 'i', 'k', 'a', 's', 'h', 'r', 'j']]

game_path = ['b', 'd', 'i', 'k', 'a', 's']

player_path = ['i','k']

alternative_options(list_of_list_of_moves,game_path,player_path,grounded,prefered)

'''
    





