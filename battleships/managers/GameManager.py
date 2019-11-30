#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import the game engine.
import engine


PLAYER_1 = 0
PLAYER_2 = 1


class GameManager(engine.GameManager):
    """
    Battleships' GameManager class.
    Handles the lifetime of the game.

    Attributes:
        players     The players of the game.
    """

    def __init__(self, config):
        """
        Class constructor.
        :param config: The configuration object.
        """
        super().__init__(config)

        # Prepare the players list.
        self.players = {PLAYER_1: None, PLAYER_2: None}
        # Prepare the human boat store.
        self.human_boats = []
        # Prepare the winner store.
        self.winner = 0

    def begin(self):
        """
        Called at the beginning of the game.
        Loads all the settings from the configuration file.
        """
        self.players[PLAYER_1] = engine.Engine.load_class(self.config["Players"]["player_1"])()
        self.players[PLAYER_2] = engine.Engine.load_class(self.config["Players"]["player_2"])()
