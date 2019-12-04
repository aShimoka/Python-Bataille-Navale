#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import the base board class.
from battleships.objects.Board import Board

# Import the engine.
import engine
from battleships.objects.FleetModel import FleetModel


class ShipBoard(Board):
    """
    Board object that renders all the ships from the player.
    """

    def __init__(self, parent):
        """
        Class constructor.
        Creates a new board on the screen.
        :param parent: The parent of the board.
        """
        # Call the parent constructor.
        super().__init__(parent)

        # Create the board background.
        ShipBoard.create_background(self, (0, 64, 128), (255, 255, 255))

        self.fleet = FleetModel()  # a model for storing boat positions & handling computations

        # **temporary HACK** so that the ShipBoard.to_ship_list() still functions
        self._ship_w_cache = dict()

    # this method is deprecated!
    def proxy_add_boat(self, shipwidget, newcell, rotation):
        btype = shipwidget.btype
        self.fleet.add_boat(btype, newcell, rotation)
        self._ship_w_cache[btype] = shipwidget

    # this method is deprecated!
    def proxy_update_boat(self, shipwidget, newcell, rotation):
        btype = shipwidget.btype
        self.fleet.update_boat(btype, newcell, rotation)
        self._ship_w_cache[btype] = shipwidget

    # this method is deprecated!
    def to_ship_list(self):
        """
        the method is here only to get retro-compatibility after a big refactoring
        it could be removed in the near future

        Returns: a list of ShipWidget that cannot be moved
        """
        retro_compat_list = list()
        for shipw in self._ship_w_cache.values():
            shipw.disable_grab()
            retro_compat_list.append(shipw)
        del self._ship_w_cache

        return retro_compat_list

    def all_boats_placed(self):
        return self.fleet.is_full()
