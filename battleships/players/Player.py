#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import the abstract class and methods.
from abc import ABC, abstractmethod

# Import the engine.
import engine


class Player(ABC):
    """
    Base class for all the Players of the game.
    Controlled by the level manager to manipulate the game.

    Attributes:
        opponent    The opponent that this player is playing against.
    """

    # Defines all the possible shots responses.
    SHOT_HIT_TYPE_MISS = 0
    SHOT_HIT_TYPE_HIT = 1
    SHOT_HIT_TYPE_HIT_AND_SUNK = 2
    SHOT_HIT_TYPE_GAME_OVER = 3

    def __init__(self):
        """

        """
        # The opponent that this player is playing against.
        self.opponent = None
        # List of all the moves made by this player.
        self.moves = {}

    def pre_game_prepare(self):
        return True

    @abstractmethod
    def start_game(self):
        """
        Starts the actual game.
        Allows the player to set itself up.
        """
        pass

    @abstractmethod
    def start_turn(self):
        """
        Starts the turn of the current player.
        :returns: True if the player has lost.
        """
        pass

    @abstractmethod
    def end_turn(self):
        """
        Ends the turn of the player.
        """
        pass

    @abstractmethod
    def request_shot(self):
        """
        Called by the manager when it become this player's turn to shoot.
        """
        pass

    @abstractmethod
    def request_hit(self, at: engine.math.Vector2):
        """
        Called by the manager to check if the hit at the given location was successful.
        """
        pass

    @abstractmethod
    def show_hit(self, at: engine.math.Vector2, hit_type: int):
        """
        Shows the user the effect of their shot.
        Also, adds the shot to the moves list.
        :param at: Where the shot landed.
        :param hit_type: One of SHOT_TYPE_.
        """
        # Add the shot to the moves.
        self.moves[at.tuple()] = hit_type

    @abstractmethod
    def await_opponent_shot(self):
        """
        Called by the manager to notify the player that
        they should be waiting for the enemy's move.
        """
        pass

    def tick(self, dt):
        pass

    def fire(self, at):
        """
        Fires a round at the specified target.
        :param at: Where to fire.
        :return: True if the fire event was accepted.
        """
        # Check if the fire event did not already occur at that position.
        if at.tuple() in self.moves.keys():
            return False

        # Tell the manager that we fired.
        engine.Engine.current_level.player_fire(at)
        return True

    def hit(self, at: engine.math.Vector2, hit_status: int):
        """
        Called by the player to notify the manager that a boat was hit.
        :param at: Where the shot landed.
        :param hit_status: One of the four SHOT_TYPE.
        """
        # Tell the manager the result of our hit.
        engine.Engine.current_level.player_hit(at, hit_status)
