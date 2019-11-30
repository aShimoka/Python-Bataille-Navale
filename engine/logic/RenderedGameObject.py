#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import the renderable class.
from engine.render.Renderable import Renderable
# Import the gameobject class.
from engine.logic.GameObject import GameObject
# Import the engine class.
from engine.Engine import Engine

# Import the abstract class.
from abc import ABC, abstractmethod


class RenderedGameObject(GameObject, Renderable, ABC):
    """
    Base class used for all the game objects that are rendered on the screen.
    """

    def __init__(self, parent):
        """
        Class constructor.
        Creates a new instance of the rendered object.
        Registers itself into the engine's renderer.
        :param parent: The parent of this game object.
        """
        # Call the parent constructor.
        super().__init__(parent)
        # Register the object into the renderer.
        Engine.renderer.add_renderable(self)

    def __del__(self):
        """
        Class destructor.
        Removes the instance from the engine renderer.
        """
        Engine.renderer.remove_renderable(self)

    @abstractmethod
    def render(self, window):
        """
        Renders the gameobject on the screen.
        :param window: The window object to render onto.
        """
        pass

    def enable_rendering(self):
        """
        Enables rendering of this item.
        """
        # Attach to the renderer.
        Engine.renderer.add_renderable(self)
