#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import the engine.
import engine
import sys

# Import the player indices.
from battleships.managers.GameManager import PLAYER_1, PLAYER_2
# Import the Player class.
from battleships.players.Player import Player


class Game(engine.LevelManager):
    """
    Main game level manager.
    Handles the duration of the entire game level.
    """

    # List of all the player indices.
    PLAYERS = [PLAYER_1, PLAYER_2]

    # Delay between each phase of the game.
    DELAY = 1

    # List of all the phases of the game.
    PHASE_PREPARE = -1
    PHASE_START_TURN = 0
    PHASE_REQUEST_SHOT = 1
    PHASE_FIRE = 2
    PHASE_REQUEST_HIT = 3
    PHASE_HIT = 4
    PHASE_SHOW_HIT = 5
    PHASE_AWAIT_OPPONENT_SHOT = 6
    PHASE_END_TURN = 7

    def __init__(self, config):
        """
        Class constructor.
        Configures the level manager instance.
        :param config: The configuration info.
        """
        super().__init__(config)

        # Prepare the timer.
        self.timer = 0

        # Set the current player index.
        self.current_player_index = 0
        # If we are the client, the server goes first.
        for i in range(len(sys.argv)):
            if sys.argv[i] == "--client":
                self.current_player_index = 1

        # Prepare the phase counter.
        self.__current_phase = Game.PHASE_PREPARE
        # Prepare the shot location store.
        self.__current_fire_location = None
        self.__current_fire_effect = None

    def begin(self):
        """
        Called by the engine at the beginning of the level.
        """
        # Add the close listener.
        engine.Engine.input_handler.add_listener(engine.CloseOnEscapeOrQuit())
        # Play the game music.
        engine.Engine.stop_sound("MenuMusic")
        engine.Engine.play_sound("GameMusic", -1, 50)

    def tick(self, dt):
        """
        Tick method.
        Waits for GAME_DELAY seconds before moving onto the next phase.
        :param dt: The time since the last frame.
        """
        # Increment the timer.
        self.timer += dt

        # If the timer reached the end.
        if self.timer > Game.DELAY:
            # Reset the timer.
            self.timer = 0

            # Advance to the next phase.
            self.__advance()

    def player_fire(self, at: engine.math.Vector2):
        """
        Used by the player class to fire at the specified location.
        :param at: The position to fire at.
        """
        # Store the position of the shot.
        self.__current_fire_location = at

        # Move on to the hit response.
        self.__current_phase = self.PHASE_REQUEST_HIT

    def player_hit(self, at: engine.math.Vector2, hit_result: int):
        """
        Used by the player class to notify that a hit event occurred.
        :param at: Where the shot landed.
        :param hit_result: The results of the shot.
        """
        # Store the effect of the shot.
        self.__current_fire_location = at
        self.__current_fire_effect = hit_result

        # Move on to the hit response.
        self.__current_phase = self.PHASE_SHOW_HIT

    def __advance(self):
        """
        Advances onto the next phase of the game.
        """
        # If the game is being prepared.
        if self.__current_phase == self.PHASE_PREPARE:
            # If both players are ready.
            if self.__get_current_player().pre_game_prepare() and self.__get_other_player().pre_game_prepare():
                # Start the turn.
                self.__current_phase = self.PHASE_START_TURN

                # Begin the game for each player.
                self.__get_current_player().start_game()
                self.__get_other_player().start_game()

        # If the game is being set up.
        elif self.__current_phase == self.PHASE_START_TURN:
            # Advance onto the request fire phase.
            self.__current_phase = self.PHASE_REQUEST_SHOT

            # Call the start turn method for both players.
            self.__get_current_player().start_turn()
            self.__get_other_player().start_turn()

        # If the game requires the user to shoot.
        elif self.__current_phase == self.PHASE_REQUEST_SHOT:
            # Advance onto the fire phase.
            self.__current_phase = self.PHASE_FIRE

            # Call the shoot method of the user.
            self.__get_current_player().request_shot()

        # If the game requires the other user to be hit.
        elif self.__current_phase == self.PHASE_REQUEST_HIT:
            # Advance onto the hit phase.
            self.__current_phase = self.PHASE_HIT

            # Call the other player's request hit method.
            self.__get_other_player().request_hit(self.__current_fire_location)

        # If the game shows the hit result.
        elif self.__current_phase == self.PHASE_SHOW_HIT:
            # Advance onto the await phase.
            self.__current_phase = self.PHASE_AWAIT_OPPONENT_SHOT

            # Call the player's show hit method.
            self.__get_current_player().show_hit(self.__current_fire_location, self.__current_fire_effect)

        # If the game awaits the next shot.
        elif self.__current_phase == self.PHASE_AWAIT_OPPONENT_SHOT:
            # If the opponent has lost.
            if self.__current_fire_effect == Player.SHOT_HIT_TYPE_GAME_OVER:
                # Store the winner's index.
                engine.Engine.game_manager.winner = self.current_player_index
                # Move to the game over phase.
                engine.Engine.load_level("GameOver")
            else:
                # Call the player's await hit method.
                self.__get_current_player().await_opponent_shot()

                # If the turn is over.
                if self.current_player_index == 1:
                    # Advance to the next turn.
                    self.__current_phase = self.PHASE_END_TURN
                else:
                    # Advance onto the next fire phase.
                    self.__current_phase = self.PHASE_REQUEST_SHOT
                    # Increment the user counter.
                    self.current_player_index = 1

        elif self.__current_phase == self.PHASE_END_TURN:
            # Start a new turn.
            self.__current_phase = self.PHASE_START_TURN
            # Decrement the user counter.
            self.current_player_index = 0

            # Call the end turn methods.
            self.__get_current_player().end_turn()
            self.__get_other_player().end_turn()

    def __get_current_player(self):
        """
        Returns the player at the current_player index.
        """
        return engine.Engine.game_manager.players[self.current_player_index]

    def __get_other_player(self):
        """
        Returns the player not at the current_player index.
        """
        return engine.Engine.game_manager.players[(self.current_player_index + 1) % 2]
