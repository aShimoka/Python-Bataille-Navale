#  Copyright © 2019 CAILLAUD Jean-Baptiste.

# Import the socket class.
import socket
# Import the system objects.
import sys
import json
# Import the engine.
import engine

# Import the player base class.
from battleships.players.Player import Player


class RemotePlayer(Player):
    """
    This class is used to represent the other player over the network.
    """

    def __init__(self):
        """
        Class constructor.
        Prepares the socket connection.
        """
        # Call the parent constructor.
        super().__init__()

        # Create the socket.
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Check the type of the game.
        self.client = None
        self.game_type = 'client'
        self.game_port = 61888
        self.game_addr = '127.0.0.1'
        for i in range(len(sys.argv)):
            # If the game is in server mode.
            if sys.argv[i] == "--server":
                self.game_type = 'server'
            elif sys.argv[i] == "--client":
                self.game_type = 'client'
            elif sys.argv[i] == "--port" and len(sys.argv) > i:
                self.game_port = int(sys.argv[i + 1])
            elif sys.argv[i] == "--address" and len(sys.argv) > i:
                self.game_addr = sys.argv[i + 1]

        # Paste those parameters.
        if self.game_type == 'server':
            self.socket.bind((self.game_addr, self.game_port))
            self.socket.listen(1)


    def __del__(self):
        if self.client is not None:
            self.client.close()

    def pre_game_prepare(self):
        """
        Prepares the socket before the game.
        """
        # If the socket is in server mode.
        if self.game_type == 'server':
            # Accept client connections.
            self.client = self.socket.accept()[0]
            return True
        else:
            # Try to connect to the server.
            try:
                self.socket.connect((self.game_addr, self.game_port))
                self.client = self.socket
                return True
            except ConnectionRefusedError:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("Connection refused.")
                return False

    def start_game(self):
        pass

    def start_turn(self):
        pass

    def end_turn(self):
        pass

    def request_shot(self):
        # Wait for the client to send their shot info.
        response = json.loads(self.client.recv(1024).decode("UTF-8"))
        if response["type"] == "shot":
            # Parse the shot info.
            self.fire(engine.math.Vector2(
                int(response["attributes"]["x"]),
                int(response["attributes"]["y"]))
            )
        else:
            raise ValueError("Received a wrong message.")

    def request_hit(self, at: engine.math.Vector2):
        # Send the hit info to the client.
        data = {"type": "shot", "attributes": {"x": at.x, "y": at.y}}
        self.client.send(json.dumps(data).encode("UTF-8"))

        # Wait for the client to send their shot info.
        response = json.loads(self.client.recv(1024).decode("UTF-8"))
        if response["type"] == "hit":
            # Parse the shot info.
            self.hit(engine.math.Vector2(
                int(response["attributes"]["x"]),
                int(response["attributes"]["y"])
            ), int(response["attributes"]["hit"]))
        else:
            raise ValueError("Received a wrong message.")

    def show_hit(self, at: engine.math.Vector2, hit_type: int):
        # Send the hit info to the client.
        data = {"type": "hit", "attributes": {"x": at.x, "y": at.y, "hit": hit_type}}
        self.client.send(json.dumps(data).encode("UTF-8"))

    def await_opponent_shot(self):
        pass
