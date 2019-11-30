#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import the pygame library.
from copy import copy

import pygame

# Import the rendered GameObject.
from engine.logic.RenderedGameObject import RenderedGameObject

# Import the math tools.
from engine.logic.Math import ZERO_VECTOR, UNIT_VECTOR, Vector2


class LineGameObject(RenderedGameObject):
    """
    Line primitive.
    Gets rendered as a simple line on the screen.

    Attributes:
        origin    The position of the beginning of the line.
        extent    The position of the end of the line.
        width     The width of the line.
        color     The color of the line.
    """

    def __init__(self, parent, origin=ZERO_VECTOR, extent=ZERO_VECTOR, width=1, color=(0, 0, 0)):
        """
        Class constructor.
        Creates a new instance and defines its values.

        :param origin The origin of the line.
        :param extent The extent of the line.
        :param width The width of the rendered line.
        :param color The color of the rendered line.
        """
        # Call the parent constructor.
        super().__init__(parent)
        # Define the class attributes.
        self.transform.position = copy(origin)
        self.extent = copy(extent)
        self.width = width
        self.color = color

    def render(self, window):
        """
        Renders the line on the screen.

        :param window The screen to render onto.
        """
        pygame.draw.line(
            window,
            self.color,
            self.transform.get_world_position().tuple(),
            (self.transform.get_world_position() + self.extent).tuple(),
            self.width
        )


class RectGameObject(RenderedGameObject):
    """
    Rectangle primitive.
    Gets rendered as a rectangle on the screen.

    Attributes:
        origin      The position of the rectangle's top-left corner.
        extent      The position of the rectangle's bottom-right corner.
        width       The width of the rectangle's line.
        inner_color The color of the rectangle's contents.
        outer_color The color of the line outline. If width is 0, does nothing.
    """

    def __init__(self, parent, extent=ZERO_VECTOR,
                 width=0, inner_color=(0, 0, 0), outer_color=(0, 0, 0)):
        """
        Class constructor.
        Creates a new instance and defines its values.

        :param extent The extent of the rectangle.
        :param width The width of the outline.
        :param inner_color The color of the inside of the rectangle.
        :param outer_color The color of the outline of the rectangle.
        """
        super().__init__(parent)
        # Define the class attributes.
        self.extent = extent
        self.width = width
        self.inner_color = inner_color
        self.outer_color = outer_color

    def render(self, window):
        """
        Renders the rect on the screen.

        :param window The screen to render onto.
        """
        # Draw the contents of the rectangle.
        pygame.draw.rect(
            window,
            self.inner_color,
            pygame.Rect(self.transform.get_world_position().tuple(), self.extent.tuple())
        )

        # If an outline is to be drawn.
        if self.width > 0:
            o = self.transform.get_world_position()
            e = self.extent
            # Compute the points.
            points = [
                o.tuple(),
                Vector2(o.x + e.x, o.y).tuple(),
                (o + e).tuple(),
                Vector2(o.x, o.y + e.y).tuple(),
            ]
            # Draw the outline.
            pygame.draw.lines(window, self.outer_color, True, points, self.width)
