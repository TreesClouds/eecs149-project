import serial
from cli import args

BAUD_RATE = 9600

class Connection:
    # Check serial connection
    def __init__(self, port: str):
        self.port = port
        self.log('Trying to open serial connection...')
        self.serial = serial.Serial(port, BAUD_RATE)
        self.log('Serial connection established')

    def log(self, value):
        print(f'[{self.port}] {value}')

    def transmit_byte(self, buffer: bytes):
        if args.debug:
            self.log(f'Attempting to transmit byte(s) {buffer}')
        try:
            self.serial.write(buffer)
            if args.debug:
                self.log(f"Transmitted byte(s) {buffer}")
        except Exception as e:
            self.log(f"Transmission failed: {e}")

    def transmit_direction(self, direction: tuple[int, int]):
        if direction[0] < 0:
            buffer = b'l'
        elif direction[0] > 0:
            buffer = b'r'
        elif direction[1] < 0:
            buffer = b'u'
        elif direction[1] > 0:
            buffer = b'd'
        else:
            raise TypeError(f'Invalid direction {direction}')
        self.transmit_byte(buffer)
    
    def start_game(self):
        self.transmit_byte(b's')

    def quit_game(self):
        self.transmit_byte(b'q')

    def close(self):
        self.log('Disconnecting...')
        self.serial.close()
        self.log('Successfully disconnected')
