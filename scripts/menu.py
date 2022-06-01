# menu.py

import sys

import map
import draw
import player
import game
import save


'''
All user interaction occurs here. Menues also handle program flow.

'''


'''
The get_sanitised_input() function handles almost every input required
by Battleships. The caller is only required to call the function once
to get completely a valid input. "extend_opt" argument causes the
function to validate complex input and pass it on to its relevant
function before returning. These 2 different types of input
have to be combined because users can choose to attack or do another,
simple function. Hence have to check for both at once.

options     = Every possible regular input of a menu, used by menues.

extend_opt = Integer index for the "attack" and "place" inputs. These 
are predefined inside the function.

              1 - "attack", 2 - "place" 

extend_opt 1 (attack): return -1 on ship miss, -2 on ship hit
extend_opt 2 (place):  return -1 on successful placement

'''
#returns: index of option, -1 on ship miss, -2 on ship hit
#                          -1 on ship placed successfully
def get_sanitised_input(options, extend_opt=0, map_arr=0, dim_x=0, dim_y=0,\
                        ship_template=0, ship=0, direction=0):

    while True:
        inp = ""
        #first check for regular options
        inp = str(input("> "))
        for i in range(len(options)):
            if inp.lower() == options[i]:
                return i
        if dim_x == 0 : #check if ingame input needs testing
            continue
        
        #now check for game options
        extend_opt_arr = ("NULL","attack", "place")
        tgt_x = -1
        tgt_y = -1
        ret = 0
        inp = inp.lower()
        inp = inp.split()
        if inp[0] == extend_opt_arr[extend_opt]:
            try:
                tgt_x = int(ord(inp[1])) - 97 #convert to ascii, then a = 0
                tgt_y = int(inp[2])
            except:
                continue

            if extend_opt == 1: #"attack"
                ret = map.map_place_attack(map_arr, tgt_y, tgt_x, dim_x, dim_y)
                if ret == 1:
                    continue
                else:
                    return ret
            if extend_opt == 2: #"place"
                ret = map.map_place_ship(map_arr, ship_template, ship, direction,\
                                         tgt_y, tgt_x, dim_x, dim_y)
                if ret == 1:
                    continue
                else:
                   return -1


#getting savefile input behaves differently, hence requiring own function.
def get_sanitised_file(do_read=False):
    
    print("Please enter a savefile name from the current directory,",\
          "or an absolute path to the savefile.")

    #Please don't chmod a-r ./* :)
    while True:
        inp = str(input("path > "))
        if do_read:
            try:
                file = open(inp, "r")
                file.close()
                return inp
            except:
                continue
        else:
            try:
                file = open(inp, "w")
                file.close()
                return inp
            except:
                continue


#getting map size input behaves differently, avoiding convolution
#of main input func.
def get_sanitised_map_size():
    
    dim_name = ('X', 'Y')
    dim = []

    print("Please enter the size of the map. Accepted range lies",\
          "between 9 and 12.")
    for i in range(2):
        while True:
            buf = "size " + dim_name[i] + " > "
            try:
                inp = int(input(buf))
                dim.append(inp)
                break
            except:
                continue

    return dim[1], dim[0]


#midgame menu
def game_menu(map_arr, enemy_map_arr, size_x, size_y):

    game_opts = ("map_ally", "map_enemy", "save", "menu", "quit")
    draw.print_game_menu()

    while True:
        inp = get_sanitised_input(options=game_opts, extend_opt=1,\
                                  map_arr=enemy_map_arr,\
                                  dim_x=size_x, dim_y=size_y)

        if inp == 0: #map_ally
            draw.print_map(map_arr, size_x, size_y, True)
            continue
        
        elif inp == 1: #map_enemy
            draw.print_map(enemy_map_arr, size_x, size_y, False)
            continue

        elif inp == 2: #save
            savefile = get_sanitised_file()
            save.save_game(map_arr, enemy_map_arr, size_x, size_y, savefile)
            print("Game saved to file: ", savefile)
            continue
        
        elif inp == 3: #menu
            draw.print_game_menu()
            continue
        
        elif inp == 4: #quit
            sys.exit("Exiting Battleships...")
            
        elif inp == -1: #ship miss
            print("Missed!")

        elif inp == -2: #ship hit
            print("Ship hit!")
            if game.check_win(enemy_map_arr, size_x, size_y):

                draw.print_map(map_arr, size_x, size_y, True)
                draw.print_map(enemy_map_arr, size_x, size_y, False)
                print("\nCongratulations! You win!")
                sys.exit("Exiting Battleships...")

        #Incase attack performed, do the bot's half
        bot_tgt_x, bot_tgt_y, bot_ret = player.bot_attack(map_arr, size_x, size_y)
        
        if bot_ret == -1:
            print("Enemy missed at: ", chr(ord('A')+bot_tgt_y), bot_tgt_x)

        elif bot_ret == -2:
            print("Enemy hit at: ", chr(ord('A')+bot_tgt_y), bot_tgt_x)
            if game.check_win(map_arr, size_x, size_y):
                
                draw.print_map(map_arr, size_x, size_y, True)
                draw.print_map(enemy_map_arr, size_x, size_y, False)
                print("\nAll of your ships are destroyed! You lose!")
                sys.exit("Exiting Battleships...")




#init game, alternative is to load.
def init_game_menu(map_arr, enemy_map_arr, ship_temp, ship_names_temp):
    
    size_x = -1
    size_y = -1

    init_opts = ("orientation", "list_ships", "menu", "map", "quit")
    direction = -1 #-1 = south, 1 = west
    direction_names = ("NULL", "west", "south")

    #draw initial empty maps
    draw.print_init_game_menu()
    size_x, size_y = get_sanitised_map_size()
    size_x, size_y = map.map_generate(map_arr, size_x, size_y)
    map.map_generate(enemy_map_arr, size_x, size_y)
    
    #place bot's ships
    player.bot_map_populate(enemy_map_arr, ship_temp, size_x, size_y)

    #place player's ships
    draw.print_init_game_menu_placeships()
    for i in range(len(ship_temp)):
        while True:
            print("Placing ship: ", ship_names_temp[i], " (",ship_temp[i],") "\
                  "Oriented: ", direction_names[direction]);
            inp = get_sanitised_input(options=init_opts, extend_opt=2,\
                                      map_arr=map_arr, dim_x=size_x,\
                                      dim_y=size_y, ship_template=ship_temp,\
                                      ship=i, direction=direction)

            if inp == 0: #orientation
                direction = direction * -1
                print("Changed orientation")
        
            elif inp == 1: #list_ships
                draw.print_init_game_ships(ship_names_temp, ship_temp, i)

            elif inp == 2: #menu
                draw.print_init_game_menu_placeships()

            elif inp == 3: #map
                draw.print_map(map_arr, size_x, size_y, True)

            elif inp == 4: #quit
                sys.exit("Exiting Battleships...")
        
            elif inp == -1: #ship placed
                break

    game_menu(map_arr, enemy_map_arr, size_x, size_y)


#main, starting menu.
def main_menu():
   
    #ships set here, makes future editing easy
    ship_template = [5, 4, 3, 3, 2, 2]
    ship_names_template = ["Aircraft Carrier", "Battleship", "Destroyer",\
                           "Cruiser", "Submarine", "Patrol Boat"]

    player_map_arr = []
    enemy_map_arr = []
    #sizes defined later

    draw.print_main_menu()

    options_tuple = ("play", "load", "help", "menu", "quit")
    
    while True:

        ret = get_sanitised_input(options_tuple)

        if ret == 0:
            init_game_menu(player_map_arr, enemy_map_arr, ship_template,\
                           ship_names_template)
        if ret == 1:
            savefile = get_sanitised_file(do_read=True)
            size_x, size_y = save.load_game(player_map_arr, enemy_map_arr, savefile)
            game_menu(player_map_arr, enemy_map_arr, size_x, size_y)
            
        if ret == 2:
            draw.print_main_menu(help=True)
        if ret == 3:
            draw.print_main_menu()
        if ret == 4:
            sys.exit("Exiting Battleships...")

main_menu()
