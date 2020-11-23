import os
import glob
import json
import curses
import random

key_mv = {"KEY_LEFT": [0, -1],
          "KEY_RIGHT": [0, 1],
          "KEY_UP": [-1, 0],
          "KEY_DOWN": [1, 0],
          " ": [0, 0]}

class Map():

    def __init__(self, name, scheme, plyr, npcs, enemies):
        self.name = name
        self.scheme = scheme
        self.plyr = plyr
        self.npcs = npcs
        self.enemies = enemies
        with open("maps/{}/mvnt.json".format(self.name), "r") as _f: self.character_data = json.load(_f)

    def display_map(self, scr):
        for i, row in enumerate(self.scheme):
            for j, cell in enumerate(row):
                scr.addstr(i, j, cell)

    def update_npc_positions(self, characters):
        for cname, char in characters.items():
            if cname != "plyr":
                char.mvnt(self.scheme)
    
    def setup_npcs(self):
        npcs = {}
        for npc, pos in self.npcs.items():
            data = self.character_data["NPC"][npc]
            npcs[data["name"]] = NPC(data["mvnt_pattern"], data["dialog"], name=data["name"], sym="?", ypos=pos[0], xpos=pos[1])

        for enemy, pos in self.enemies.items():
            data = self.character_data["enemy"][enemy]
            npcs[data["name"]] = Enemy(mvnt=data["mvnt_pattern"], dialog=data["dialog"], name=data["name"], sym="&", ypos=pos[0], xpos=pos[1])
        return npcs

class Character():

    def __init__(self, name, sym, ypos, xpos):
        self.name = name
        self.sym = sym
        self.ypos = ypos; self.init_ypos = ypos
        self.xpos = xpos; self.init_xpos = xpos
        self.turns_since_last_move = 0
        self.last_move = None
    
    def check_position_delta(self, yd, xd, map_scheme):
        ypos = self.ypos + yd; xpos = self.xpos + xd
        if map_scheme[ypos][xpos] == " ":
            self.ypos += yd; self.xpos += xd
    


class NPC(Character):

    def __init__(self, mvnt, dialog, **kwargs):
        self.mvnt = {"RANDOM": self.random,
                     "SQUARE": self.follow_series,
                     "BACK_&_FORTH": self.follow_series}[mvnt]
        self.mvnt_series = {"RANDOM": [],
                            "SQUARE": [(0, 1),  (0, 1),
                                       (1, 0),  (1, 0),
                                       (0, -1), (0, -1),
                                       (-1, 0), (-1, 0)],
                            "BACK_&_FORTH": [(0, 1), (0, 1), (0, 1),
                                             (0, -1), (0, -1), (0, -1)]}[mvnt]
        self.mvnt_series_index = -1
        self.dialog = dialog
        super(NPC, self).__init__(**kwargs)
    

    # Movement patterns
    def random(self, map_scheme):
        if self.turns_since_last_move == 1:
            yd = random.randint(-1, 1)
            xd = random.randint(-1, 1)
            self.turns_since_last_move = 0
            self.check_position_delta(yd, xd, map_scheme)
        else: self.turns_since_last_move += 1

    def follow_series(self, map_scheme):
        if self.mvnt_series_index == len(self.mvnt_series) - 1:
            self.mvnt_series_index = -1

        if self.turns_since_last_move == 1:
            self.mvnt_series_index += 1
            yd, xd = self.mvnt_series[self.mvnt_series_index]
            self.check_position_delta(yd, xd, map_scheme)
            self.turns_since_last_move = 0
        else: self.turns_since_last_move += 1

    def temp_mvnt(self, map_scheme):
        pass

class Enemy(NPC):
    def __init__(self, **kwargs):
        super(Enemy, self).__init__(**kwargs)


def load_maps(scr_dim):
    maps = {}
    for map_dir in glob.glob("maps/*"):
        nmap = map_dir.split("/")[-1]

        load_map = []
        with open(map_dir + "/" + "map", "r") as _f:
            for line in _f:
                load_map.append(list(line.strip("\n")))
        
        npc_pos = {}; enemy_pos = {}
        full_map = []
        num_rows = len(load_map); num_cols = len(load_map[0])
        y_pad = int((scr_dim[0] - num_rows) / 2)
        x_pad = int((scr_dim[1] - num_cols) / 2)
        blank_row = [" " for i in range(scr_dim[1]-1)]
        row_pad = [" " for i in range(x_pad)]
        for i in range(y_pad): full_map.append(blank_row)
        for row in load_map:
            full_row = row_pad + row + row_pad
            final_row = []
            for i, cell in enumerate(full_row):
                if cell == "@":
                    plyr_pos = (len(full_map), i)
                    final_row.append(" ")
                elif cell in ["1", "2", "3", "4", "5"]:
                    npc_pos[cell] = (len(full_map), i)
                    final_row.append(" ")
                elif cell.isalpha(): enemy_pos[cell] = (len(full_map), i)
                else: final_row.append(cell)
            full_map.append(final_row)
        for i in range(y_pad): full_map.append(blank_row)
        
        maps[nmap] = Map(nmap, full_map, plyr_pos, npc_pos, enemy_pos)

    return maps

def check_relative_pos(characters):
    plyr_pos = (characters["plyr"].ypos, characters["plyr"].xpos)
    for cname, char in characters.items():
        if cname != "plyr":
            char_pos = (char.ypos, char.xpos)
            yd = plyr_pos[0] - char_pos[0]
            xd = plyr_pos[1] - char_pos[1]

            if (yd == 0 and xd in [-1, 1]) or (xd == 0 and yd in [-1, 1]):
                return char

def update_scr(scr, characters, curr_map):
    scr.clear()
    curr_map.display_map(scr)
    for character, data in characters.items():
        scr.addstr(data.ypos, data.xpos, data.sym)
    scr.refresh()

def main(scr, *args):
    curses.noecho(); curses.cbreak(); curses.curs_set(0)

    num_rows, num_cols = scr.getmaxyx()
    scr_dim = (num_rows, num_cols)

    maps = load_maps(scr_dim)
    start_map = maps["test"]

    start_map.display_map(scr)

    characters = {}

    ypos, xpos = start_map.plyr
    characters["plyr"] = Character("player", "@", ypos, xpos)
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
            adjacent_char = check_relative_pos(characters)
            if adjacent_char:
                scr.addstr(1, 3, "\"{}\"".format(adjacent_char.dialog))
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

        
if __name__ == "__main__":
    curses.wrapper(main)