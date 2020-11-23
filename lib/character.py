import random


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

    def check_relative_pos(self, characters):
        #plyr_pos = (characters["plyr"].ypos, characters["plyr"].xpos)
        for cname, char in characters.items():
            #if cname != "plyr":
            if cname != self.name:
                char_pos = (char.ypos, char.xpos)
                #yd = plyr_pos[0] - char_pos[0]
                #xd = plyr_pos[1] - char_pos[1]
                yd = self.ypos - char_pos[0]
                xd = self.xpos - char_pos[1]

                if (yd == 0 and xd in [-1, 1]) or (xd == 0 and yd in [-1, 1]):
                    return char


class Player(Character):

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)

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
