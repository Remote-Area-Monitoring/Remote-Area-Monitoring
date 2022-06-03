from source.util.database import Database
from source.util.settings import Settings
from source.network.mesh import Mesh
from source.util.timekeeper import Timestamps
from serial import Serial
import serial
import json
import source.util.shared_config as cfg



class Comm:
    def __init__(self):
        cfg.initialize()
        self.ts = Timestamps()
        self.config = Settings('general.config')
        self.com_port = self.config.get_setting('mesh_network', 'port')
        self.baud = self.config.get_int_setting('mesh_network', 'baud_rate')
        self.serial_timeout = self.config.get_int_setting('mesh_network', 'serial_timeout')
        self.port = self.__get_port()
        self.network_connection = self.is_connected()


    def __get_port(self):
        try:
            return Serial(self.com_port, self.baud, timeout=self.serial_timeout)
        except serial.SerialException:
            print('Windows COM port not found')
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

    def is_connected(self):
        if self.port is None:
            print('No com port found - not connected')
            return False
        startup = self.ts.get_timestamp()
        while True:
            topo = self.get_topology()
            if topo is not None:
                if 'subs' in topo:
                    return True
            if self.ts.get_timestamp() - startup > 120:
                print("TIMEOUT ERROR: Node Failed to Connect to Mesh")
                return False

    def receive_json(self, timeout=60):
        start = self.ts.get_timestamp()
        while True:
            if self.ts.get_timestamp() - start > timeout:
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

    def send(self, node_id, message):
        msg = {'node_id': node_id, 'message': message}
        msg = json.dumps(msg).encode()
        self.port.write(msg)

    def get_sensor_data(self, node_id):
        self.send(node_id, 'sensor_data')
        data = self.receive_json()
        if data is None:
            return data
        elif 'bus_voltage_V' not in data:
            self.send(node_id, 'sensor_data')
            data = self.receive_json()
        if data is None:
            return data
        elif 'bus_voltage_V' not in data:
            return None
        data_with_timestamp = {'timestamp': self.ts.get_timestamp()}
        data_with_timestamp.update(data)
        return data_with_timestamp

    def handle_commands(self):
        # {'command_id': 1, 'priority': 5, 'status': 'incomplete', 'command': 'get_sensor_data', 'node_id': 4144723677}
        # {'command_id': 2, 'priority': 1, 'status': 'complete', 'command': 'get_topology'}
        commands = sorted(cfg.mesh_requests, key=lambda d: d['priority'])
        for command in commands:
            if command['status'] == 'incomplete':
                print('Processing Mesh:', command)
                if command['command'] == 'get_sensor_data':
                    command['response'] = self.get_sensor_data(command['node_id'])
                    command['status'] = 'complete'
                elif command['command'] == 'get_topology':
                    command['response'] = self.get_topology()
                    command['status'] = 'complete'



def main():
    comm = Comm()
    while True:
        comm.handle_commands()


if __name__ == '__main__':
    main()