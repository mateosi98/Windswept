import random
import time
import os

time_delay = 1.0
human_move = None
current_game = 10 * [0]
how_many_additional_bricks_in_each_level = 10 * [0]
how_many_destroyed_bricks_in_each_level = 10 * [0]
wind_level = 0

def clear_screen():
    os.system("clear")

def print_game():
    clear_screen()
    print("Here is how your tower looks now:")
    for i in range(9, -1, -1):
        print("{} {}".format(i, current_game[i] * 'o'))
    time.sleep(time_delay)

def print_game_with_new_bricks_shown():
    clear_screen()
    print("You have added some new bricks:")
    for i in range(9, -1, -1):
        print("{} {}".format(i, (current_game[i]
                                 - how_many_additional_bricks_in_each_level[i]) * 'o'
                                 + how_many_additional_bricks_in_each_level[i] * '+'))
    time.sleep(time_delay)

def print_game_with_wind_shown():
    global wind_level
    clear_screen()
    wind_level = random.randint(0, 9)
    print("The wind is blowing at level {}:".format(wind_level))
    for i in range(9, -1, -1):
        print("{} {} {}".format(i, current_game[i] * 'o', "~~~~~" if i == wind_level else ""))
    time.sleep(time_delay)

def print_game_with_wind_and_damage_shown():
    global how_many_destroyed_bricks_in_each_level
    clear_screen()
    print("The wind is doing some damage to your tower" if current_game[wind_level] > 0 else "The wind did not affect your tower")
    how_many_destroyed_bricks_in_each_level = 10 * [0]
    if current_game[wind_level] > 0:
        for i in range(10):
            if i >= wind_level and current_game[i] >= current_game[wind_level]:
                how_many_destroyed_bricks_in_each_level[i] = 1
    for i in range(9, -1, -1):
        print("{} {}".format(i, (current_game[i]
                                 - how_many_destroyed_bricks_in_each_level[i]) * 'o'
                                 + how_many_destroyed_bricks_in_each_level[i] * "-"))
        current_game[i] -= how_many_destroyed_bricks_in_each_level[i]
    time.sleep(time_delay)

def input_move():
    global how_many_additional_bricks_in_each_level
    how_many_bricks_to_add = random.randint(1, 3)
    print("enter {} number{}".format(how_many_bricks_to_add, "s with Enter after each" if how_many_bricks_to_add>1 else " and press Enter"))
    levels_where_bricks_added = []
    for i in range(how_many_bricks_to_add):
        levels_where_bricks_added.append(int(input("number {}: ".format(i+1))))
    how_many_additional_bricks_in_each_level = 10 * [0]
    for i in range(how_many_bricks_to_add):
        current_game[levels_where_bricks_added[i]] += 1
        how_many_additional_bricks_in_each_level[levels_where_bricks_added[i]] += 1

for i in range(100):
    print_game()
    input_move()
    print_game_with_new_bricks_shown()
    print_game()
    # add condition here: if the sky reached, stop
    if current_game[9] > 0:
        break
    print_game_with_wind_shown()
    print_game_with_wind_and_damage_shown()
print("You have completed your tower in {} moves".format(i))
input("Press Enter to close the game")
