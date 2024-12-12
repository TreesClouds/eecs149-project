# CLI arguments
from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('-c', '--camera', action='store_true',
                    help='Integrate the camera')
parser.add_argument('-w', '--wireless', action='store_true',
                    help='Integrate the wireless Bluetooth modules')
parser.add_argument('-d', '--debug', action='store_true',
                    help='Enable additional print statements and GUI elements')
args = parser.parse_args()
