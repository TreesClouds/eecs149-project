import gui
import wireless

gui.movement_callback = wireless.on_press

def exit_callback():
	wireless.close()
	exit()
gui.exit_callback = exit_callback

gui.start()
