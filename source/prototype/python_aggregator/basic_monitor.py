
from tinydb import TinyDB
from tinydb import Query
from timekeeper import Timestamps
import sys
import glob
import time
import serial
import json

class Database:
    def __init__(self, path):
        self.db = TinyDB(path)
        self.ts = Timestamps()

    def insert(self, dataobj):
        self.db.insert(dataobj)

    # def get_records(self, start_date: float = None, charge_code=None):
    #     data = []
    #     if charge_code is not None:
    #         if start_date is not None:
    #             data.extend((Query().fragment({'charge_code': charge_code})) & (Query()['clock_in'] >= start_date))
    #         else:
    #             data.extend(self.get_report_single_field('charge_code', charge_code))
    #     elif start_date is not None:
    #         data.extend(self.db.search(Query()['clock_in'] >= start_date))
    #     else:
    #         data = self.db.all()
    #     if not data:
    #         return None
    #     return data

    def get_report_single_field(self, field, value):
        return self.db.search(Query()[field] == value)


def main():
    port = serial.Serial('COM3', 115200, timeout=1)
    time.sleep(2)
    ts = Timestamps()
    db = Database('\\\\ubuntu\\net-dev\\databases\\solar_log.json')
    while True:
        line = port.readline()
        line = line.decode()
        if 'bus_voltage' in line:
            data = json.loads(line)
            data['timestamp'] = ts.get_timestamp()
            db.insert(data)
            print(data)


if __name__ == "__main__":
    main()
