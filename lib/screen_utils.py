def update_scr(scr, characters, curr_map):
    scr.clear()
    curr_map.display_map(scr)
    for character, data in characters.items():
        scr.addstr(data.ypos, data.xpos, data.sym)
    scr.refresh()
