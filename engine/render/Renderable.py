#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import the abstract class object.
from abc import ABC, abstractmethod


class Renderable(ABC):
    """
    Main renderable object class.
    This class should be overloaded for each renderable type.
    """

    def __init__(self):
        """
        Class constructor.
        Declares the flags of the renderable.
        """
        # Flag set if the renderable is visible.
        self.visible = True

    @abstractmethod
    def render(self, window):
        """
        Renders the object to the display.
        :param window: The surface to render onto.
        """
        pass
