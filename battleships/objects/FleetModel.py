#  Copyright © 2019
#  authored by Jean-Baptiste CAILLAUD et al.
#  contributor list on: https://github.com/yShimoka/python-bataille-navale

from copy import copy

from battleships import glvars
from engine.logic import Vector2


class FleetModel:
    """
    model for storing boat positions & handling computations
    """

    NB_BOAT_TYPES = 5
    BOAT_TYPES = range(0x2193, 0x2193 + NB_BOAT_TYPES)  # enumerating 5 symbols

    F_EAST, F_NORTH, F_WEST, F_SOUTH = range(1, 5)

    AIRCRAFT_CARRIER, BATTLESHIP, CRUISER, SUBMARINE, PATROLBOAT = BOAT_TYPES

    BOAT_LENGTHS = {
        AIRCRAFT_CARRIER: 5,
        BATTLESHIP: 4,
        CRUISER: 3,
        SUBMARINE: 3,
        PATROLBOAT: 2
    }

    def __init__(self):
        self._btype_to_origincell = dict()
        self._btype_to_direction = dict()

        self._btype_to_occupied_cells = dict()

        self._btype_to_hitpoints = copy(self.BOAT_LENGTHS)

    @classmethod
    def generate_dummy_fleet(cls, common_dir):
        obj = cls()
        next_ncell = 0

        # for each boat type...
        for btype in cls.BOAT_TYPES:
            # adujst next_ncell, then convert ncell:int to target_v2cell:Vector2
            i, j = next_ncell % 10, next_ncell // 10
            target_v2cell = Vector2(i, j)

            while not obj.can_add(btype, target_v2cell, common_dir):
                next_ncell += 1
                i, j = next_ncell % 10, next_ncell // 10
                target_v2cell = Vector2(i, j)

            # append the boat
            obj.add_boat(btype, target_v2cell, common_dir)

        return obj

    @classmethod
    def generate_random_fleet(cls):
        raise NotImplementedError()

    def has(self, boat_type):
        return boat_type in self._btype_to_origincell

    def is_full(self):
        return len(self._btype_to_origincell) == self.NB_BOAT_TYPES

    @classmethod
    def _asset_arg_validity(cls, bt, c):
        assert (bt in cls.BOAT_TYPES)
        assert ((-1 < c.x < 10) and (-1 < c.y < 10))

    @classmethod
    def _compute_occ_cells(cls, btype, origincell, boat_dir):
        boat_len = cls.BOAT_LENGTHS[btype]
        return cls.__get_covered_cells(origincell, boat_len, boat_dir)

    def add_boat(self, btype, cell: Vector2, direction: int):
        self._asset_arg_validity(btype, cell)
        self._btype_to_origincell[btype] = cell
        self._btype_to_direction[btype] = direction
        self._btype_to_occupied_cells[btype] = self._compute_occ_cells(btype, cell, direction)

        if glvars.debug_mode:
            print('origincell= '+str(self._btype_to_origincell))
            print('direction= '+str(self._btype_to_direction))
            print('occupiedcell= '+str(self._btype_to_occupied_cells))
            print(self)

    def update_boat(self, btype, new_cell: Vector2, new_dir=None):
        self._asset_arg_validity(btype, new_cell)

        self._btype_to_origincell[btype] = new_cell
        if new_dir is not None:
            self._btype_to_direction[btype] = new_dir

        del self._btype_to_occupied_cells[btype]
        self._btype_to_occupied_cells[btype] = self._compute_occ_cells(btype, new_cell, new_dir)

    def can_add(self, btype, cell: Vector2, direction):
        """
        Checks if the position is valid for the specified ship.
        :param btype: int, see the FleetModel class
        :param cell: The cell that is requested.
        :param direction: The direction of the ship.

        :return: True if the position is valid.
        """

        if not 0 <= cell.x < 10:
            return False
        if not 0 <= cell.y < 10:
            return False

        length = self.BOAT_LENGTHS[btype]

        if direction in (self.F_EAST, self.F_WEST):
            if cell.x + length > 10:
                return False
            return self.collision_check(cell, length, direction) is None

        if cell.y + length > 10:
            return False
        return self.collision_check(cell, length, direction) is None

    @classmethod
    def __get_covered_cells(cls, cell, length, direction):
        covered_cells = set()
        for i in range(length):
            if direction in (cls.F_NORTH, cls.F_SOUTH):
                covered_cells.add((i * 10) + (cell.x + cell.y * 10))
            else:
                covered_cells.add(i + (cell.x + cell.y * 10))

        return covered_cells

    def collision_check(self, cell, length, direction):
        # Compute all the cells covered by the ship/shot.
        covered_cells = FleetModel.__get_covered_cells(cell, length, direction)

        # Loop through all the ships.
        for btype in self.BOAT_TYPES:
            if btype not in self._btype_to_origincell:  # boat not in fleet
                continue

            intersect = self._btype_to_occupied_cells[btype] & covered_cells
            if len(intersect) > 0:
                return btype

    def damage(self, btype):
        assert(self._btype_to_hitpoints[btype] > 0)
        self._btype_to_hitpoints[btype] -= 1

    def is_sunk(self, btype=None):
        if btype is not None:
            return self._btype_to_hitpoints[btype] == 0

        # if btype is None, we're testing the whole fleet
        fleet_hp = sum(self._btype_to_hitpoints.values())
        return fleet_hp == 0

    def __str__(self):
        # - for debugging purpose
        taken_ncells = set()
        for occ in self._btype_to_occupied_cells.values():
            taken_ncells |= occ  # union set

        res = ''
        for btype in self.BOAT_TYPES:
            if btype not in self._btype_to_occupied_cells:
                continue
            res += 'btype={} - origincell={}'.format(btype, self._btype_to_origincell[btype])
            res += '\n'

        for j in range(10):
            for i in range(10):
                ncell = j * 10 + i

                if ncell in taken_ncells:
                    cool_char = '?'
                    if self.has(self.AIRCRAFT_CARRIER) and\
                            ncell in self._btype_to_occupied_cells[self.AIRCRAFT_CARRIER]:
                        cool_char = 'A'
                    elif self.has(self.BATTLESHIP) and\
                            ncell in self._btype_to_occupied_cells[self.BATTLESHIP]:
                        cool_char = 'B'
                    elif self.has(self.CRUISER) and\
                            ncell in self._btype_to_occupied_cells[self.CRUISER]:
                        cool_char = 'C'
                    elif self.has(self.SUBMARINE) and\
                            ncell in self._btype_to_occupied_cells[self.SUBMARINE]:
                        cool_char = 'S'
                    elif self.has(self.PATROLBOAT) and\
                            ncell in self._btype_to_occupied_cells[self.PATROLBOAT]:
                        cool_char = 'P'
                    res += '{} '.format(cool_char)

                else:
                    res += '~ '

            res += '\n'
        return res
