#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# import the engine.
import engine


class GameOver(engine.LevelManager):
    """
    Renders the game over screen.
    """

    def begin(self):
        # Add the close handler.
        engine.Engine.input_handler.add_listener(engine.CloseOnEscapeOrQuit())

        # Create the game over message.
        text = engine.TextGameObject(
            engine.Engine.scene,
            "Futura",
            48,
            "You won !" if engine.Engine.game_manager.winner == 0 else "You lost ...",
            (255, 255, 255)
        )
        text.transform.position = engine.math.Vector2(256, 256)
        text.transform.offset = text.size / -2
