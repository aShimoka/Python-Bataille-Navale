#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import the abstract classes.
from abc import ABC, abstractmethod


class GameManager(ABC):
    """
    GameManager class. Holds information that is stored during the entire game's run time.

    Attributes:
        config      The game manager's configuration object.
    """

    def __init__(self, config):
        """
        Class constructor.
        Stores the game manager's configuration object.
        :param config: The configuration object of the class.
        """
        self.config = config

    @abstractmethod
    def begin(self):
        """
        Method called right after the engine finished initializing.
        """
        pass

    def end(self):
        """
        Method called at the very end of the run time.
        """
        pass
