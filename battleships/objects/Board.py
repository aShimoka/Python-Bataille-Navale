#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import the copy tool.
from copy import copy
# Import the abstract class.
from abc import ABC

# Import the engine.
import engine


class Board(engine.GameObject, ABC):
    """
    Main board abstract class.
    Represents a 10x10 usable board.
    """

    # Defines the size of a cell.
    CELL_SIZE = 48

    @staticmethod
    def get_size():
        """
        Returns size of the board.
        """
        return engine.math.UNIT_VECTOR * Board.CELL_SIZE * 10

    @staticmethod
    def create_background(parent, color, line_color):
        """
        Creates the background rect of the board.
        :param parent: The parent to attach the board to.
        :param color: The color of the background.
        :param line_color: The color of the lines.
        """
        # Create the rectangle for the background.
        rect = engine.RectGameObject(
            parent,
            engine.math.Vector2(Board.CELL_SIZE * 10, Board.CELL_SIZE * 10),
            4,
            color,
            (255, 255, 255)
        )
        rect.transform.offset = rect.extent / -2

        # Create the lines.
        Board.__create_lines(rect, line_color)

    def get_top_left(self):
        """
        Returns the "true" top left of the board.
        """
        return self.transform.position - self.get_size() / 2

    @staticmethod
    def __create_lines(parent, color):
        """
        Creates the lines for the background.
        :param parent: The parent of all the line objects.
        :param color: The color of the lines.
        """
        # Loop through the vertical lines.
        for i in range(1, 10):
            engine.LineGameObject(
                parent,
                engine.math.Vector2(0, Board.CELL_SIZE * i),
                engine.math.Vector2(Board.CELL_SIZE * 10, 0),
                2,
                color
            ).transform.offset = copy(parent.transform.offset)
        # Loop through the horizontal lines.
        for i in range(1, 10):
            engine.LineGameObject(
                parent,
                engine.math.Vector2(Board.CELL_SIZE * i, 0),
                engine.math.Vector2(0, Board.CELL_SIZE * 10),
                2,
                color
            ).transform.offset = copy(parent.transform.offset)
