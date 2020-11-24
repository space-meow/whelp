import json
import glob
from lib.key_map import *
from lib.character import (Job, NPC, Enemy)


class Map():

    def __init__(self, name, scheme, plyr, npcs, enemies, scr_dim):
        self.name = name
        self.scheme = scheme
        self.plyr = plyr
        self.npcs = npcs
        self.enemies = enemies
        with open("maps/{}/config.json".format(self.name), "r") as _f: self.config = json.load(_f)
        self.scr_dim = scr_dim

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
            data = self.config["characters"]["NPC"][npc]
            npcs[data["name"]] = NPC(data["mvnt_pattern"], data["dialog"], name=data["name"], sym="?", ypos=pos[0], xpos=pos[1])

        for enemy, pos in self.enemies.items():
            data = self.config["characters"]["enemy"][enemy]
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
        
        maps[nmap] = Map(nmap, full_map, plyr_pos, npc_pos, enemy_pos, scr_dim)

    return maps

def run_start_scr(scr, *args):

    num_rows, num_cols = scr.getmaxyx()

    y_center = int(num_rows / 2)
    x_center = int(num_cols / 2)

    name_prompt = "What's your name? "
    confirm_prompt = "Press \"{}\" to confirm. ".format(CONFIRM)
    scr.addstr(y_center - 2, x_center - len(confirm_prompt), confirm_prompt)
    scr.addstr(y_center - 3, x_center - len(name_prompt), name_prompt)

    name = []
    while True:
        key = scr.getkey()
        if key != "1":
            scr.addstr(y_center - 3, x_center + len(name), key)
            name.append(key)
        else:
            break
    
    job_prompt = "Choose a class. Press \"{}\" to confirm.".format(CONFIRM)
    job = None
    arrow_y = y_center - 2
    while True:
        scr.clear()
        scr.addstr(y_center - 4, x_center - int(len(job_prompt) / 2), job_prompt)
        scr.addstr(y_center - 2, x_center, "WARRIOR")
        scr.addstr(y_center - 1, x_center, "KNIGHT")
        scr.addstr(y_center, x_center, "MAGE")
        scr.addstr(y_center + 1, x_center, "SAGE")
        scr.addstr(arrow_y, x_center - 2, ">")
        scr.refresh()
    
        key = scr.getkey()
        if key == DOWN:
            if arrow_y + 1 != y_center + 2:
                arrow_y += 1
        elif key == UP:
            if arrow_y - 1 != y_center - 3:
                arrow_y -= 1
        elif key == CONFIRM:
            if arrow_y == y_center - 2:
                job = Job.WARRIOR
            elif arrow_y == y_center - 1:
                job = Job.KNIGHT
            elif arrow_y == y_center:
                job = Job.MAGE
            elif arrow_y == y_center + 1:
                job = Job.SAGE
            break

    return "".join(name), job
