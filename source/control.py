import serial
from serial import Serial
import json
import time
from source.timekeeper import Timestamps


class Command:
    def __init__(self, port, baud=115200):
        self.port = port
        self.baud = baud
        self.serial_timeout = 2
        self.ts = Timestamps()
        self.port = self.__get_connection()

    def __get_connection(self):
        try:
            port = Serial('COM3', self.baud, timeout=self.serial_timeout)
            startup = time.time()
            while True:
                port.write('{"node_id":0, "message":"None"}'.encode())
                line = port.readline().decode()
                print(line)
                if 'subs' in line.lower():
                    return port
                if time.time() - startup > 120:
                    print("TIMEOUT ERROR: Node Failed to Connect to Mesh")
                    return None
        except serial.SerialException:
            print('Windows COM port not found')
        try:
            return Serial('/dev/tty.usbserial-0001', self.baud, timeout=self.serial_timeout)
        except serial.SerialException:
            print('Mac COM port not found')
        print('No COM Ports Found')
        return None

    # def __get_status(self):
    #     if self.startup is True:
    #         start = time.time()
    #         while True:
    #             if self.receive_json()

    def send(self, node_id, message):
        msg = {'node_id': node_id, 'message': message}
        msg = json.dumps(msg).encode()
        self.port.write(msg)

    def receive_json(self, key=None, timeout=60):
        message = ''
        start = time.time()
        while True:
            if time.time() - start > timeout:
                return None
            try:
                message = self.port.readline()
                message = message.decode().split('*')[0]
                if '{' in message and '}' in message:
                    # print(message)
                    data = json.loads(message)
                    return data
            except Exception as e:
                print(e)
                continue

    def get_sensor_data(self, node_id):
        self.send(node_id, 'sensor_data')
        data = self.receive_json()
        if data is None:
            return data
        elif 'bus_voltage_V' not in data:
            data = self.receive_json()
        if data is None:
            return data
        data_with_timestamp = {'timestamp': self.ts.get_timestamp()}
        data_with_timestamp.update(data)
        return data_with_timestamp


def main():
    command = Command('COM3')
    command.send(2222631473, 'This is a test message')
    print(command.receive_json())


if __name__ == '__main__':
    main()


