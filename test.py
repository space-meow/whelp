import curses
from lib.map import (Map, load_maps)
from lib.character import (Character, Player, NPC, Enemy)
from lib.screen_utils import (update_scr)


key_mv = {"KEY_LEFT": [0, -1],
          "KEY_RIGHT": [0, 1],
          "KEY_UP": [-1, 0],
          "KEY_DOWN": [1, 0],
          " ": [0, 0]}


def main(scr, *args):
    curses.noecho(); curses.cbreak(); curses.curs_set(0)

    num_rows, num_cols = scr.getmaxyx()
    scr_dim = (num_rows, num_cols)

    maps = load_maps(scr_dim)
    start_map = maps["test"]

    start_map.display_map(scr)

    characters = {}

    ypos, xpos = start_map.plyr
    characters["plyr"] = Player(name="player", sym="@", ypos=ypos, xpos=xpos)
    plyr = characters["plyr"]
    characters.update(start_map.setup_npcs())

    update_scr(scr, characters, start_map)
    for i, char in enumerate(characters.keys()):
        scr.addstr(3+i, 3, "{} position: {}".format(characters[char].name, (characters[char].ypos, characters[char].xpos)))
    scr.refresh()
    while True:
        key = scr.getkey()
        if key in key_mv.keys():
            # Update player position
            yd, xd = key_mv[key]
            plyr.check_position_delta(yd, xd, start_map.scheme)

            # Update everyone else
            start_map.update_npc_positions(characters)

            update_scr(scr, characters, start_map)

        elif key == "e":
            adjacent_char = plyr.check_relative_pos(characters)
            if adjacent_char:
                scr.addstr(1, 3, "{} dialog: \"{}\"".format(adjacent_char.name, adjacent_char.dialog))
            else:
                scr.addstr(1, 3, "No adjacent character")

        elif key == "q":
            break

        for i, char in enumerate(characters.keys()):
            scr.addstr(3+i, 3, "{} position: {}".format(characters[char].name, (characters[char].ypos, characters[char].xpos)))
        scr.addstr(2, 3, "                        ")
        scr.addstr(2, 3, "Key pressed: {}".format(key))
        scr.refresh()
    
    curses.echo(); curses.nocbreak(); curses.curs_set(1)
    return 


def run_start_scr(scr, *args):
    curses.noecho(); curses.cbreak(); curses.curs_set(0); scr.keypad(1)

    num_rows, num_cols = scr.getmaxyx()

    y_center = int(num_rows / 2)
    x_center = int(num_cols / 2)

    name_prompt = "What's your name? "
    scr.addstr(y_center - 3, x_center - len(name_prompt), name_prompt)

    name = []
    while True:
        ch = scr.getkey()
        if ch != "1":
            scr.addstr(y_center - 3, x_center + len(name), ch)
            name.append(ch)
        else:
            break


    curses.echo(); curses.nocbreak(); curses.curs_set(1)
    return 

        
if __name__ == "__main__":
    curses.wrapper(run_start_scr)
    #curses.wrapper(main)