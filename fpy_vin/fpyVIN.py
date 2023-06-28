import cmd
import os
import sys
import threading
import time
import termios
import serial
import serial_port.serial_portPY as serial_port
from filelock import FileLock
from csum.crc import crc16
from csum.xor import xor
from convertes.to_bytes import to_bytes
from convertes.to_int import to_int


BROADCAST_ADDRESS = 0xA0


class VINMachine:
    serial_port = None
    default_address = None
    test_cmd = None

    send_callback = None
    receive_callback = None
    mode = None

    VINR_OK = 0x00
    VINR_INVOPR = 0x01
    VINR_INVCRC = 0x02
    VINR_INVLNG = 0x03
    VINR_NOTSUP = 0x04
    VINR_INVPAR = 0x05
    VINR_INVNUM = 0x06
    VINR_ARRLIM = 0x07
    VINR_BUSY = 0x09
    VINR_NOTRESP = 0x10
    VINR_INVCRCR = 0x11
    VINR_INVXORR = 0x12

    codes_description = {
        VINR_OK: 'OK',
        VINR_INVOPR: 'Command not supported',
        VINR_INVCRC: 'Invalid crc on device receive',
        VINR_INVLNG: 'Command not supported',
        VINR_NOTSUP: 'Not supported frame',
        VINR_INVPAR: 'Invalid parameters',
        VINR_INVNUM: 'Invalid param number',
        VINR_ARRLIM: 'Array limit reached',
        VINR_BUSY: 'Device is busy',
        VINR_NOTRESP: 'Machine is not on network',
        VINR_INVCRCR: 'Invalid crc on host receive',
        VINR_INVXORR: 'Invalid xor on host receive'
    }

    def __init__(self, args, port=None, it_is_binary=False):
        if it_is_binary == False:
            self.args = args
            if port is not None:
                self.serial_port = serial_port.SerialPort(str(port), timeout=self.args.timeout)
                self.start()
        else:
            self.args = args
            if port is not None:
                self.serial_port = serial_port.SerialPort(port, timeout=100)
                self.start()

    def set_mode(self, mode):
        self.mode = 'xor' if mode.lower() == 'xor' else 'crc16'

    def set_callbacks(self, receive, send=None):
        self.send_callback = send
        self.receive_callback = receive

    def set_port(self, port):
        self.serial_port = serial_port.SerialPort(str(port), timeout=self.args.timeout)

    def start(self):
        return self.serial_port.open()

    def stop(self):
        return self.serial_port.close()

    def set_baudrate(self, baudrate):
        self.serial_port.set_baudrate(baudrate)

    def reset_input_buffer(self):
        if self.serial_port.opened:
            self.serial_port.reset_input_buffer()



    def compose_write(self, address, cmd, data=None):
        msg = ''
        msg += chr(address) + chr(cmd)
        msg += ''.join(data) if data is not None else ''
        if self.mode == 'xor':
            rx_xor = xor(msg)
            msg += chr(rx_xor)
        elif self.mode == 'crc16':
            rx_crc = to_bytes(crc16(msg))
            msg += chr(rx_crc[0])
            try:
                msg += chr(rx_crc[1])
            except:
                # так как crc16 занимает два байта, то в случае получения контрольной суммы занимающей всего один байт, добавляем в конце пустой байт
                msg += chr(0)
        for i in range(len(msg)):
            if msg[i] in ('\xFF', '\xFE'):
                msg = msg[:i + 1] + '\x00' + msg[i + 1:]
        return str('\xFE') + str('\xFE') + msg + str('\xFF') + str('\xFF')

    def make_binary_package(self, address, bin_command, data=None):
        bin_package = bytearray()
        bin_package.append(0xFE)
        bin_package.append(0xFE)
        # адресc устройства в HEX
        bin_package.append(address)
        # бинарная команда для устройства
        bin_package.append(bin_command)
        # если data пуст, то сразу прибавляем xor или crc16
        if data == None:
            if self.mode == 'xor':
                rx_xor = xor(bin_package)
                bin_package.append(rx_xor)
            else:
                pass
        # если data не пуст, то добавляем байты по очереди в массив и подсчитываем контрольную сумму xor или crc16
        else:
            for i in data:
                bin_package.append(i)
            if self.mode == 'xor':
                rx_xor = xor(bin_package)
                bin_package.append(rx_xor)
            else:
                pass
        bin_package.append(0xFF)
        bin_package.append(0xFF)
        return bin_package

    def command_send(self, address, cmd, bin_command=None, data=None, it_is_binary=False):
        if not self.serial_port.opened:
            print('No connection set on device port')
            return None
        try:
            self.serial_port.flush()
        except termios.error:
            print('I/O Error. device has been disconected.')
            return None
        if it_is_binary == False:
            msg = self.compose_write(address, cmd, data)
            if self.send_callback is not None:
                self.send_callback(msg)
            return self.serial_port.write(msg)
        else:
            msg = self.make_binary_package(address, bin_command, data)
            if self.send_callback is not None:
                self.send_callback(msg)
            return self.serial_port.write(msg, it_is_binary)

    def set_timeout(self, to):
        self.serial_port.set_timeout(to)

    def set_default_address(self, addr):
        self.default_address = addr

    def set_test_command(self, test_cmd):
        self.test_cmd = test_cmd

    def get_error_info(self, c):
        return self.codes_description[c] if c in self.codes_description.keys() else 'Unknown error'

    def reply_read(self):
        got_ff, got_fe, got_start, got_frame = False, False, False, False
        rx_data, raw_data_accumulator = '', ''

        while not got_frame:
            if not self.serial_port.opened:
                self.serial_port.open()
                return [None, '']
            try:
                data = self.serial_port.read(1).decode('latin-1')
            except serial.serialutil.SerialException:
                if len(serial_port.scanAvaiableSerialPorts()) != 0:
                    port = sorted(serial_port.scanAvaiableSerialPorts())[0]
                    self.serial_port = serial_port.SerialPort(str(port), timeout=self.args.timeout)
                    self.set_baudrate(self.args.baudrate)
                    self.set_default_address(self.args.address)
                    self.serial_port.open()
                    print('device is connected on port {}'.format(port))
                return [None, '']
            raw_data_accumulator += data
            if data is None or data == '':
                return [self.VINR_NOTRESP, None]
            for c in data:
                b = ord(c)
                if b == 0xFE:
                    if got_fe:
                        if got_start:
                            rx_data = ''
                        got_start = True
                        got_fe = False
                    else:
                        got_fe = True
                elif b == 0xFF:
                    if got_ff:
                        got_frame = True
                        break
                    else:
                        got_ff = True
                else:
                    if got_start:
                        if got_fe:
                            got_fe = False
                            b = 0xFE
                        if got_ff:
                            got_ff = False
                            b = 0xFF
                        rx_data += chr(b)
        if self.mode == 'xor':
            rx_xor = ord(rx_data[-1])
            rx_data = rx_data[:-1]
            if rx_xor != xor(rx_data):
                return [self.VINR_INVXORR, None]
        elif self.mode == 'crc16':
            rx_crc = to_int(rx_data[-2:])
            rx_data = rx_data[:-2]
            if rx_crc != crc16(rx_data):
                return [self.VINR_INVCRCR, None]
        return_code = rx_data[1]
        rx_data = rx_data[2:-1]
        if self.receive_callback is not None:
            self.receive_callback(raw_data_accumulator)
        return [return_code, rx_data]

    def read_response_bin_command(self):
        massive_byte_from_serial = []
        counter_ff = 0
        while True:
            byte_from_serial = self.serial_port.read(1)
            if byte_from_serial == b'\xfe':
                continue
            elif byte_from_serial == b'\xff':
                counter_ff += 1
                if counter_ff == 2:
                    break
            else:
                massive_byte_from_serial.append(byte_from_serial)
        if self.mode == 'xor':
            # удаляем контрольную сумму из конца массива и сохраняем в переменную, чтобы потом сравнить
            xor_from_device = massive_byte_from_serial.pop(len(massive_byte_from_serial) - 1)
            calculated_xor = 0
            for i in massive_byte_from_serial:
                calculated_xor ^= ord(i)
            if ord(xor_from_device) != calculated_xor:
                print('!!XOR ERR!!')
                return 'XorErr'
            else:
                # проверяем код ответа
                response_code = massive_byte_from_serial.pop(1)
                return_data = None
                if response_code == b'\x00':
                    return_data = massive_byte_from_serial[1:]
                else:
                    return_data = response_code
                return return_data

    def command_a(self, address, cmd, data=None, it_is_binary=False, bin_command=None):
        if address == None:
            address = self.default_address
        else:
            pass
        if address is None:
            raise Exception("Address for command or default address must be set!")
        self.reset_input_buffer()
        self.command_send(address=address, cmd=cmd, data=data, it_is_binary=it_is_binary, bin_command=bin_command)
        if it_is_binary == False:
            if address == BROADCAST_ADDRESS:
                return self.command_c(self, address, cmd, data)
            return self.reply_read()
        else:
            return self.read_response_bin_command()

    def command_c(self, address, cmd, data=None):
        address = self.default_address if address is None else None
        if address is None:
            raise Exception("Address for command or default address must be set!")
        self.reset_input_buffer()
        self.command_send(address, cmd, data)
        return [self.VINR_OK, None]

    def cli_command(self, address, data):
        address = self.default_address if address is None else None
        if address is None:
            raise Exception("Address for command or default address must be set!")
        command_part_length = 32
        space_pointer = 0
        while space_pointer < data.__len__() - 1 and data[space_pointer] != ' ':
            space_pointer += 1
        command_part = list(data[:space_pointer])
        argument_part = []
        if space_pointer != data.__len__() - 1:
            argument_part = list(data[space_pointer + 1:])
        else:
            command_part.extend(data[space_pointer])
        if command_part.__len__() < command_part_length:
            command_part.extend(['\x00'] * (command_part_length - command_part.__len__()))
        self.reset_input_buffer()
        self.command_send(address=address, cmd=0x1f, data=command_part + argument_part)
        return self.reply_read()

    def console_config(self, no_print=False):

        if self.serial_port:
            self.stop()
        if not no_print:
            print('set port {}'.format(self.args.port))
        self.set_port(self.args.port)
        if not no_print:
            print('set baudrate {}'.format(self.args.baudrate))
        self.set_baudrate(self.args.baudrate)
        if not no_print:
            print('set default_address 0x{:02X}'.format(self.args.address))
        self.set_default_address(self.args.address)
        self.set_test_command(self.args.test)
        self.start()


class VINCmd(object):
    def __init__(self, machine, cmd_code, up_struct=None, down_struct=None):
        self.machine = machine
        self.code = cmd_code
        self.up_struct = up_struct
        self.down_struct = down_struct

    def before_send(self):
        return True

    def after_reply(self, reply_code, data):
        return True

    def engage(self):
        self.before_send()
        if self.up_struct is None:
            reply_code, reply_msg = self.machine.command_a(None, self.code)
        else:
            reply_code, reply_msg = self.machine.command_a(None, self.code, self.up_struct.get_ptr())
        if reply_code == self.machine.VINR_OK:
            if self.down_struct is not None:
                self.down_struct.update(reply_msg)
        self.after_reply(reply_code, reply_msg)
        return reply_code, reply_msg


class Interface(cmd.Cmd):
    def __init__(self, args=None):
        cmd.Cmd.__init__(self)
        self.args = args
        self.intro = 'CLI started. Type help or ? to list commands.\n'
        self.prompt = '(cli): '
        self.machine = VINMachine(self.args)
        self.default_address = 0x00
        self.is_cmd_repeating = False
        self.prev_cmd = None
        self.lock = FileLock("/run/lock/fpyVIN.lock")
        self.lock.release(force=True)

    def cmdloop(self):
        try:
            super().cmdloop()
        except KeyboardInterrupt:
            self.do_exit()
            sys.exit()

    def set_mode(self, mode):
        self.machine.set_mode(mode)

        # ----- Interface setup and send command from cli-----

    def send_test_cmd(self):
        self.do_config(no_print=True)
        self.default(self.args.test)
        self.do_exit(no_output=True)
        sys.exit()

    def preloop(self):
        if self.args.test:
            self.send_test_cmd()
        else:
            self.do_config()

    def emptyline(self):
        if not self.is_cmd_repeating:
            self.default('')
        else:
            self.is_cmd_repeating = False

        # ----- Basic commands -----

    def default(self, line):
        try:
            with self.lock:
                print(self.machine.cli_command(None, line)[1])
        except UnicodeEncodeError:
            print('Only ASCII symbols are permitted')
        self.prev_cmd = line

    def do_exit(self, no_output=False):
        '''Application terminating command'''
        self.is_cmd_repeating = False
        if not no_output: print('Exiting from CLI...')
        if self.machine.serial_port.opened:
            self.machine.serial_port.close()
        return True

    def do_cls(self, arg):
        '''Clear screen'''
        os.system('cls' if os.name == 'nt' else 'clear')

    def do_config(self, no_print=False):
        self.machine.console_config(no_print)

    def do_repeat(self, arg='repeat 1'):
        '''
        Repeates last non-zero command with given (as argument) interval in seconds;
                        default value is 1 second
        '''
        if self.prev_cmd:
            self.is_cmd_repeating = True
            def repeating_function():
                try:
                    sleeptime = float(arg.split(' ')[0])
                    print(sleeptime)
                except ValueError:
                    print("Time of periodic sending wasn't recognized; set it to default value (1s)")
                    sleeptime = 1
                while self.is_cmd_repeating:
                    with self.lock:
                        self.do_cls(None)
                        print('"{}" sent'.format(self.prev_cmd))
                        self.onecmd(self.prev_cmd)
                    time.sleep(sleeptime)
            repeating_thread = threading.Thread(target=repeating_function)
            repeating_thread.daemon = True
            repeating_thread.start()
        else:
            print("CLI-commands for serial device weren't sent yet")
