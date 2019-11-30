#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import the LevelManager class.
from engine import LevelManager, Engine, CloseOnEscapeOrQuit, InputListener, TexturedGameObject, math, TextGameObject

from pygame.locals import MOUSEBUTTONDOWN

class NextListener(InputListener):
    def handle_input(self, event):
        if event.type == MOUSEBUTTONDOWN:
            Engine.load_level("LevelBuilding")

class MainMenu(LevelManager):
    def begin(self):
        # Add the close listener.
        Engine.input_handler.add_listener(CloseOnEscapeOrQuit())

        # Add the next listener.
        Engine.input_handler.add_listener(NextListener())

        # Play the main menu music.
        Engine.play_sound("MenuMusic", -1, 50)

        # Load the objects.
        self.__create_objects()

    def end(self):
        Engine.input_handler.clear_listeners()

    def __create_objects(self):
        # Create the antimatter icon.
        am_icon = TexturedGameObject(Engine.scene, "AntiMatterEngine", math.Vector2(64, 64))
        am_icon.transform.position = math.Vector2(448, 48)
        am_icon.transform.offset = am_icon.size / -2

        # Create the antimatter text.
        am_text = TextGameObject(am_icon, "Futura", 12, "Anti-Matter Engine", (128, 128, 128))
        am_text.transform.position = math.Vector2(0, -36)
        am_text.transform.offset = am_text.size / -2

        # Create the title text.
        title = TextGameObject(Engine.scene, "Futura Italic", 64, "Battleships", (255, 128, 128))
        title.transform.position = math.Vector2(256, 256)
        title.transform.offset = title.size / -2

        # Create the sub text.
        subtitle = TextGameObject(title, "Futura", 48, "Click anywhere to play.", (255, 255, 255))
        subtitle.transform.position = math.Vector2(0, 96)
        subtitle.transform.offset = subtitle.size / -2
