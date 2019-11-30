#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import the board base class.
from battleships.objects import Board

# Import the engine.
import engine


class ShotBoard(Board):
    """
    Board object that renders all the shots from the player.
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
        ShotBoard.create_background(self, (200, 200, 200), (64, 64, 64))

        # List of all the placed shots.
        self.placed_shots = []

    def add_shot(self, at, hit):
        """
        Adds a new shot on the board.
        :param at: Where to put the shot.
        :param hit: True if the shot is a hit.
        """
        new_shot = engine.RectGameObject(
            self,
            engine.math.Vector2(32, 32),
            0,
            (255, 0, 0) if hit else (64, 64, 64)
        )
        print(self.get_top_left())
        new_shot.transform.set_world_position(at * Board.CELL_SIZE + self.get_top_left())
        new_shot.transform.offset = engine.math.Vector2(8, 8)
