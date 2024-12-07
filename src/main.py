# CLI arguments
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-c', '--camera', action='store_true',
                    help='Integrate the camera')
parser.add_argument('-w', '--wireless', action='store_true',
                    help='Integrate the wireless Bluetooth modules')
args = parser.parse_args()

# GUI and startup
import gui

if args.camera:
    gui.use_camera = True

if args.wireless:
    import wireless
    gui.movement_callback = wireless.on_press
    gui.exit_callback = wireless.close

gui.start()
