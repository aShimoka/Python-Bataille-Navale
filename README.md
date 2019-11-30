
<p>
    <a target="_blank" href="https://app.gitkraken.com/glo/board/XZsYWKr2-gAPzpd7" alt="Issue Tracker">
        <img src="https://img.shields.io/badge/tracker-GitKraken%20Glo-blue" />
    </a>
</p>

# Battleships - Python
_This is a Python3 project made to recreate the game "Battleships" with networked multiplayer capabilities._

## Running the project.
To run the project, simply clone this repository and start the [main.py](main.py) file.

## Arguments
__REQUIRED:__ `--config (or -c) [CONFIG_FILE_NAME]`
Selects the configuration of the game. Use `MultiplayerConfig` for the default multiplayer mode or `SingleplayerConfig` 
for a single player game. (**NOTE: The singleplayer is *not* working for now**)

`--server`
Launches the instance of the game in server mode.

`--client`
Launches the instance of the game in client mode.

`--port [PORT]`
The port to use for multiplayer sessions.

`--address [ADDRESS]` The listening address used by the server or the address to connect to for the client.

`--silenced` Turns all sounds off.
