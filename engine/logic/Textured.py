#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import the pygame utility.
from copy import copy

import pygame

# Import the ZERO vector.
from engine.logic.Math import ZERO_VECTOR
# Import the rendered game object class.
from engine.logic.RenderedGameObject import RenderedGameObject
import engine


class TexturedGameObject(RenderedGameObject):
    """
    Game object that is rendered with a texture.

    Attributes:
        texture     The texture of this object.
        size        The size of the rendered image.
    """

    def __init__(self, parent, texture_path, size):
        """
        Class constructor.
        Creates a new textured game object and load the texture.
        :param parent: The parent of this game object.
        :param texture_path: The path to the texture to load.
        :param size: The size of the image to draw on the screen.
        """
        # Call the parent constructor.
        super().__init__(parent)

        # Try to load the texture.
        if texture_path is not None:
            self.texture = pygame.image.load("Data/Textures/{}.bmp".format(texture_path)).convert()
            self.texture.set_colorkey(self.texture.get_at((1, 1)))
            self.rendered = self.texture.copy()
        else:
            self.texture = None
            self.rendered = None

        # Save the size.
        self.size = copy(size)

    def render(self, window):
        """
        Renders the texture on the screen.
        Uses the world matrix to generate the origin and extent of the rendering target.
        :param window: The window to render the texture onto.
        """
        # If the rendered texture is a none.
        if self.rendered is None:
            # If the texture is set.
            if self.texture is not None:
                self.rendered = self.texture.copy()
            else:
                raise ValueError("There is no texture to render !")

        # Get the origin and extent points of the image.
        origin = self.transform.get_world_position()
        # Check if the scale has changed.
        scale = (self.size * self.transform.get_world_scale()).tuple(True)
        if scale[0] != self.texture.get_width() or scale[1] != self.texture.get_height():
            self.rendered = pygame.transform.scale(self.texture, scale)

        # Blit the image.
        window.blit(self.rendered, pygame.Rect(origin.tuple(), ZERO_VECTOR.tuple()))
