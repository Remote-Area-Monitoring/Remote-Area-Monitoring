import serial
from serial import Serial
import json
import time
from source.util.timekeeper import Timestamps
import re


class Command:
    def __init__(self, port, baud=115200):
        self.port = port
        self.baud = baud
        self.serial_timeout = 2
        self.ts = Timestamps()
        self.port = self.__get_connection()
        self.network_connection = self.is_connected()

    def __get_connection(self):
        # TODO: Move first try block to a function to check connection for any OS
        print(self.port)
        try:
            return Serial(self.port, self.baud, timeout=self.serial_timeout)
        except serial.SerialException:
            print('Windows COM port not found')
        try:
            return Serial('/dev/tty.usbserial-0001', self.baud, timeout=self.serial_timeout)
        except serial.SerialException:
            print('Mac COM port not found')
        print('No COM Ports Found')
        return None

    def get_topology(self):
        self.port.write('{"node_id":0, "message":"None"}'.encode())
        data = self.receive_json()
        if data is None:
            return data
        elif 'nodeId' not in data:
            data = self.receive_json()
        if 'nodeId' not in data:
            return None
        print(data)
        return data

    def list_connected_nodes(self):
        topo = self.get_topology()
        # topo = {'nodeId': 2222635529, 'subs': [{'nodeId': 2222631473, 'subs': [{'nodeId': 2222817205}]}]}
        if topo is None:
            return None
        elif 'subs' not in topo:
            return None
        # nodes = list()
        topo.pop('nodeId')
        topo = json.dumps(topo)
        nodes = re.findall(r'\d+', topo)
        int_nodes = list()
        for node in nodes:
            try:
                int_nodes.append(int(node))
            except Exception as e:
                print('Invalid Node ID: ', node)
                print(e)
        return int_nodes

    def is_connected(self):
        if self.port is None:
            print('No com port found - not connected')
            return False
        startup = time.time()
        while True:
            topo = self.get_topology()
            if topo is not None:
                if 'subs' in topo:
                    return True
            if time.time() - startup > 120:
                print("TIMEOUT ERROR: Node Failed to Connect to Mesh")
                return False

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
    # command.send(4144723677, 'This is a test message')
    # print(command.receive_json())
    print(command.get_topology())


if __name__ == '__main__':
    main()


