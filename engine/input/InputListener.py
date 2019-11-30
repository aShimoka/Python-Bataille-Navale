#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import the abstract objects.
from abc import ABC, abstractmethod


class InputListener(ABC):
    """
    Object that is used to listen to all the events of the application.
    """

    @abstractmethod
    def handle_input(self, event):
        """
        Handles the specified event.
        :param event: The event to handle.
        """
        pass
