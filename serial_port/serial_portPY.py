import os
import re
import sys
import serial


class SerialPort:
    port = ''
    instance = None
    baudrate = 115200
    opened = False
    timeout = 0.1

    def __init__(self, port, timeout):
        self.port = port
        self.timeout = timeout

    def __del__(self):
        self.close()

    def open(self):
        try:
            self.instance = serial.Serial(self.port, timeout=self.timeout, baudrate=self.baudrate)
            self.opened = True
            return True
        except Exception as e:
            print(e)
            print("Address for command or default address must be set!")
            pass
            return False

    def reopen(self):
        self.close()
        self.open()

    def set_timeout(self, to):
        self.timeout = to
        if self.opened:
            self.reopen()

    def set_baudrate(self, br):
        self.baudrate = br
        if self.opened:
            self.reopen()

    def close(self):
        if self.instance is not None:
            self.instance.close()
            self.instance = None
            self.opened = False
            return True
        return False

    def read(self, b2r):
        return self.instance.read(b2r)

    def write(self, data, it_is_binary=False):
        if it_is_binary == False:
            if self.instance is not None:
                self.instance.write(bytes(data, encoding='latin-1'))
        else:
            if self.instance is not None:
                self.instance.write(data)

    def flush(self):
        self.instance.flush()

    def reset_input_buffer(self):
        self.instance.reset_input_buffer()

    def __repr__(self):
        return "SerialPort attached to " + self.name

    def __str__(self):
        return self.name


def scanAvaiableSerialPorts():
    ports = []

    if sys.platform == 'win32':
        rawports = ['COM%s' % (i + 1) for i in range(256)]
        for port in rawports:
            try:
                ser = serial.Serial(port)
                ser.close()
                ports.append(port)
            except (OSError):
                pass

    elif sys.platform == 'darwin':
        ports = ['/dev/' + f for f in os.listdir('/dev/') if re.match(r'tty\.\w*', f)]

    elif 'linux' in sys.platform.lower():
        ports = ['/dev/' + f for f in os.listdir('/dev/') if re.match(r'ttyUSB\w*', f)]

    return ports
