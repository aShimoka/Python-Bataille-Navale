#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import pygame locals.
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

# Import the engine classes.
from engine.Engine import Engine
from engine.input.InputListener import InputListener


class CloseOnEscapeOrQuit(InputListener):
    """
    Simple class that closes the engine on a escape press or a QUIT event.
    """

    def handle_input(self, event):
        """
        Checks if the event is a QUIT or a K_ESCAPE.
        Then, requests the engine to exit.
        :param event: The event to parse.
        """
        if event.type == QUIT:
            Engine.request_exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                Engine.request_exit()
