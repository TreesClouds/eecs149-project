from cli import args

# GUI and startup
import gui

if args.wireless:
    PACMAN_PORT = '/dev/ttyUSB2'
    GHOST_PORT = '/dev/ttyUSB3'
    from wireless import Connection
    gui.pacman.connection = Connection(PACMAN_PORT)
    gui.ghost.connection = Connection(GHOST_PORT)

gui.start()
