import pygame
import serial

# Check serial connection
print('Trying to open serial connection...')
try:
    bluetooth_serial = serial.Serial('/dev/ttyUSB0', 9600)
    print("Serial connection established.")
except Exception as e:
    print(f"Error opening serial port: {e}")
    exit()

def on_press(key):
    try:
        # Debug print for each key press
        print(f"Key pressed: {key}")
        match key:
            case pygame.K_UP:
                bluetooth_serial.write(b'u')
                print("Up arrow key sent")
            case pygame.K_DOWN:
                bluetooth_serial.write(b'd')
                print("Down arrow key sent")
            case pygame.K_LEFT:
                bluetooth_serial.write(b'l')
                print("Left arrow key sent")
            case pygame.K_RIGHT:
                bluetooth_serial.write(b'r')
                print("Right arrow key sent")
    except Exception as e:
        print(f"Error: {e}")

def close():
    bluetooth_serial.close()
    print("Exiting...")
