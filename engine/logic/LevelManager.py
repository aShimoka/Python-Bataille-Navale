#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import the abstract classes.
from abc import ABC, abstractmethod


class LevelManager(ABC):
    """
    Base manager class for all game levels.
    This class allows the simple manipulation of level objects.

    Attributes:
        config      The configuration object of this level.
    """

    def __init__(self, config):
        """
        Creates the new level manager.
        Stores the configuration object locally.
        :param config: The configuration object of the level.
        """
        self.config = config

    @abstractmethod
    def begin(self):
        """
        Method called once the level is ready to be loaded.
        """
        pass

    def end(self):
        """
        Method called right before the game gets unloaded.
        """
        pass

    def tick(self, dt):
        """
        Method that gets called evey tick.
        :param dt: The time since the last frame.
        """
        pass
