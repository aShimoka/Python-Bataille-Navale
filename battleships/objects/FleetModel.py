#  Copyright © 2019
#  authored by Jean-Baptiste CAILLAUD et al.
#  contributor list on: https://github.com/yShimoka/python-bataille-navale

from copy import copy

from engine.logic import Vector2


class FleetModel:
    """
    model for storing boat positions & handling computations
    """

    NB_BOAT_TYPES = 5
    BOAT_TYPES = range(0x2193, 0x2193 + NB_BOAT_TYPES)  # enumerating 5 symbols

    AIRCRAFT_CARRIER, BATTLESHIP, CRUISER, PATROLBOAT, SUBMARINE = BOAT_TYPES

    BOAT_LENGTHS = {
        AIRCRAFT_CARRIER: 5,
        BATTLESHIP: 4,
        CRUISER: 3,
        SUBMARINE: 3,
        PATROLBOAT: 2
    }

    def __init__(self):
        self._btype_to_origincell = dict()
        self._btype_to_rotation = dict()

        self._btype_to_occupied_cells = dict()

        self._btype_to_hitpoints = copy(self.BOAT_LENGTHS)

    def has(self, boat_type):
        return boat_type in self._btype_to_origincell

    def is_full(self):
        return len(self._btype_to_origincell) == self.NB_BOAT_TYPES

    @classmethod
    def _enforce_arg_validity(cls, bt, c):
        assert (bt in cls.BOAT_TYPES)
        assert ((-1 < c.x < 10) and (-1 < c.y < 10))

    def __compute_occ_cells(self, btype):
        origincell = self._btype_to_origincell[btype]
        boat_len = self.BOAT_LENGTHS[btype]
        boat_dir = self._btype_to_rotation[btype]

        self._btype_to_occupied_cells[btype] = FleetModel.__get_covered_cells(origincell, boat_len, boat_dir)

    def add_boat(self, btype, cell: Vector2, rotation: int):
        self._enforce_arg_validity(btype, cell)

        self._btype_to_origincell[btype] = cell
        self._btype_to_rotation[btype] = rotation

        self.__compute_occ_cells(btype)

    def update_boat(self, btype, new_cell: Vector2, rotation_val=None):
        self._enforce_arg_validity(btype, new_cell)

        self._btype_to_origincell[btype] = new_cell
        if rotation_val is not None:
            self._btype_to_rotation[btype] = rotation_val

        self.__compute_occ_cells(btype)

    def can_add(self, btype, cell, direction):
        """
        Checks if the position is valid for the specified ship.
        :param btype: int, see the FleetModel class
        :param cell: The cell that is requested.
        :param direction: The direction of the ship.

        :return: True if the position is valid.
        """
        length = self.BOAT_LENGTHS[btype]

        # Check if the position is within the bounds.
        if cell.x >= 0 and cell.y >= 0:
            if cell.x <= 10 and cell.y <= 10:
                # If the ship is in the bounds.
                if direction % 2 == 0:
                    if cell.x <= 10 - length:
                        # Check for collisions
                        return self.collision_check(cell, length, direction) is None
                else:
                    if cell.y <= 10 - length:
                        # Check for collisions
                        return self.collision_check(cell, length, direction) is None

    @staticmethod
    def __get_covered_cells(cell, length, direction):
        covered_cells = set()
        for i in range(length):
            if direction % 2 == 0:
                covered_cells.add(i + (cell.x + cell.y * 10))
            else:
                covered_cells.add((i * 10) + (cell.x + cell.y * 10))
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
