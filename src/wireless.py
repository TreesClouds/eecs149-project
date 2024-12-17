import serial
from cli import args

BAUD_RATE = 9600

class Connection:
    # Check serial connection
    def __init__(self, port: str=''):
        self.port = port
        if not self.port:
            self.log('Empty port, creating dummy connection')
            return
        self.log('Trying to open serial connection...')
        self.serial = serial.Serial(port, BAUD_RATE)
        self.log('Serial connection established')

    def log(self, value):
        if args.debug:
            print(f'[{self.port}] {value}')

    def transmit_letter(self, letter: str):
        if not self.port:
            self.log('Dummy connection, aborting transmission')
            return
        buffer = bytes(letter, 'utf-8')
        self.log(f'Attempting to transmit byte(s) {buffer}')
        try:
            self.serial.write(buffer)
            self.log(f"Transmitted byte(s) {buffer}")
        except Exception as e:
            self.log(f"Transmission failed: {e}")
    
    def start_game(self):
        self.transmit_letter('s')

    def quit_game(self):
        self.transmit_letter('q')

    def close(self):
        self.log('Disconnecting...')
        self.serial.close()
        self.log('Successfully disconnected')
