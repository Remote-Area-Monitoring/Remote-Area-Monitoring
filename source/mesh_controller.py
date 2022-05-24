from control import Command
from timekeeper import Timestamps
from database import Database
from settings import Settings


class Controller:
    def __init__(self):
        self.ts = Timestamps()
        self.config = Settings('general.config')
        nodes_db_path = self.config.get_setting('databases', 'nodes_db_path')
        self.nodes_db = Database(self.config.get_setting('databases', 'nodes_db_path'))
        self.sensor_data_db = Database(self.config.get_setting('databases', 'sensor_data_db_path'))
        self.mesh = Command(self.config.get_setting('mesh_network', 'port'))

    def update_nodes_sensor_data(self):
        records = list()
        nodes = self.nodes_db.get_all()
        for node in nodes:
            if node['status'] == 'active':
                data = self.mesh.get_sensor_data(node['node_id'])
                if data is not None:
                    print(data)
                    records.append(data)
                else:
                    # TODO: record error when node data is not found
                    print('Error: No data available for node', node['node_id'])
        self.sensor_data_db.insert_multiple(records)

    def update(self):
        start = 0
        count = 1
        while True:
            if self.ts.get_timestamp() - start > self.config.get_float_setting('mesh_network', 'query_interval'):
                print('Mesh Network Query:', count)
                start = self.ts.get_timestamp()
                self.update_nodes_sensor_data()
                count += 1


def main():
    try:
        mesh = Controller()
        mesh.update()
    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    main()





