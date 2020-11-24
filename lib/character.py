import random
from enum import Enum


class Job(Enum):
    WARRIOR = 1
    KNIGHT = 2
    MAGE = 3
    SAGE = 4

class RelPos(Enum):
    LEFT = 1
    RIGHT = 2
    ABOVE = 3
    BELOW = 4

class Character():

    def __init__(self, name, sym, ypos, xpos):
        self.name = name
        self.sym = sym
        self.ypos = ypos; self.init_ypos = ypos
        self.xpos = xpos; self.init_xpos = xpos
        self.turns_since_last_move = 0
        self.last_move = None
    
    def check_position_delta(self, posd, map_scheme):
        ypos = self.ypos + posd[0]; xpos = self.xpos + posd[1]
        if map_scheme[ypos][xpos] == " ":
            self.ypos += posd[0]; self.xpos += posd[1]

    def check_relative_pos(self, characters):
        for cname, char in characters.items():
            if cname != self.name:
                char_pos = (char.ypos, char.xpos)
                yd = self.ypos - char_pos[0]
                xd = self.xpos - char_pos[1]

                if (yd == 0 and xd in [-1, 1]) or (xd == 0 and yd in [-1, 1]):
                    if yd == 0:
                        if xd == -1: plyr_pos = RelPos.LEFT
                        else: plyr_pos = RelPos.RIGHT
                    else:
                        if yd == -1: plyr_pos = RelPos.ABOVE
                        else: plyr_pos = RelPos.BELOW
                    return char, plyr_pos
        return None, None

class Player(Character):

    def __init__(self, job, **kwargs):
        self.job = job
        self.set_stats()
        super(Player, self).__init__(**kwargs)
    
    def set_stats(self):
        if self.job == Job.WARRIOR:
            self.hp = 10
            self.attack = 9; self.defense = 7
            self.magic = 3;  self.magic_defense = 4
        elif self.job == Job.KNIGHT:
            self.hp = 10
            self.attack = 7; self.defense = 9
            self.magic = 3;  self.magic_defense = 5
        elif self.job == Job.MAGE:
            self.hp = 7
            self.attack = 5; self.defense = 4
            self.magic = 9;  self.magic_defense = 7
        elif self.job == Job.SAGE:
            self.hp = 7
            self.attack = 5; self.defense = 6
            self.magic = 7;  self.magic_defense = 9

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
            self.check_position_delta((yd, xd), map_scheme)
        else: self.turns_since_last_move += 1

    def follow_series(self, map_scheme):
        if self.mvnt_series_index == len(self.mvnt_series) - 1:
            self.mvnt_series_index = -1

        if self.turns_since_last_move == 1:
            self.mvnt_series_index += 1
            yd, xd = self.mvnt_series[self.mvnt_series_index]
            self.check_position_delta(self.mvnt_series[self.mvnt_series_index], map_scheme)
            self.turns_since_last_move = 0
        else: self.turns_since_last_move += 1

    def temp_mvnt(self, map_scheme):
        pass

class Enemy(NPC):
    def __init__(self, **kwargs):
        super(Enemy, self).__init__(**kwargs)
