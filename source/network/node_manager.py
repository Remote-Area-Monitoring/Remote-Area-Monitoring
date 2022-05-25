from source.util.database import Database
from source.util.timekeeper import Timestamps
from source.util.settings import Settings


class Nodes:
    def __init__(self):
        self.ts = Timestamps()
        self.config = Settings('config/general.config')
        self.db = Database(self.config.get_setting('databases', 'nodes_db_path'))

    def add_node(self, node_id, status, lat, lon, node_config: dict = None):
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


def main():
    nodes = Nodes()
    # Adds dev prototype node
    nodes.add_node(2222631473, 'active', 28.316450, -80.726982)


if __name__ == '__main__':
    main()
