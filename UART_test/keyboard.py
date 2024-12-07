import serial
from pynput import keyboard

# Establish a serial connection (adjust '/dev/ttyUSB0' and baud rate as needed)
bluetooth_serial = serial.Serial('/dev/ttyUSB0', 9600)

def on_press(key):
    try:
        # Check for arrow keys and send specific bytes or strings over serial
        if key == keyboard.Key.up:
            bluetooth_serial.write(b'u')
            print("Up arrow key sent")
        elif key == keyboard.Key.down:
            bluetooth_serial.write(b'd')
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
    # Stop listener on 'Esc' key press
    if key == keyboard.Key.esc:
        bluetooth_serial.close()  # Close the serial connection when exiting
        print("Exiting...")
        return False

# Start the keyboard listener
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()