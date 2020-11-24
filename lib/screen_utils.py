from lib.key_map import *
from lib.character import (RelPos)


def update_scr(scr, characters, curr_map, temp_displays=[], print_debug=True, debug_msg=[]):
    scr.clear()
    curr_map.display_map(scr)
    for character, data in characters.items():
        scr.addstr(data.ypos, data.xpos, data.sym)

    for disp in temp_displays:
        scr.addstr(disp[0], disp[1], disp[2])
    
    if print_debug:
        update_debug_console(scr, characters, debug_msg)

    plyr = characters["plyr"]
    scr.addstr(curr_map.scr_dim[0] - 6, 5, "Name: {}".format(plyr.name))
    scr.addstr(curr_map.scr_dim[0] - 5, 5, "HP: {}".format(plyr.hp))
    scr.addstr(curr_map.scr_dim[0] - 4, 5, "Attack: {}\tDefense: {}".format(plyr.attack, plyr.defense))
    scr.addstr(curr_map.scr_dim[0] - 3, 5, "Magic: {}\tMagic Defense: {}".format(plyr.magic, plyr.magic_defense))

    scr.refresh()

def update_debug_console(scr, characters, debug_msg):
    for i, char in enumerate(characters.keys()):
        scr.addstr(3+i, 3, "{} position: {}".format(characters[char].name, (characters[char].ypos, characters[char].xpos)))
    for msg in debug_msg:
        scr.addstr(msg[0], msg[1], msg[2])

def show_dialog(scr, adjacent_char, plyr_pos, repl_dialog=None):
    if plyr_pos == RelPos.ABOVE: y_mod = 1
    else: y_mod = -1
    
    if repl_dialog: dialog = repl_dialog
    else: dialog = adjacent_char.dialog
    dialog_str = "{} says \"{}\"".format(adjacent_char.name, dialog)
    return (adjacent_char.ypos + y_mod, adjacent_char.xpos - int(len(dialog_str) / 4), dialog_str)

def show_menu(scr):
    num_rows, num_cols = scr.getmaxyx()
    arrow_y = 5
    while True:
        scr.clear()
        scr.addstr(5, 5, "WARRIOR")
        scr.addstr(6, 5, "KNIGHT")
        scr.addstr(7, 5, "MAGE")
        scr.addstr(8, 5, "SAGE")
        scr.addstr(arrow_y, 3, ">")
        scr.refresh()
        key = scr.getkey()

        if key == DOWN:
            arrow_y += 1
        elif key == UP:
            arrow_y -= 1
        elif key == QUIT:
            return
