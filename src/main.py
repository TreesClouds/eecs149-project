from cli import args

# GUI and startup
import gui

if args.camera:
    gui.use_camera = True

if args.wireless:
    import wireless
    gui.transmit_direction = wireless.transmit_direction
    gui.exit_callback = wireless.close

if args.debug:
    gui.enable_debug = True

gui.start()
