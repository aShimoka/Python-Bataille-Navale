#  Copyright © 2019 CAILLAUD Jean-Baptiste.
from engine import Engine
from engine.input.CloseOnEscapeOrQuit import CloseOnEscapeOrQuit
from engine.logic.GameManager import GameManager
from engine.logic.Math import Vector2
from engine.logic.Primitives import RectGameObject, LineGameObject

class MovingRect(RectGameObject):
    def tick(self, dt):
        self.transform.position.x = self.transform.position.x + (32 * dt)
        if self.transform.position.x > 512:
            self.transform.position.x = 0
        pass

class GameMode(GameManager):
    def begin(self):
        rect = MovingRect(Engine.scene, Vector2(128, 128), 5, (255, 0, 0), (0, 255, 0))
        rect.transform.position = Vector2(256, 256)
        Engine.input_handler.add_listener(CloseOnEscapeOrQuit())


def start():
    Engine.initialize()

    Engine.start()
