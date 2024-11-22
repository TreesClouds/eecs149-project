# Physical Pac-Man
## Requirements
This package has been tested on the following systems:
- Ubuntu 22.04.5
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

## Running
```
sudo chmod a+rw /dev/ttyUSB0
```

```
python3 src/main.py
```
