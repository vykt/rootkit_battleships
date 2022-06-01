# save.py

import copy

#yes, this can be more concise but im tired
def save_game(map_arr, enemy_map_arr, dim_x, dim_y, savefile):
    file = open(savefile, "w") #already error checked
    file.write(str(dim_x))
    file.write("\n")
    file.write(str(dim_y))
    file.write("\n")
    
    for i in range(dim_x):
        for j in range(dim_y):
            file.write(map_arr[i][j])
            if j != dim_y - 1:
                file.write(",")
        file.write("\n")

    for i in range(dim_x):
        for j in range(dim_y):
            file.write(enemy_map_arr[i][j])
            if j != dim_y - 1:
                file.write(",")
        file.write("\n")
    file.close()
    

#doesn't error check savefiles. if you edit them you agree to the risk 
def load_game(map_arr, enemy_map_arr, savefile):

    file = open(savefile, "r") #already error checked
    dim_x = int(file.readline().replace('\n', ''))
    dim_y = int(file.readline().replace('\n', ''))

    for i in range(dim_x):
        buffer_arr = file.readline().replace('\n', '').split(',')
        map_arr.append(copy.deepcopy(buffer_arr))
    for i in range(dim_x):
        buffer_arr = file.readline().replace('\n', '').split(',')
        enemy_map_arr.append(copy.deepcopy(buffer_arr))
    file.close()

    return dim_x, dim_y
