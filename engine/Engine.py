#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import the sys module.
import sys
# Import the ini parser.
from configparser import ConfigParser
# Import pygame.
from pygame import time, mixer

# Import the GameManager base class.
from engine.logic.GameManager import GameManager
# Import the level manager class.
from engine.logic.LevelManager import LevelManager

# Import the GameObject base class.
from engine.logic.GameObject import GameObject

# Import the renderer class.
from engine.render.Renderer import Renderer
# Import the input handler class.
from engine.input.InputHandler import InputHandler


class Engine:
    """
    Game engine class.
    Handles all the engine events of the application.

    Attributes:
        renderer       The Renderer instance used by this engine.
        game_manager   The GameManager instance used for this game.
        input_handler  The input handler used by this engine.
        scene          The root object of the current scene.
    """

    # Renderer instance.
    renderer = None
    # GameManager instance
    game_manager = None
    # Input handler instance
    input_handler = InputHandler()
    # Scene instance.
    scene = GameObject()
    # Name of the level currently loaded.
    current_level = None

    FPS_CAP = 80
    # utility clock
    __engine_clock = time.Clock()
    # Time since the last frame.
    frame_time = 0

    # Configuration object.
    __config = ConfigParser()
    # Looping status.
    __is_looping = False
    # Next level to load.
    __loaded_level = None
    # All loaded sounds.
    __sounds = {}
    __silenced = False

    __config_files_buffer = ["Data/GameConfig.ini"]

    @classmethod
    def queue_config_file(cls, name):
        # mark the file at this location.
        cls.__config_files_buffer.append("Data/%s.ini" % name)

    @classmethod
    def set_game_silenced(cls, boolval=True):
        cls.__silenced = boolval

    @classmethod
    def initialize(cls, game_options=None):
        """
        Class initializer.
        Initializes the game engine singleton.
        """

        # - this way of parsing may be useful sometimes, but it is not standard
        # let's keep it but make it optionnal with "game_options" param

        if game_options is None:
            # - legacy parsing
            # Check if an additional configuration file was specified
            for arg_i in range(len(sys.argv)):
                # Check for the --config or -c flag.
                if sys.argv[arg_i] == "--config" or sys.argv[arg_i] == "-c":
                    # If there is an argument behind.
                    if arg_i + 1 < len(sys.argv):
                        # mark the file at this location.
                        cls.queue_config_file("Data/%s.ini" % sys.argv[arg_i + 1])

                # Check for the --silenced flag.
                if sys.argv[arg_i] == "--silenced":
                    cls.set_game_silenced()

        else:
            # - new way of parsing (done upfront, takes only one more config_file)
            cls.queue_config_file(game_options.config_file)
            if game_options.mute_sound:
                cls.set_game_silenced()

        # Try to load the configuration file(s).
        cls.__config.read(cls.__config_files_buffer)

        # Read the renderer info.
        render_info = cls.__config["Renderer"]
        # Create the renderer class.
        cls.renderer = Renderer((render_info.getint("window_width"), render_info.getint("window_height")))

        # Create the isLooping attribute.
        cls.__is_looping = True

    @classmethod
    def start(cls):
        """
        Runs the game engine instance.
        This method blocks until the game is exited.
        """
        # Call the setup method.
        cls.__setup()

        # Loop until the engine is stopped.
        cls.__engine_clock.tick()
        while cls.__is_looping:
            # Call the loop.
            cls.__loop()

        # Call the close method.
        cls.__close()

    @classmethod
    def request_exit(cls):
        """
        Requires the engine to exit on the next frame.
        """
        # Set the is looping flag to false.
        cls.__is_looping = False

    @classmethod
    def load_class(cls, class_name):
        """
        Dynamically loads the specified class.
        :param class_name: The class to load.
        """
        class_info = class_name.rsplit(".", 1)
        mod = __import__(class_info[0], fromlist=[class_info[1]])
        return getattr(mod, class_info[1])

    @classmethod
    def load_level(cls, level_name):
        """
        Loads a new level in the scene.
        :param level_name: The name of the level to load.
        """
        # Set the load_level flag.
        cls.__loaded_level = level_name

    @classmethod
    def play_sound(cls, sound_path, loops=0, fade=0):
        # If the game is silent, do nothing.
        if cls.__silenced:
            return
        # Load the sound.
        sound = None
        # If it was already loaded.
        if sound_path in cls.__sounds.keys():
            # Load the cached version.
            sound = cls.__sounds[sound_path]
        else:
            # Load the file.
            sound = mixer.Sound("Data/Sounds/{}.wav".format(sound_path))
            # Store the file in cache.
            cls.__sounds[sound_path] = sound

        # Play the sound.
        sound.play(loops, 0, fade)

    @classmethod
    def stop_sound(cls, sound_path):
        # If the game is silent, do nothing.
        if cls.__silenced:
            return
        # If it was already loaded.
        if sound_path in cls.__sounds.keys():
            # Load the cached version.
            sound = cls.__sounds[sound_path]
            # Stop the sound.
            sound.stop()
        else:
            print("The sound {} was not loaded.".format(sound_path))

    @classmethod
    def __setup(cls):
        """
        Prepares the game engine.
        Loads the game manager instance from the parameters.
        """
        # Get the manager instance string.
        manager = cls.__config["Level"]["game_manager"]

        # Load the class.
        cls.game_manager = cls.load_class(manager)(cls.__config)
        # Check if the game manager inherits GameManager.
        if not isinstance(cls.game_manager, GameManager):
            raise TypeError("Loaded game manager %s is not a GameManager class." %
                            cls.__config["Level"]["game_manager"])

        # Setup the manager.
        cls.game_manager.begin()

        # Load the default level.
        cls.__loaded_level = cls.__config["Level"]["first_level"]
        cls.__load_level()

    @classmethod
    def __loop(cls):
        # Call the object's tick method.
        cls.scene._tick_internal(cls.frame_time)
        # Call the manager's tick method.
        cls.current_level.tick(cls.frame_time)

        # Render the renderables.
        cls.renderer.render()

        # Compute the new frame time.
        cls.__engine_clock.tick(cls.FPS_CAP)
        cls.frame_time = cls.__engine_clock.get_time() / 1000

        # Handle the events.
        cls.input_handler.handle_events()

        # If there is a new level to load.
        if cls.__loaded_level is not None:
            # Load the new level.
            cls.__load_level()

    @classmethod
    def __close(cls):
        # Unload the level.
        cls.__unload_level()

    @classmethod
    def __unload_level(cls):
        """
        Unloads the current level.
        """
        # Tell the level that the level is over.
        if cls.current_level is not None:
            cls.current_level.end()
        # Tell the scene that the scene is being unloaded.
        cls.scene._end_internal()
        # Remove all rendered references.
        cls.renderer.clear()

    @classmethod
    def __load_level(cls):
        """
        Loads the level currently in the __loaded_level attribute.
        """
        # Unload the current level.
        cls.__unload_level()

        # Get the configuration of the new level.
        level_config = ConfigParser()
        level_config.read("Data/Levels/%s.ini" % cls.__loaded_level)
        level_manager = level_config["Manager"]["level_manager"]

        # Load the class.
        cls.current_level = cls.load_class(level_manager)(level_config)
        # Check if the game manager inherits GameManager.
        if not isinstance(cls.current_level, LevelManager):
            raise TypeError("Loaded game level %s is not a LevelManager class." %
                            level_config["Game"]["manager_class"])

        # Check if the level requires any size change.
        n_width  = cls.renderer.get_window_size()[0]
        n_height = cls.renderer.get_window_size()[1]
        if "Display" in level_config.keys():
            if "window_width" in level_config["Display"].keys():
                n_width = level_config["Display"].getint("window_width")
            if "window_height" in level_config["Display"].keys():
                n_height = level_config["Display"].getint("window_height")
        cls.renderer.resize_window(n_width, n_height)

        # Setup the manager.
        cls.__loaded_level = None
        cls.current_level.begin()
