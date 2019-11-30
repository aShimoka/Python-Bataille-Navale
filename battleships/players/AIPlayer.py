#  Copyright © 2019 CAILLAUD Jean-Baptiste.
import random

import engine
from battleships.players.Player import Player


class AIPlayer(Player):
    def start_game(self):
        pass

    def start_turn(self):
        pass

    def end_turn(self):
        pass

    def request_shot(self):
        self.current_cell += 1
        self.fire(engine.math.Vector2(self.current_cell % 10, self.current_cell // 10))

    def request_hit(self, at: engine.math.Vector2):
        self.hit(at, self.SHOT_HIT_TYPE_GAME_OVER if at == self.ship_cell else self.SHOT_HIT_TYPE_MISS)

    def show_hit(self, at: engine.math.Vector2, hit_type: int):
        pass

    def await_opponent_shot(self):
        pass

    def __init__(self):
        super().__init__()
        self.current_cell = 0

        self.ship_cell = engine.math.Vector2(4, 4)
