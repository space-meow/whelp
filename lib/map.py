import json
import glob
from lib.character import (NPC, Enemy)


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
