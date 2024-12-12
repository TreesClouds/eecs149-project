from cli import args

# GUI and startup
import gui

if args.wireless:
    PACMAN_PORT = '/dev/ttyUSB0'
    GHOST_PORT = '/dev/ttyUSB1'
    from wireless import Connection
    gui.pacman_connection = Connection(PACMAN_PORT)
    gui.pacman_connection = Connection(GHOST_PORT)

gui.start()
