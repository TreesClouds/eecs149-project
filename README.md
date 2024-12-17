# Physical Pac-Man
# Requirements
## OS/Architecture
This package has been tested on the following OS/architecture configurations:
- **Ubuntu 22.04.5 (recommended)**: If you don't already have an Ubuntu machine, you'll need to set up a VM, which takes ~90 minutes total.
	- To run Ubuntu on Windows, emulate it in VirtualBox.
	- To run Ubuntu on M1/M2 Apple Silicon: Follow [this guide](https://techblog.shippio.io/how-to-run-an-ubuntu-22-04-vm-on-m1-m2-apple-silicon-9554adf4fda1) to download UTM and create the VM. Note that the Boot ISO image link will install the latest Ubuntu version (>=24.04.1) but this should still work (untested). Installing the server took ~30 minutes on Jeffrey's laptop, then installing ubuntu-desktop took another ~30 minutes.
- M1 MacBook Pro (GUI only)

## Python/pip
All packages will be run with a virtual environment on Python 3.10 (latest version supported by pyrealsense2 for aarch64), so install the relevant packages if needed:

    sudo apt install python3.10 python3.10-venv python3-pip

# Installation
Create a virtual environment with Python 3.10 and install all packages:

	python3.10 -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt

# Running
## Board Digitization (only needed if you changed the board)
Each time you change the physical board, you'll also need to change the digitized board:

1. Open [board.txt](assets/board.txt) in a text editor.
2. Decide on the number of rows `R` (R ≥ 1) and columns `C` (C ≥ 1).
3. Change the grid according to our file format. By the end, the file should become a (2R + 1) x (2C + 1) ASCII grid.

	| Cell Type | Coordinates (0-indexed, r and c are integers) | Description | Character* |
	|---|---|---|---|
	| Corner | (2r, 2c) where 0 ≤ r ≤ R and 0 ≤ c ≤ C | Intersection of 2+ wall slots (always filled) | `+` |
	| Space | (2r + 1, 2c + 1) where 0 ≤ r < R and 0 ≤ c < C | The empty spaces in between wall slots (always empty) | (whitespace) |
	| Wall | All others | Slots corresponding to our modular walls. Can be either filled or empty, except for border walls which must always be filled. | `-` or `\|` |

	\* Technically, you can use any non-whitespace character(s) for filled ASCII grid cells. These characters are just recommended for human-readability.

## Startup
To only use the GUI (no integrated hardware), just run the driver script `main.py`:

    python3 src/main.py

To integrate additional hardware, add the respective flag(s).

## Integrating Camera
1. Connect the webcam to your computer via USB cable. TODO add more instructions for selecting the device?
2. Add one or both of these flags on the CLI:
	1. Pac-Man: `--pacman` or `-p`
	2. Ghost: `--ghost` or `-g`

## Integrating Wireless
1. Connect the master BT module to your computer via USB cable and select the device. Check that it shows up as `/dev/ttyUSB0` with `ls /dev/ttyUSB*`. If not, you may need to hold the USB cable there.
2. You may need to give yourself permissions to use the device(s) (this example is for port 0):

       sudo chmod a+rw /dev/ttyUSB0
3. Add one or both of these flags on the CLI:
	1. Pac-Man: `--Pacman=<pacman port>` or `-P=<pacman port>`
	2. Ghost: `--Ghost=<ghost port>` or `-G=<ghost port>`

Default ports you should use if using ports 0 and 1 for projector and camera: `/dev/ttyUSB2` (Pac-Man), `/dev/ttyUSB3` (Ghost)

## Integrating Projector
1. Connect a Pico LED projector to your computer via USB cable.
2. When running the GUI, it's highly recommended to go fullscreen to maximize the projector size.

## Debug Mode
1. Add the `--debug` or `-d` flag as a CLI argument.

## Gameplay
Use the arrow keys to move Pac-Man. **Note:** Walls are hidden outside of debug mode, making the game unplayable looking only at the screen. This is to hide misalignment of walls in the projected board.
