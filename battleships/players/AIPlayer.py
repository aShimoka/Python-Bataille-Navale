#  Copyright © 2019
#  authored by Jean-Baptiste CAILLAUD et al.
#  contributor list on: https://github.com/yShimoka/python-bataille-navale

import random

import engine
from battleships import glvars
from battleships.objects.FleetModel import FleetModel
from battleships.players.Player import Player


class AIPlayer(Player):
    def __init__(self):
        super().__init__()

        self._ai_fleet = None

        self._destroy_center = None
        self._destroyer_segme_indxby_dir = dict()
        self._destroyer_active_dir = None

        self.last_hit_result = None
        self._ijcells_tried_s = set()
        self._rem_white_ijcells = list()

    # override
    @classmethod
    def is_human(cls):
        return False

    def start_game(self):
        # surprise ;)
        self._ai_fleet = FleetModel.generate_random_fleet()

        # compute "white" cells
        for cpt in range(10*10):
            i, j = cpt % 10, cpt // 10
            is_white = False
            if (j+1) % 2 != 0:  # odd line nb
                if (cpt+1) % 2 == 0:
                    is_white = True
            else:  # even line nb
                if (cpt+1) % 2 != 0:
                    is_white = True
            if is_white:
                self._rem_white_ijcells.insert(0, (i, j))

        # randomizing the AI strategy
        if not glvars.debug_mode:
            random.shuffle(self._rem_white_ijcells)

    def input_feedback(self, ijcell, result_code):
        self._ijcells_tried_s.add(ijcell)

        if self._destroy_center:
            if result_code == Player.SHOT_HIT_TYPE_HIT_AND_SUNK:
                self._destroy_center = None
                self._destroyer_segme_indxby_dir.clear()
                self._destroyer_active_dir = None

            elif result_code == Player.SHOT_HIT_TYPE_MISS:
                # backtrack & change dir
                k = self._destroyer_active_dir
                del self._destroyer_segme_indxby_dir[k]
                self._destroyer_active_dir = (k+1) % 4
            return

        if result_code == Player.SHOT_HIT_TYPE_HIT:
            self._destroy_center = ijcell

            # - list all candidates
            for m in (-1, 1):
                for n in range(1, 5):  # max boat len -1
                    cand = (ijcell[0], ijcell[1] + m * n)
                    direct = 1 if m > 0 else 3
                    if direct not in self._destroyer_segme_indxby_dir:
                        self._destroyer_segme_indxby_dir[direct] = list()
                    if (0 <= cand[0] < 10) and (0 <= cand[1] < 10):
                        self._destroyer_segme_indxby_dir[direct].append(cand)

            for m in (-1, 1):
                for n in range(1, 5):  # max boat len -1
                    cand = (ijcell[0] + m * n, ijcell[1])
                    direct = 0 if m > 0 else 2
                    if direct not in self._destroyer_segme_indxby_dir:
                        self._destroyer_segme_indxby_dir[direct] = list()
                    if (0 <= cand[0] < 10) and (0 <= cand[1] < 10):
                        self._destroyer_segme_indxby_dir[direct].append(cand)

            # pick a direction, at random
            self._destroyer_active_dir = random.randint(0, 3)

            if glvars.debug_mode:
                print('--destroyer activated--')
                print('center ' + str(self._destroy_center))
                print('segme  ' + str(self._destroyer_segme_indxby_dir))
                print('activ dir ' + str(self._destroyer_active_dir))

    def start_turn(self):
        pass

    def end_turn(self):
        pass

    def request_shot(self):
        if self._destroy_center:

            # - search
            chosen_c = None
            while chosen_c is None or chosen_c in self._ijcells_tried_s:
                li_cand = self._destroyer_segme_indxby_dir[self._destroyer_active_dir]

                # skip dead ends
                while len(li_cand) == 0:
                    del self._destroyer_segme_indxby_dir[self._destroyer_active_dir]
                    self._destroyer_active_dir = (self._destroyer_active_dir + 1) % 4
                    li_cand = self._destroyer_segme_indxby_dir[self._destroyer_active_dir]

                chosen_c = li_cand.pop(0)

        else:
            chosen_c = self._rem_white_ijcells.pop()
            while chosen_c in self._ijcells_tried_s:
                chosen_c = self._rem_white_ijcells.pop()

        self.fire(engine.math.Vector2(*chosen_c))

    def request_hit(self, at: engine.math.Vector2):
        touched_t = self._ai_fleet.collision_check(at, 1, 1)

        if touched_t is None:
            self.hit(at, self.SHOT_HIT_TYPE_MISS)  # notice game it did not hit
            return

        # Increment the damages on the boat.
        self._ai_fleet.damage(touched_t)

        if not self._ai_fleet.is_sunk(touched_t):  # hit, but not sunk
            self.hit(at, self.SHOT_HIT_TYPE_HIT)

        else:
            if self._ai_fleet.is_sunk():  # all ships just sunk
                self.hit(at, self.SHOT_HIT_TYPE_GAME_OVER)

            else:  # some ships remain
                self.hit(at, self.SHOT_HIT_TYPE_HIT_AND_SUNK)
        # self.hit(at, self.SHOT_HIT_TYPE_GAME_OVER if at == self.ship_cell else self.SHOT_HIT_TYPE_MISS)

    def show_hit(self, at: engine.math.Vector2, hit_type: int):
        pass

    def await_opponent_shot(self):
        pass
