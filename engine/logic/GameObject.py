#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import the transform class.
from engine.logic.Transform import Transform


# Defines the different mode of ticking.
TICKMODE_CHILDREN_FIRST = 1
TICKMODE_PARENT_FIRST = 2


class GameObject:
    """
    GameObject base class.
    All objects in the engine should be GameObject instances.

    Attributes:
        transform     Matrix representing the state of this object.
        tick_mode     The ticking mode of this object. Defaults to PARENT_FIRST.
    """

    def __init__(self, parent=None):
        """
        Class constructor.
        Initializes the game object instance.
        """
        self.transform = Transform(parent.transform if isinstance(parent, GameObject) else None, gameobject=self)
        self.tick_mode = TICKMODE_PARENT_FIRST
        # Flag set if the object is persistent.
        self.persistent = False
        # Flag set if the gameobject is visible.
        self.visible = True

    def is_visible(self):
        """
        Enables rendering of this item.
        """
        # Return the rendering state.
        return self.visible and (
            self.transform.parent.gameobject.is_visible() if self.transform.parent is not None else True
        )

    def begin(self):
        """
        Called when the engine instanced this object in the scene.
        """
        pass

    def tick(self, dt):
        """
        Called on each of the engine's tick.
        """
        pass

    def end(self):
        """
        Called before the object is deleted from the scene.
        """
        pass

    def _tick_internal(self, dt):
        """
        Tick method called internally for the scene tree.
        Used to determine the ticking mode of this object.
        """
        # If the children should get the tick event first.
        if self.tick_mode == TICKMODE_CHILDREN_FIRST:
            # Loop through the children.
            for child in self.transform.children:
                # Call the internal method.
                child.gameobject._tick_internal(dt)

            # Call the parent tick.
            self.tick(dt)
        else:
            # Call the parent tick.
            self.tick(dt)

            # Loop through the children.
            for child in self.transform.children:
                # Call the internal method.
                child.gameobject._tick_internal(dt)

    def _end_internal(self):
        """
        End method called internally for the scene tree.
        """
        # Loop through the children.
        for child in self.transform.children:
            # Call the internal method.
            child.gameobject._end_internal()

        # Delete all the children, if necessary.
        for child in self.transform.children:
            self.transform.children.remove(child)

        # Call the parent end.
        self.end()
