import serial
from pynput import keyboard

# Check serial connection
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
        
        if key == keyboard.Key.up:
            bluetooth_serial.write(b'u')
            print("Up arrow key sent")
        elif key == keyboard.Key.down:
            bluetooth_serial.write(b'b')
            print("Down arrow key sent")
        elif key == keyboard.Key.left:
            bluetooth_serial.write(b'l')
            print("Left arrow key sent")
        elif key == keyboard.Key.right:
            bluetooth_serial.write(b'r')
            print("Right arrow key sent")
    except Exception as e:
        print(f"Error: {e}")

def on_release(key):
    if key == keyboard.Key.esc:
        bluetooth_serial.close()
        print("Exiting...")
        return False

print("Starting listener...")
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()