import curses
from lib.key_map import *
from lib.map import (Map, load_maps, run_start_scr)
from lib.character import (Character, Player, NPC, Enemy)
from lib.screen_utils import (update_scr, show_dialog, show_menu)


key_mv = {LEFT: [0, -1],
          RIGHT: [0, 1],
          UP: [-1, 0],
          DOWN: [1, 0],
          SPACE: [0, 0]}


def main(scr, *args):
    curses.noecho(); curses.cbreak(); curses.curs_set(0)

    num_rows, num_cols = scr.getmaxyx()
    scr_dim = (num_rows, num_cols)

    maps = load_maps(scr_dim)
    start_map = maps["test"]

    for screen in start_map.config["screen_sequence"]:
        if screen == "START_SCREEN":
            plyr_name, plyr_job = run_start_scr(scr)

        else:
            start_map.display_map(scr)

            characters = {}

            ypos, xpos = start_map.plyr
            characters["plyr"] = Player(plyr_job, name=plyr_name, sym="@", ypos=ypos, xpos=xpos)
            plyr = characters["plyr"]
            characters.update(start_map.setup_npcs())

            update_scr(scr, characters, start_map)
            for i, char in enumerate(characters.keys()):
                scr.addstr(3+i, 3, "{} position: {}".format(characters[char].name, (characters[char].ypos, characters[char].xpos)))
            scr.refresh()
            while True:
                temp_displays = []
                debug_msg = []
                adjacent_char, plyr_pos = plyr.check_relative_pos(characters)
                key = scr.getkey()
                if key in key_mv.keys():
                    # Update player position
                    plyr.check_position_delta(key_mv[key], start_map.scheme)

                    # Update everyone else
                    start_map.update_npc_positions(characters)

                elif key == ACTION:
                    if adjacent_char:
                        debug_msg.append((1, 3, "{} dialog: \"{}\"; player position: {}".format(adjacent_char.name, adjacent_char.dialog, plyr_pos)))
                        temp_displays.append(show_dialog(scr, adjacent_char, plyr_pos))

                    else:
                        debug_msg.append((1, 3, "No adjacent character"))

                elif key == FIGHT:
                    if adjacent_char:
                        if type(adjacent_char) == Enemy:
                            debug_msg.append((1, 3, "Can fight; player position: {}".format(plyr_pos)))
                        else:
                            debug_msg.append((1, 3, "Can't fight; player position: {}".format(plyr_pos)))
                    else:
                        debug_msg.append((1, 3, "No adjacent character to fight"))
                
                elif key == MENU:
                    show_menu(scr)

                elif key == QUIT:
                    break

                debug_msg.append((2, 3, "Key pressed: {}".format(key)))
                update_scr(scr, characters, start_map, temp_displays, True, debug_msg)
    
    curses.echo(); curses.nocbreak(); curses.curs_set(1)
    return 


if __name__ == "__main__":
    curses.wrapper(main)
