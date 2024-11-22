# Physical Pac-Man
# Requirements
## Setup
This package has been tested on the following systems:
- Ubuntu 22.04.5
	- To run Ubuntu on Windows, emulate it in VirtualBox
	- To run Ubuntu on macOS (arm64):
		- Download the [Ubuntu 22.04.5 LTS disk image](https://cdimage.ubuntu.com/releases/22.04.3/release/)
		- Follow [this guide](https://techblog.shippio.io/how-to-run-an-ubuntu-22-04-vm-on-m1-m2-apple-silicon-9554adf4fda1) to set up UTM
- M1 MacBook Pro (GUI only)

These should both ship with Python 3.12.4.

## Installation
On a new Ubuntu machine, pip needs to be installed first:
```
sudo apt install python3-pip
```

Then you can use pip to install all required packages:
```
pip3 install -r requirements.txt
```

# Running
Connect the master BT module to your computer via USB cable and select the device. Check that it shows up as `/dev/ttyUSB0` with `ls /dev/ttyUSB*`. If not, you may need to hold the USB cable there.

You may need to give yourself permissions to use the device:
```
sudo chmod a+rw /dev/ttyUSB0
```

Then just run the driver script `main.py`:
```
python3 src/main.py
```

# Gameplay Instructions
Use the arrow keys to move Pac-Man.
