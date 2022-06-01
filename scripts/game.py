# game.py

'''
Basic file that only stores the function used to decide if someone won.
The online version of the game makes much more use of this file. In this
version, it could have also been placed in player.py instead.

'''


#Check for victory conditions for a single player
#return: 0 - fail, 1 - victory
def check_win(map_arr, dim_x, dim_y):
    
    '''
    Another solution is to keep track of a number of remaining ship tiles
    and decrement them by 1 each time a ship hit is scored. This however
    adds even more arguments to already cumbersome functions. Therefore
    this approach is used, even if it has slighly more overhead.

    '''
    for i in range(dim_x):
        for j in range(dim_y):
            if map_arr[i][j] == 'S':
                return 0

    return 1
