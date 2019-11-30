#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import the base board class.
from battleships.objects.Board import Board

# Import the engine.
import engine


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

        # List of all the placed ships.
        self.placed_ships = []

    def remove_boat(self, boat):
        if boat in self.placed_ships:
            self.placed_ships.remove(boat)

    def place_boat(self, boat):
        self.placed_ships.append(boat)

    def all_boats_placed(self):
        return len(self.placed_ships) == 5

    def position_is_valid(self, cell, length, direction):
        """
        Checks if the position is valid for the specified ship.
        :param cell: The cell that is requested.
        :param length: The length of the ship to place.
        :param direction: The direction of the ship.
        :return: True if the position is valid.
        """
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
        covered_cells = []
        for i in range(length):
            if direction % 2 == 0:
                covered_cells.append(i + (cell.x + cell.y * 10))
            else:
                covered_cells.append((i * 10) + (cell.x + cell.y * 10))

        return covered_cells

    def collision_check(self, cell, length, direction):
        # Compute all the cells covered by the ship/shot.
        covered_cells = ShipBoard.__get_covered_cells(cell, length, direction)

        # Loop through all the ships.
        for ship in self.placed_ships:
            ship_cells = ShipBoard.__get_covered_cells(ship.get_cell(), ship.length, ship.rotation)
            intersect = list(set(covered_cells) & set(ship_cells))
            if len(intersect) > 0:
                return ship

        return None

