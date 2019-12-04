#  Copyright © 2019
#  authored by Jean-Baptiste CAILLAUD et al.
#  contributor list on: https://github.com/yShimoka/python-bataille-navale

from abc import ABC
from copy import copy

import pygame
import pygame.locals

import engine
from battleships.objects.FleetModel import FleetModel


class ShipWidget(engine.TexturedGameObject, engine.InputListener, ABC):
    """
    Base class for all the ships that are usable on the level.

    Attributes:
        length      The length (in squares) of the ship.
        board       Reference to the board instance.
        rotation    The rotation angle of the ship.
    """

    def __init__(self, btype, board, length, texture):
        """
        Class constructor.
        Creates a new ship instance.
        :param board: The board that this boat is placed on.
        :param length: The length of the ship, in squares.
        :param texture: The texture of this ship.
        """
        # Call the parent constructor.
        super().__init__(board, texture, engine.math.Vector2(49, 48 * length + 1))

        self.btype = btype  # linked to the model...
        self._model_ref = board.fleet

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

        # Check if the mouse was released.
        if event.type == pygame.locals.MOUSEBUTTONUP:
            if self.__is_grabbed:
                # Drop the ship.
                self.__is_grabbed = False
                # If the position is valid.
                newcell = self.get_cell()
                if self.board.fleet.can_add(self.btype, newcell, self.compute_dir()):

                    # Place the boat on the board.
                    if self.board.fleet.has(self.btype):
                        self.board.proxy_update_boat(self, newcell, self.compute_dir())
                    else:
                        self.board.proxy_add_boat(self, newcell, self.compute_dir())

                else:
                    # Put the boat back at its place.
                    self.transform.set_world_position(self.initial_position)
                    self.rotate(self.initial_rotation)

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

    # the goal here is to better dissociate model and view, if the view/ GUI evolves
    # the model should not be impacted
    def compute_dir(self):
        if self.rotation == 1:
            return FleetModel.F_SOUTH
        if self.rotation == 2:
            return FleetModel.F_EAST
        if self.rotation == 3:
            return FleetModel.F_NORTH
        if self.rotation == 4:
            return FleetModel.F_WEST
        raise ValueError('cannot compute dir from self.rotation(= {}) stored in ShipWidget obj'.format(self.rotation))

    def rotate(self, angle):
        """
        Rotates the ship object by the given amount - COUNTER-CW

        Possible values: 1 (0 deg), 2 (90 deg), 3 (180 deg) or 4 (270 deg)
        :param angle: The angle to rotate the ship by.
        """
        # Compute the angle from the given value.
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


class AircraftCarrier(ShipWidget):
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
        super().__init__(FleetModel.AIRCRAFT_CARRIER, parent, 5, "AircraftCarrier")


class BattleShip(ShipWidget):
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
        super().__init__(FleetModel.BATTLESHIP, parent, 4, "BattleShip")


class Cruiser(ShipWidget):
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
        super().__init__(FleetModel.CRUISER, parent, 3, "Cruiser")


class PatrolBoat(ShipWidget):
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
        super().__init__(FleetModel.PATROLBOAT, parent, 2, "PatrolBoat")


class Submarine(ShipWidget):
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
        super().__init__(FleetModel.SUBMARINE, parent, 3, "Submarine")
