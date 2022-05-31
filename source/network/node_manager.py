from source.util.database import Database
from source.util.timekeeper import Timestamps
from source.util.settings import Settings


class Nodes:
    def __init__(self):
        self.ts = Timestamps()
        self.config = Settings('general.config')
        self.db = Database(self.config.get_setting('databases', 'nodes_db_path'))

    def add_node(self, node_id, status, lat, lon, node_config: dict = None):
        existing_record = self.db.get_data_single_field('node_id', node_id)
        if len(existing_record) > 0:
            return False
        dataobj = {
            'node_id': node_id,
            'status': status,
            'lat': lat,
            'lon': lon,
            'node_config': node_config,
            'date_created': self.ts.get_timestamp(),
            'date_last_modified': self.ts.get_timestamp()
        }
        self.db.insert(dataobj)
        return True

    def remove_node(self, node_id):
        dataobj = {
            'node_id': node_id
        }
        removed_ids = self.db.remove_single_record(dataobj)
        if len(removed_ids) > 0:
            return True
        return False


def main():
    nodes = Nodes()
    # Adds dev prototype node
    print(nodes.add_node(2222631473, 'active', 28.316450, -80.726982))
    # print(nodes.remove_node(2222631473))
    # Adds proto 1 node
    # nodes.add_node(4144723677, 'active', 28.316450, -80.726982)


if __name__ == '__main__':
    main()