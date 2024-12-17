from cli import args

import gui
from wireless import Connection
# If these arguments are empty, it just defaults to a dummy connection
gui.pacman.connection = Connection(args.Pacman)
gui.ghost.connection = Connection(args.Ghost)

gui.start()
