# player.py
import random
import copy

import map


#attack, but for bots.
def bot_attack(map_arr, dim_x, dim_y):
    
    while True:
        tgt_x = random.randint(0, dim_x-1)
        tgt_y = random.randint(0, dim_y-1)
        ret = map.map_place_attack(map_arr, tgt_x, tgt_y, dim_x, dim_y)
        if ret != 1:
            break

    return tgt_x, tgt_y, ret


#place enemy ships on the enemy map.
def bot_map_populate(map_arr, ship_template, dim_x, dim_y):
    
    xpos = -1
    ypos = -1
    direction = 0 #-1 = south, 1 = west 
    place_success = -1

    for i in range(len(ship_template)):
        while True:
            #Try to place ship i randomly. Break on success 
            xpos = random.randint(0, dim_x-1)
            ypos = random.randint(0, dim_y-1)
            direction = random.randint(0, 1)
            place_success = map.map_place_ship(map_arr, ship_template, i, direction,\
                                               xpos, ypos, dim_x, dim_y)
            if place_success == 0:
                break


#create player's map, empty.
def player_init(map_arr, ship_arr, ship_template, dim_x, dim_y):
    
    #Generate map and ship arrays for player
    dim_x, dim_y = map.map_generate(map_arr, dim_x, dim_y)
    ship_arr = copy.deepcopy(ship_template)

    return dim_x, dim_y 
