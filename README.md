# Physical Pac-Man
# Requirements
## OS/Architecture
This package has been tested on the following OS/architecture configurations:
- **Ubuntu 22.04.5 (recommended)**: If you don't already have an Ubuntu maching, you'll need to set up a VM, which takes ~90 minutes total.
	- To run Ubuntu on Windows, emulate it in VirtualBox.
	- To run Ubuntu on M1/M2 Apple Silicon: Follow [this guide](https://techblog.shippio.io/how-to-run-an-ubuntu-22-04-vm-on-m1-m2-apple-silicon-9554adf4fda1) to download UTM and create the VM. Note that the Boot ISO image link will install the latest Ubuntu version (>=24.04.1) but this should still work (untested). Installing the server took ~30 minutes on Jeffrey's laptop, then installing ubuntu-desktop took another ~30 minutes.
- M1 MacBook Pro (GUI only)

## Python
Install Python 3.11 if you don't already have it.

# Installation
1. On a new Ubuntu machine, pip needs to be installed first:

		sudo apt install python3-pip
2. Create a virtual environment with Python 3.11 (latest version supported by pyrealsense2) and install all packges with pip:

		python3.11 -m venv venv
		source venv/bin/activate
		pip install -r requirements.txt

# Running
## Board Digitization (only needed if you changed the board)
Each time you change the physical board, you'll also need to change the digitized board:

1. Open [board.txt](assets/board.txt) in a text editor.
2. Decide on the number of rows `R` (R ≥ 1) and columns `C` (C ≥ 1).
3. Change the grid according to our file format. By the end, the file should become a (2R + 1) x (2C + 1) ASCII grid.

TODO make file format table (jt)

`W` (wall), `V` (vertex), and `␣` (empty cell / absent wall).

All vertices (intersection of two or more walls) are represented by the character `V`. Vertices must **always** be present for alignment.

## Startup
To only use the GUI (no integrated hardware), just run the driver script `main.py`:

		python3 src/main.py

To integrate additional hardware, add the respective flag(s).

## Integrating Wireless
1. Connect the master BT module to your computer via USB cable and select the device. Check that it shows up as `/dev/ttyUSB0` with `ls /dev/ttyUSB*`. If not, you may need to hold the USB cable there.
2. You may need to give yourself permissions to use the device:

		sudo chmod a+rw /dev/ttyUSB0
3. Add the `--wireless` or `-w` flag as a command-line argument:

		python3 src/main.py -w

## Integrating Camera
1. Connect the webcam to your computer via USB cable. TODO add more instructions for selecting the device?
2. Add the `--camera` or `-c` flag as a command-line argument:

		python3 src/main.py -c

## Gameplay
Use the arrow keys to move Pac-Man.
