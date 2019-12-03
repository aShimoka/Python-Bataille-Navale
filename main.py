#  Copyright © 2019
#  authored by Jean-Baptiste CAILLAUD et al.
#  contributor list on: https://github.com/yShimoka/python-bataille-navale

import battleships
import argparse


# - arg parsing setup
_parser = argparse.ArgumentParser(add_help=False)
dhost = 'localhost'
dport = 21337

# descriptions
argdesc = {
    '-c': 'specify the config file for playing the game (accepted values: solo / multiplayer)',

    '-h': "specify the server host (either IP or domain name) if you're the client. Using {} by default".format(dhost),
    '-p': 'specify how to connect to the server. Using port {} by default'.format(dport),

    '-s': 'start a multiplayer as the game server. Behaves as a client by default',

    '-m': 'turn off all sound & music',
    '-?': 'show this help message and exit'  # newbies exist
}

# required args
required = _parser.add_argument_group('required arguments')
required.add_argument('-c', '--config-file', help=argdesc['-c'], required=True)

# optional args
optional = _parser.add_argument_group('optional arguments')

_parser.add_argument('-h', '--host', help=argdesc['-h'], default=dhost)
_parser.add_argument('-p', '--port', help=argdesc['-p'], default=dport, type=int)

_parser.add_argument('-s', '--server', help=argdesc['-s'], action='store_true')

_parser.add_argument('-m', '--mute-sound', help=argdesc['-m'], action='store_true')
_parser.add_argument("-?", "--help", help=argdesc['-?'], action="help")

# parsing for real now
battleships.glvars.g_options = _parser.parse_args()
print(str(battleships.glvars.g_options))  # debug

# - start the game
battleships.start(battleships.glvars.g_options)
