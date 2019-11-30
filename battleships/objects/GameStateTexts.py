#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import the engine.
import engine


class GameStateTexts(engine.GameObject):
    """
    Simple game object that groups all game state texts together.
    """

    # Lists all the showable texts.
    TEXT_GAME_STARTING = 0x00
    TEXT_GAME_NEW_TURN = 0x10
    TEXT_GAME_REQ_FIRE = 0x20
    TEXT_GAME_DO_SHOOT = 0x30
    TEXT_GAME_REQ_HIT = 0x40
    TEXT_GAME_GET_HIT_MISS = 0x50
    TEXT_GAME_GET_HIT_HIT = 0x51
    TEXT_GAME_GET_HIT_SUNK = 0x52
    TEXT_GAME_SHOW_HIT_MISS = 0x60
    TEXT_GAME_SHOW_HIT_HIT = 0x61
    TEXT_GAME_SHOW_HIT_SUNK = 0x62
    TEXT_GAME_AWAIT_SHOT = 0x70
    TEXT_GAME_END_TURN = 0x80
    TEXT_GAME_END_GAME = 0x90

    def __init__(self, parent=None):
        """
        Class constructor.
        Creates all the text objects.
        :param parent: The parent of this object.
        """
        # Call the parent constructor.
        super().__init__(parent)

        # Create the text objects.
        self.t = {
            self.TEXT_GAME_STARTING:
                engine.TextGameObject(self, "Futura", 25, "Starting a new game !", (255, 255, 255)),
            self.TEXT_GAME_NEW_TURN:
                engine.TextGameObject(self, "Futura", 25, "Starting a new turn", (255, 255, 255)),
            self.TEXT_GAME_REQ_FIRE:
                engine.TextGameObject(self, "Futura", 25, "Please, select where to shoot.", (255, 255, 255)),
            self.TEXT_GAME_DO_SHOOT:
                engine.TextGameObject(self, "Futura", 25, "FIRE !", (255, 255, 255)),
            self.TEXT_GAME_REQ_HIT:
                engine.TextGameObject(self, "Futura", 25, "UNDER FIRE !", (255, 255, 255)),
            self.TEXT_GAME_GET_HIT_MISS:
                engine.TextGameObject(self, "Futura", 25, "They missed", (255, 255, 255)),
            self.TEXT_GAME_GET_HIT_HIT:
                engine.TextGameObject(self, "Futura", 25, "We are hit !", (255, 255, 255)),
            self.TEXT_GAME_GET_HIT_SUNK:
                engine.TextGameObject(self, "Futura", 25, "We are going down !!!", (255, 255, 255)),
            self.TEXT_GAME_SHOW_HIT_MISS:
                engine.TextGameObject(self, "Futura", 25, "We missed", (255, 255, 255)),
            self.TEXT_GAME_SHOW_HIT_HIT:
                engine.TextGameObject(self, "Futura", 25, "That's a hit !", (255, 255, 255)),
            self.TEXT_GAME_SHOW_HIT_SUNK:
                engine.TextGameObject(self, "Futura", 25, "It is going down !!!", (255, 255, 255)),
            self.TEXT_GAME_AWAIT_SHOT:
                engine.TextGameObject(self, "Futura", 25, "The enemy is going to fire, get ready !", (255, 255, 255)),
            self.TEXT_GAME_END_TURN:
                engine.TextGameObject(self, "Futura", 25, "Turn over.", (255, 255, 255)),
            self.TEXT_GAME_END_GAME:
                engine.TextGameObject(self, "Futura", 25, "Game over.", (255, 255, 255))
        }

        self.hide_all()
        for t in self.t.values():
            t.transform.offset = t.size / -2

    def hide_all(self):
        for t in self.t.values():
            t.visible = False

    def show_text(self, text):
        self.hide_all()
        self.t[text].visible = True

