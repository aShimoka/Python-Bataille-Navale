#  Copyright © 2019 CAILLAUD Jean-Baptiste.
import pygame
import pygame.locals


class Renderer:
    """
    Rendering engine used to display on a window.
    Creates a new window on instantiation.
    """
    def __init__(self, size):
        """
        Class constructor.
        Initializes the attributes of the renderer.

        :param size: The size of the new window to create.
        """
        # Initialize the renderables list.
        self.__renderables = []

        # Initialize pygame.
        pygame.init()
        # Create the window.
        pygame.display.init()
        self.__window = pygame.display.set_mode(size)
        self.__world = pygame.Surface(size, pygame.SRCALPHA, 32)
        self.__window_size = size

        # Initialize font management.
        pygame.font.init()
        pygame.mixer.init()

    def __del__(self):
        """
        Class destructor.
        De-initializes pygame and clears the display.
        """
        # Delete the window.
        pygame.display.quit()

        # Quit pygame.
        pygame.font.quit()
        pygame.mixer.quit()
        pygame.quit()

    def add_renderable(self, renderable):
        """
        Adds a new renderable item to the rendered list.
        :param renderable: The renderable item to add to the list.
        """
        self.__renderables.append(renderable)

    def remove_renderable(self, renderable):
        """
        Removes the specified renderable item from the list.
        :param renderable: The item to remove from the rendered list.
        """
        # Check if the item exists in the list.
        if renderable in self.__renderables:
            # Remove the item from the list.
            self.__renderables.remove(renderable)

    def clear(self):
        """
        Clears the entire renderer.
        """
        self.__renderables.clear()

    def get_world_surface(self):
        return self.__world

    def render(self):
        """
        Renders all the renderable instances to the screen.
        """
        # Fill the window with black.
        self.__world.fill((0, 0, 0, 255))

        # Render all the renderable instances.
        for renderable in self.__renderables:
            if renderable.is_visible():
                renderable.render(self.__world)

        # Flip the display.
        self.__window.blit(self.__world, pygame.Rect((0, 0), self.get_window_size()))
        pygame.display.flip()

    def get_window_size(self):
        """
        :return: The dimensions of the window.
        """
        return self.__window_size

    def resize_window(self, width, height):
        """
        Changes the size of the screen.
        :param width: The new width of the window.
        :param height: The new height of the window.
        """
        # Check if the size is the same.
        if self.__window_size != (width, height):
            self.__window_size = (width, height)
            self.__window = pygame.display.set_mode(self.__window_size)
            self.__world = pygame.Surface(self.__window_size, pygame.SRCALPHA, 32)
