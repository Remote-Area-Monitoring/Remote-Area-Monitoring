import serial
from serial import Serial
import json
import time
from source.util.timekeeper import Timestamps
from source.util.database import Database
from source.util.settings import Settings
import re
import sys


class Mesh:
    def __init__(self):
        self.ts = Timestamps()
        self.config = Settings('general.config')
        self.nodes_db = Database(self.config.get_setting('databases', 'nodes_db_path'))
        self.sensor_data_db = Database(self.config.get_setting('databases', 'sensor_data_db_path'))
        self.port = self.config.get_setting('mesh_network', 'port')
        self.baud = self.config.get_int_setting('mesh_network', 'baud_rate')
        self.serial_timeout = self.config.get_int_setting('mesh_network', 'serial_timeout')
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
            if time.time() - startup > self.config.get_int_setting('mesh_network', 'connection_timeout'):
                print("TIMEOUT ERROR: Node Failed to Connect to Mesh")
                return False

    def send(self, node_id, message):
        msg = {'node_id': node_id, 'message': message}
        msg = json.dumps(msg).encode()
        self.port.write(msg)

    def receive_json(self):
        timeout = self.config.get_int_setting('mesh_network', 'receive_timeout')
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

    def update_nodes_sensor_data(self):
        records = list()
        nodes = self.nodes_db.get_all()
        for node in nodes:
            if node['status'] == 'active':
                data = self.get_sensor_data(node['node_id'])
                if data is not None:
                    print(data)
                    records.append(data)
                else:
                    # TODO: record error when node data is not found
                    print('Error: No data available for node', node['node_id'])
        self.sensor_data_db.insert_multiple(records)

    def receive_pixel_packets(self):
        # interesting note: The number of packets has no effect on the transfer speed, only the amount of data
        timeout = self.config.get_int_setting('mesh_network', 'image_timeout')
        start = self.ts.get_timestamp()
        packets = list()
        total_packets = None
        while True:
            if self.ts.get_timestamp() - start > timeout:
                return None
            try:
                packet = self.port.readline()
                packet = packet.decode().replace('*', '')
                # print(packet)
                data = json.loads(packet)
                if 'pixels' in data:
                    print(len(data['pixels']))
                    print(packet)
                    packets.append(data)
                elif 'total_packets_sent' in data:
                    total_packets = data['total_packets_sent']
                    print(data)
                    print(total_packets)
                if total_packets is not None:
                    if len(packets) >= total_packets:
                        print('All Packets Received')
                        break
            except Exception as e:
                print(e)
                continue
        print("Transmission Time:", self.ts.get_timestamp() - start)
        return packets

    def get_image_data(self, node_id):
        self.send(node_id, 'image')
        pixels = list()
        packet_data = self.receive_pixel_packets()
        packets = sorted(packet_data, key=lambda d: d['packet_number'])
        for packet in packets:
            pixels.extend(packet['pixels'])
        pixel_data = bytearray(pixels)
        return pixel_data

    def write_image(self):
        pixels = self.get_image_data(4144885065)
        test_obj = dict()
        test_obj['pixel_data'] = pixels
        print(test_obj)
        print("test_obj size: {} bytes".format(sys.getsizeof(test_obj)))
        with open('test_img7.jpg', 'wb') as file:
            file.write(bytes(pixels))
        print('done')




def main():
    command = Mesh()
    # command.send(4144723677, 'This is a test message')
    # print(command.receive_json())
    # print(command.get_topology())
    # print(command.get_sensor_data(4144723677))
    # print(command.get_sensor_data(2222631473))
    # start = 0
    # while True:
    #     try:
    #         if time.time() - start > 5:
    #             start = time.time()
    #             print(command.get_sensor_data(4144723677))
    #     except KeyboardInterrupt:
    #         exit(0)
    # command.get_topology()
    command.write_image()


if __name__ == '__main__':
    main()


