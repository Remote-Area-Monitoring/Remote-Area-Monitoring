from timekeeper import Timestamps
from collections import OrderedDict
import csv
from tinydb import TinyDB
from tinydb import Query
from timekeeper import Timestamps

DEFAULT_PATH = "\\Desktop"


class DataFormatter:
    def __init__(self, path):
        self.db = TinyDB(path)
        self.ts = Timestamps()

    def get_records(self, start_date: float = None):
        data = []
        if start_date is not None:
            data.extend(self.db.search(Query()['timestamp'] >= start_date))
        else:
            data = self.db.all()
        if not data:
            return None
        return data

    def get_report_single_field(self, field, value):
        return self.db.search(Query()[field] == value)

    def get_solar_data(self, start_date: float = None):
        formatted_data = []
        count = 0
        raw_data = self.get_records(start_date)
        for record in raw_data:
            data = dict()
            data['Log Number'] = count
            data['Bus Voltage (V)'] = record['bus_voltage']
            data['Shunt Voltage (mV)'] = record['shunt_voltage']
            data['Load Current (mA)'] = record['current']
            data['Load Voltage (V)'] = record['bus_voltage'] + (record['shunt_voltage'] / 1000)
            data['Power (mW)'] = record['power']
            data['DateTime'] = self.ts.get_excel_timestring(record['timestamp'])
            count += 1
            formatted_data.append(data)
        return formatted_data

    def generate_csv(self, data, file_name):
        # headers = set()
        # for record in data:
        #     headers.update(OrderedDict(record).keys())
        ts = Timestamps()
        ordered_filenames = OrderedDict(data[len(data) - 1])
        output_file = file_name + ts.get_time_string() + ".csv"
        with open(output_file, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=ordered_filenames, restval="-", extrasaction="ignore")
            writer.writeheader()
            for record in data:
                writer.writerow(record)


def main():
    df = DataFormatter('solar_log.json')
    data = df.get_solar_data()
    print(data)
    df.generate_csv(data, 'solar_data_')


if __name__ == '__main__':
    main()
