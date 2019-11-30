#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import the abstract class.
from abc import ABC
# Import the copy tool.
from copy import copy
# Import pygame
import pygame
import pygame.locals

# Import the engine.
import engine


class Ship(engine.TexturedGameObject, engine.InputListener, ABC):
    """
    Base class for all the ships that are usable on the level.

    Attributes:
        length      The length (in squares) of the ship.
        board       Reference to the board instance.
        rotation    The rotation angle of the ship.
    """

    def __init__(self, board, length, texture):
        """
        Class constructor.
        Creates a new ship instance.
        :param board: The board that this boat is placed on.
        :param length: The length of the ship, in squares.
        :param texture: The texture of this ship.
        """
        # Call the parent constructor.
        super().__init__(board, texture, engine.math.Vector2(49, 48 * length + 1))
        self.texture = self.texture.convert_alpha()
        self.base_texture = self.texture.copy()
        self.base_size = copy(self.size)
        self.board = board

        # Store the length of the ship.
        self.length = length
        self.damage = 0

        # Flag set if the ship is being grabbed.
        self.__is_grabbed = False
        # Current rotation of the ship.
        self.rotation = 1
        # Store the initial position of the ship.
        self.initial_position = copy(self.transform.position)
        self.initial_rotation = self.rotation
        self.__is_on_board = False

    def enable_drag(self):
        """
        Enables the drag and drop behaviour of the ship.
        """
        # Start listening to inputs.
        engine.Engine.input_handler.add_listener(self)

    def disable_grab(self):
        """
        Disables the drag and drop behaviour of the ship.
        """
        # Stop listening to inputs.
        engine.Engine.input_handler.remove_listener(self)
        # Reset the is grabbed toggle.
        self.__is_grabbed = False

    def handle_input(self, event):
        """
        Handles drag and drop inputs.
        :param event: The event that is parsed.
        """
        # Check if the ship was clicked.
        if event.type == pygame.locals.MOUSEBUTTONDOWN:
            if engine.math.Vector2.in_rect(
                    engine.math.Vector2(event.pos[0], event.pos[1]),
                    self.transform.get_world_position(),
                    self.size
            ):
                # Set the grabbed flag.
                self.__is_grabbed = True
                # Store the initial position of the ship.
                self.initial_position = self.transform.get_world_position()
                self.initial_rotation = self.rotation
                # Move the boat to the position.
                self.transform.set_world_position(engine.math.Vector2(event.pos[0], event.pos[1]))
                # If the boat was on the board.
                if self.__is_on_board:
                    self.board.remove_boat(self)

        # Check if the mouse was released.
        if event.type == pygame.locals.MOUSEBUTTONUP:
            if self.__is_grabbed:
                # Drop the ship.
                self.__is_grabbed = False
                # If the position is valid.
                if self.board.position_is_valid(self.get_cell(), self.length, self.rotation):
                    # Place the boat on the board.
                    self.board.place_boat(self)
                    self.__is_on_board = True
                else:
                    # Put the boat back at its place.
                    self.transform.set_world_position(self.initial_position)
                    self.rotate(self.initial_rotation)
                    # If the boat was on the board, put it back.
                    if self.__is_on_board:
                        self.board.place_boat(self)

        # Check if the mouse moved.
        if event.type == pygame.locals.MOUSEMOTION:
            if self.__is_grabbed:
                # If the mouse is over the board.
                mouse_pos = engine.math.Vector2(event.pos[0], event.pos[1])
                if engine.math.Vector2.in_rect(mouse_pos, self.board.get_top_left(), self.board.get_size()):
                    # Lock the position to the board.
                    mouse_pos = ((mouse_pos - self.board.get_top_left()) // self.board.CELL_SIZE) * self.board.CELL_SIZE
                    self.transform.set_world_position(self.board.get_top_left() + mouse_pos)
                else:
                    # Move the boat to the position.
                    self.transform.set_world_position(mouse_pos)

        # If the boat is grabbed.
        if self.__is_grabbed:
            # Check if the R key was pressed.
            if event.type == pygame.locals.KEYDOWN:
                if event.key == pygame.locals.K_r:
                    # Rotate the ship once.
                    self.rotation = (self.rotation % 4) + 1
                    self.rotate(self.rotation)

    def get_cell(self):
        """
        Returns the cell that this ship is placed on.
        """
        return (self.transform.get_world_position() - self.board.get_top_left()) // self.board.CELL_SIZE

    def rotate(self, angle):
        """
        Rotates the ship object by the given amount.
        Possible values: 1 (0 deg), 2 (90 deg), 3 (180 deg) or 4 (270 deg)
        :param angle: The angle to rotate the ship by.
        """
        # Compute the angle from the given value.
        deg_angle = None
        if angle == 1:
            deg_angle = 0
        elif angle == 2:
            deg_angle = 90
        elif angle == 3:
            deg_angle = 180
        elif angle == 4:
            deg_angle = 270
        else:
            raise ValueError("Cannot rotate the ship by values other than 1, 2, 3 or 4. Got {}".format(angle))

        # Check if the size parameters need to be swapped.
        self.size = copy(self.base_size)
        if angle % 2 == 0:
            tmp = self.size.x
            self.size.x = self.size.y
            self.size.y = tmp

        self.texture = pygame.transform.rotate(self.base_texture, deg_angle)
        self.rotation = angle


class AircraftCarrier(Ship):
    """
    Class representing an aircraft carrier.
    """

    def __init__(self, parent):
        """
        Class constructor.
        Creates a new ship instance.
        :param parent: The parent of the ship.
        """
        # Call the parent constructor.
        super().__init__(parent, 5, "AircraftCarrier")


class BattleShip(Ship):
    """
    Class representing a battleship.
    """

    def __init__(self, parent):
        """
        Class constructor.
        Creates a new ship instance.
        :param parent: The parent of the ship.
        """
        # Call the parent constructor.
        super().__init__(parent, 4, "BattleShip")


class Cruiser(Ship):
    """
    Class representing a cruiser.
    """

    def __init__(self, parent):
        """
        Class constructor.
        Creates a new ship instance.
        :param parent: The parent of the ship.
        """
        # Call the parent constructor.
        super().__init__(parent, 3, "Cruiser")


class PatrolBoat(Ship):
    """
    Class representing a patrol boat.
    """

    def __init__(self, parent):
        """
        Class constructor.
        Creates a new ship instance.
        :param parent: The parent of the ship.
        """
        # Call the parent constructor.
        super().__init__(parent, 2, "PatrolBoat")


class Submarine(Ship):
    """
    Class representing a submarine.
    """

    def __init__(self, parent):
        """
        Class constructor.
        Creates a new ship instance.
        :param parent: The parent of the ship.
        """
        # Call the parent constructor.
        super().__init__(parent, 3, "Submarine")
