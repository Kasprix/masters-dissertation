from framework_and_tree import create_game_tree


def play_game(framework, initial_argument, game_type):

    listed = create_game_tree(framework, initial_argument, game_type)

    print(listed)

    # --------------------BEGIN GAME----------------------


    move_count = 0
    game_path = []
    player_moves = []
    cpu_moves = []
    player_move = False
    current_argument = initial_argument
    active_game = True