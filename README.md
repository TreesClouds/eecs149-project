# Physical Pac-Man
# Requirements
Total setup time: ~90 minutes

This package has been tested on the following OS/architecture configurations:
- **Ubuntu 22.04.5 on amd64/x86_64 (recommended)**
	- To run Ubuntu on Windows, emulate it in VirtualBox.
	- To run Ubuntu on macOS (arm64):
		1. Download the [amd64 boot ISO image](https://releases.ubuntu.com/jammy/ubuntu-22.04.5-live-server-amd64.iso).
		2. Follow [this guide](https://techblog.shippio.io/how-to-run-an-ubuntu-22-04-vm-on-m1-m2-apple-silicon-9554adf4fda1) to download UTM but **don't virtualize with the arm64 image**. Instead, emulate with the amd64 image from step 1. Installing the server took ~30 minutes on my laptop, then installing ubuntu-desktop took another ~30 minutes.
- Ubuntu 22.04.5 on arm64 (worked for Shri's laptop but failed to install some tag detection packages on Jeffrey's laptop)
	1. Follow [this guide](https://techblog.shippio.io/how-to-run-an-ubuntu-22-04-vm-on-m1-m2-apple-silicon-9554adf4fda1) to download UTM and virtualize the VM.
- M1 MacBook Pro (GUI only)

These should both ship with Python 3.12.4.

# Installation
1. On a new Ubuntu machine, pip needs to be installed first:

		sudo apt install python3-pip
2. **(arm64 only)** Remove pyrealsense2 from requirements.txt since it requires x86.
3. Create a virtual environment with Python 3.11 (latest version supported by pyrealsense2) and install all packges with pip:

		python3.11 -m venv venv
		source venv/bin/activate
		pip install -r requirements.txt
4. **(arm64 only)** Build Intel Realsense from source (might not work):
	1. Install these dependencies if needed:

			sudo apt-get install cmake libssl-dev libx11-dev xorg-dev libglu1-mesa-dev libusb-1.0.0-dev libudev-dev libcurl4-openssl-dev
	2. Download Source Code zip from the [direct download link](https://github.com/IntelRealSense/librealsense/archive/refs/tags/v2.56.3.zip). If the direct link doesn't work, click the first "Source code (zip)" link in the [releases list](https://github.com/IntelRealSense/librealsense/releases/).
	3. Extract folder in any directory and enter it:

			cd librealsense-2.56.3
	4. Run these commands:

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
### GUI Only (no connected hardware)
1. Just run the driver script `main.py`:

		python3 src/main.py

### Integrating Wireless
1. Connect the master BT module to your computer via USB cable and select the device. Check that it shows up as `/dev/ttyUSB0` with `ls /dev/ttyUSB*`. If not, you may need to hold the USB cable there.
2. You may need to give yourself permissions to use the device:

		sudo chmod a+rw /dev/ttyUSB0

3. Add the `--wireless` or `-w` flag as a command-line argument:

		python3 src/main.py -w

### Integrating Camera
1. Connect the webcam to your computer via USB cable. TODO add more instructions for selecting the device?
2. Add the `--camera` or `-c` flag as a command-line argument:

		python3 src/main.py -c

## Gameplay
Use the arrow keys to move Pac-Man.
