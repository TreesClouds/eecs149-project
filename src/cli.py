# CLI arguments
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('-p', '--pacman', action='store_true',
                    help='Integrate camera for Pac-Man')
parser.add_argument('-g', '--ghost', action='store_true',
                    help='Integrate camera for ghost')
parser.add_argument('-P', '--Pacman', action='store', type=str,
                    help='Integrate wireless for Pac-Man over the specified port')
parser.add_argument('-G', '--Ghost', action='store', type=str,
                    help='Integrate wireless for ghost over the specified port')
parser.add_argument('-d', '--debug', action='store_true',
                    help='Enable additional print statements and GUI elements')
args = parser.parse_args()

camera = args.pacman or args.ghost
wireless = args.Pacman or args.Ghost
