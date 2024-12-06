# Physical Pac-Man
# Requirements
This package has been tested on the following systems:
- **Ubuntu 22.04.5**
	- To run Ubuntu on Windows, emulate it in VirtualBox
	- To run Ubuntu on macOS (arm64):
		- Download the [Ubuntu 22.04.5 LTS disk image](https://cdimage.ubuntu.com/releases/22.04.3/release/)
		- Follow [this guide](https://techblog.shippio.io/how-to-run-an-ubuntu-22-04-vm-on-m1-m2-apple-silicon-9554adf4fda1) to download UTM and emulate
- M1 MacBook Pro (GUI only)

These should both ship with Python 3.12.4.

# Installation
1. On a new Ubuntu machine, pip needs to be installed first:

		sudo apt install python3-pip

2. Then you can use pip to install all required packages (besides the tag detection, which must be done in the next step):

		pip3 install -r requirements.txt

3. Set up the camera packages:
	1. Download Source Code zip from: https://github.com/IntelRealSense/librealsense/releases/
	2. Extract folder and cd into librealsense
	3. Run these commands:

			mkdir build
			cd build
			cmake ../ -DFORCE_RSUSB_BACKEND=ON -DBUILD_PYTHON_BINDINGS:bool=true -DPYTHON_EXECUTABLE=/usr/bin/python3 -DCMAKE_BUILD_TYPE=release -DBUILD_EXAMPLES=true -DBUILD_GRAPHICAL_EXAMPLES=true
			sudo make -j4
			sudo make install

# Running
## Board Digitization (only needed if you changed the board)
Each time you change the physical board, you'll also need to change the digitized board:

1. Open [board.txt](assets/board.txt) in a text editor.
2. Decide on the number of rows `R` (R ≥ 1) and columns `C` (C ≥ 1).
3. Change the grid according to our file format. By the end, the file should become a (2R + 1) x (2C + 1) grid of the characters `W` (wall), `V` (vertex), and `␣` (empty cell / absent wall).

TODO make file format table (jt)

All vertices (intersection of two or more walls) are represented by the character `V`. Vertices must **always** be present for alignment.

## Startup
1. Connect the master BT module to your computer via USB cable and select the device. Check that it shows up as `/dev/ttyUSB0` with `ls /dev/ttyUSB*`. If not, you may need to hold the USB cable there.
2. You may need to give yourself permissions to use the device:

		sudo chmod a+rw /dev/ttyUSB0

3. Then just run the driver script `main.py`:

		python3 src/main.py

## Gameplay
Use the arrow keys to move Pac-Man.
