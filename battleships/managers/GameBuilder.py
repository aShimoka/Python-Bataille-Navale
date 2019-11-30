#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import pygame locals.
import pygame.locals

# Import the engine.
import engine

# Import the ships.
from battleships.objects import *


class NextButton(engine.GameObject, engine.InputListener):
    """
    Button placed on the bottom right of the window.
    Is used to advance to the next level, if the board is complete.
    """

    def __init__(self, parent, board):
        """
        Class constructor.
        """
        # Call the parent constructor.
        super().__init__(parent)

        # Store the board object.
        self.board = board

        # Create the text objects.
        self.disabled_text = engine.TextGameObject(self, "Futura Italic", 72, "Next", (64, 64, 64))
        self.enabled_text = engine.TextGameObject(self, "Futura", 72, "Next", (96, 164, 96))
        self.selected_text = engine.TextGameObject(self, "Futura", 72, "Next", (128, 255, 128))

        # Hide the enabled and selected texts.
        self.enabled_text.visible = False
        self.selected_text.visible = False

        # Place the buttons.
        self.disabled_text.transform.position = engine.math.Vector2(512, 384)
        self.enabled_text.transform.position = engine.math.Vector2(512, 384)
        self.selected_text.transform.position = engine.math.Vector2(512, 384)

        # Enable listening.
        engine.Engine.input_handler.add_listener(self)

    def handle_input(self, event):
        """
        Listens to the game inputs and checks if the button is being pressed.
        :param event:
        """

        # If the button is enabled.
        if self.enabled_text.visible or self.selected_text.visible:
            # If the event is a mouse motion.
            if event.type == pygame.locals.MOUSEMOTION:
                # If the mouse is on the button.
                mouse_pos = engine.math.Vector2(event.pos[0], event.pos[1])
                if engine.math.Vector2.in_rect(mouse_pos, engine.math.Vector2(512, 384), self.disabled_text.size):
                    # Show the selected button.
                    self.selected_text.visible = True
                    self.enabled_text.visible = False
                else:
                    # Hide the selected button.
                    self.selected_text.visible = False
                    self.enabled_text.visible = True

            # If the event is a mouse release.
            if event.type == pygame.locals.MOUSEBUTTONUP:
                # If the selected button is shown.
                if self.selected_text.visible:
                    # Load the next level.
                    GameBuilder.load_next_level()
        else:
            # If the event is a mouse motion.
            if event.type == pygame.locals.MOUSEMOTION:
                # Check if the board is full.
                if self.board.all_boats_placed():
                    # Enable the text.
                    self.enabled_text.visible = True
                    self.disabled_text.visible = False


class GameBuilder(engine.LevelManager):
    """
    Level of the game that is used to build the player's board.
    The boats can be placed wherever the player desires but cannot overlap.
    """

    # Current board used.
    board = None

    def __init__(self, config):
        """
        Class constructor.
        Prepares the boat variables.
        :param config: The configuration object.
        """
        super().__init__(config)
        # Prepare the ships store.
        self.ships = []

    def begin(self):
        """
        Called on the start of the level.
        """
        # Add the close listener.
        engine.Engine.input_handler.add_listener(engine.CloseOnEscapeOrQuit())
        # Create the board.
        GameBuilder.board = ShipBoard(engine.Engine.scene)
        GameBuilder.board.transform.position = engine.math.Vector2(256, 256)

        # Create the button.
        NextButton(engine.Engine.scene, GameBuilder.board)
        # Create the rotate instructions.
        dnd = engine.TextGameObject(engine.Engine.scene, "Futura Italic", 20, "Drag and drop ships.", (255, 255, 255))
        rot = engine.TextGameObject(engine.Engine.scene, "Futura Italic", 20, "R to rotate.", (255, 255, 255))
        dnd.transform.set_world_position(engine.math.Vector2(512, 316))
        rot.transform.set_world_position(engine.math.Vector2(512, 348))

        # Create all the ships.
        self.ships = [
            AircraftCarrier(GameBuilder.board),
            BattleShip(GameBuilder.board),
            Cruiser(GameBuilder.board),
            Submarine(GameBuilder.board),
            PatrolBoat(GameBuilder.board)
        ]

        # Place the ships and enable dragging.
        for i in range(len(self.ships)):
            # Rotate the ships 90 degrees.
            self.ships[i].rotate(2)
            # Set their position.
            self.ships[i].transform.set_world_position(engine.math.Vector2(512, 48 * i + 64))
            # Enable dragging.
            self.ships[i].enable_drag()

    @staticmethod
    def load_next_level():
        """
        Loads the next level, as described in the ini file.
        """
        # Stop all boats from being grabbed.
        for boat in GameBuilder.board.placed_ships:
            boat.disable_grab()
        # Store the boats in the game manager.
        engine.Engine.game_manager.human_boats = GameBuilder.board.placed_ships
        # Load the next level.
        engine.Engine.load_level("Game")
