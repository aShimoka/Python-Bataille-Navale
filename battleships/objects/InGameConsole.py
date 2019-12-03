#  Copyright © 2019
#  authored by Jean-Baptiste CAILLAUD et al.
#  contributor list on: https://github.com/yShimoka/python-bataille-navale

import engine
from engine.logic import Vector2


class InGameConsole(engine.GameObject):
    """
    Simple game object that groups all game state texts together.
    """

    MAX_MSG_LEN = 48  # max. nb of characters to be shown
    LINE_SPACING = 28  # px

    # Lists all the showable texts.
    TEXT_GAME_STARTING = 0x00
    TEXT_GAME_NEW_TURN = 0x10
    TEXT_GAME_REQ_FIRE = 0x20
    TEXT_GAME_DO_SHOOT = 0x30
    TEXT_GAME_REQ_HIT = 0x40
    TEXT_GAME_GET_HIT_MISS = 0x50
    TEXT_GAME_GET_HIT_HIT = 0x51
    TEXT_GAME_GET_HIT_SUNK = 0x52
    TEXT_GAME_SHOW_HIT_MISS = 0x60
    TEXT_GAME_SHOW_HIT_HIT = 0x61
    TEXT_GAME_SHOW_HIT_SUNK = 0x62
    TEXT_GAME_AWAIT_SHOT = 0x70
    TEXT_GAME_END_TURN = 0x80
    TEXT_GAME_END_GAME = 0x90

    _text_by_code = {
        TEXT_GAME_STARTING: "new game begins",
        TEXT_GAME_NEW_TURN: "new turn begins",

        TEXT_GAME_END_TURN: "turn ends",
        TEXT_GAME_END_GAME: "game over",

        TEXT_GAME_REQ_FIRE: "choose where to shoot",
        TEXT_GAME_AWAIT_SHOT: "enemy's playing",

        TEXT_GAME_DO_SHOOT: "fire!",
        TEXT_GAME_REQ_HIT: "enemy fires!",

        TEXT_GAME_SHOW_HIT_MISS: "- you miss -",
        TEXT_GAME_GET_HIT_MISS: "- enemy misses -",

        TEXT_GAME_SHOW_HIT_HIT: "* you hit a target *",
        TEXT_GAME_GET_HIT_HIT: "* enemy hits a target *",

        TEXT_GAME_GET_HIT_SUNK: "**~ your ship is going down ~**",
        TEXT_GAME_SHOW_HIT_SUNK: "**~ enemy ship is going down ~**"
    }

    _color_levels = {
        0: (255, 69, 0),
        1: (120, 120, 240),
        2: (45, 45, 90),
        3: (15, 15, 30),
    }
    CONTENTS_CAP = len(_color_levels)  # showing 4 texts at most

    def __init__(self, parent=None):
        super().__init__(parent)
        self._contents = list()

    def show_std_text(self, text_code):
        txt = self._text_by_code[text_code]
        self._console_print(txt)

    def show_custom_text(self, raw_txt):
        txt = raw_txt[:self.MAX_MSG_LEN]
        self._console_print(txt)

    def _console_print(self, txt):
        initcolor = self._color_levels[0]
        obj = engine.TextGameObject(self, "Futura", 26, txt, initcolor)
        obj.transform.offset = obj.size / -2  # centering text

        # adding to contents
        self._contents.insert(0, obj)
        if len(self._contents) > self.CONTENTS_CAP:  # remove one text when needed
            tmp = self._contents.pop()
            tmp.visible = False
            del tmp

        # updating color & position
        for k in range(len(self._contents)):
            c = self._color_levels[k]
            text_obj = self._contents[k]
            text_obj.set_color(c)

            y_offset = -k * self.LINE_SPACING
            text_obj.transform.position = Vector2(0, y_offset)
