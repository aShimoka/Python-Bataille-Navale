#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import the os module.
import os
# Import the sys module.
import sys

# Add the current directory to the python path.
sys.path.append(os.getcwd())

# Import the Battleships module.
import battleships
# Start the game
battleships.start()
