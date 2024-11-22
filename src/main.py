import src.gui as gui
import src.wireless as wireless

gui.movement_callback = wireless.on_press

def exit_callback():
	wireless.close()
	exit()
gui.exit_callback = exit_callback
