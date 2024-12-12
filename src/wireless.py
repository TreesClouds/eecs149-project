import serial
from cli import args

# Check serial connection
print('Trying to open serial connection...')
try:
    bluetooth_serial = serial.Serial('/dev/ttyUSB0', 9600)
    print("Serial connection established.")
except Exception as e:
    print(f"Error opening serial port: {e}")
    exit()

def transmit(key):
    if args.debug:
        print(f"Attempting to transmit key {key}")
    try:
        bluetooth_serial.write(key)
        if args.debug:
            print(f"Transmitted key {key}")
    except Exception as e:
        print(f"Error: {e}")

def close():
    bluetooth_serial.close()
    print("Exiting...")
