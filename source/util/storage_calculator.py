from source.util.settings import Settings
from source.util.database import Database
import os


class Storage:
    def get_sensor_estimate(self, years, num_nodes, polling_rate):
        config = Settings('general.config')
        db = Database(config.get_setting('databases', 'sensor_data_db_path'))
        data = db.get_all()
        file_size = os.path.getsize(config.get_setting('databases', 'sensor_data_db_path'))
        record_size_bytes = file_size / len(data)
        seconds_per_year = 31556952
        records_per_node = (seconds_per_year / polling_rate)
        total_records_per_year = records_per_node * num_nodes
        total_records = total_records_per_year * years
        file_size_bytes = record_size_bytes * total_records
        file_size_gb = file_size_bytes * 0.000000001
        print('--- {} Year Sensor Database Size Estimate ---'.format(years))
        print('Current database size: {} bytes'.format(file_size))
        print('Total Records: ', len(data))
        print('----')
        print('Size in {} years: {} Gb'.format(years, round(file_size_gb, 2)))
        print('----')


def main():
    store = Storage()
    store.get_sensor_estimate(5, 150, 15*60)


if __name__ == '__main__':
    main()
