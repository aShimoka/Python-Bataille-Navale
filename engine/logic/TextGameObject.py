#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import the pygame module.
import pygame

# Import the rendered base class.
from engine.logic.Textured import TexturedGameObject
# Import the math module
import engine.logic.Math as math


class TextGameObject(TexturedGameObject):
    """
    Gets rendered as a text on the screen.

    Attributes:
        text    The text that is written (read-only)
        font    The name of the font used. (read-only)
    """

    # Dictionary of all the loaded fonts.
    __fonts = {}

    def __init__(self, parent, font_name, size, text, color=(0, 0, 0)):
        """
        Class constructor.
        Loads the font from the specified name and creates the texture.
        :param parent: The parent of this game_object.
        :param font_name: The name of the font to load.
        :param size: The size of the font.
        :param text: The text to render.
        :param color: The color of the rendered text.
        """
        super().__init__(parent, None, math.ZERO_VECTOR)
        # Load the font.
        self.font = TextGameObject.__load_font(font_name, size)
        self.text = text

        # Render the text.
        self.texture = self.font.render(self.text, True, color)
        self.size = math.Vector2(self.texture.get_width(), self.texture.get_height())

    @classmethod
    def __load_font(cls, font_name, size):
        """
        Loads the specified font.
        If it was already loaded, return the previous one instead or re-creating it.
        :param font_name: The name of the font to load.
        :param size: The size of the font to load.
        :return: The loaded Font object.
        """
        # If the font was already loaded.
        if (font_name, size) in cls.__fonts.keys():
            return cls.__fonts[(font_name, size)]
        else:
            # Load the font.
            font = pygame.font.Font("Data/Fonts/{}.ttf".format(font_name), size)

            # Save the font into the dictionary.
            cls.__fonts[(font_name, size)] = font

            # Return the font.
            return font
