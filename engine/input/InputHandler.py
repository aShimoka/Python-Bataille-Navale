#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import the pygame library.
import pygame
import pygame.locals


class InputHandler:
    """
    Pygame input handler class.
    Listens for events and passed them onto the InputListener instances.
    """

    def __init__(self):
        """
        Class constructor.
        Initializes the listener list.
        """
        # Create the list.
        self.__listeners = []

    def add_listener(self, listener):
        """
        Adds a new listener to the list.
        :param listener: The listener to add to the list.
        """
        self.__listeners.append(listener)

    def remove_listener(self, listener):
        """
        Removes the specified listener from the list.
        :param listener: The listener to remove from the list.
        """
        # Check if the listener is found in the list.
        if listener in self.__listeners:
            self.__listeners.remove(listener)

    def clear_listeners(self):
        """
        Clears all the listener from the list.
        """
        self.__listeners.clear()

    def handle_events(self):
        """
        Polls for all the events in the pygame queue.
        Passes them on to the listener instances.
        """
        # Loop until the queue is empty.
        for event in pygame.event.get():
            # Pass the event onto all the listeners.
            for listener in self.__listeners:
                listener.handle_input(event)
