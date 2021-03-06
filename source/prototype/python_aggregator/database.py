from tinydb import TinyDB
from tinydb import Query
from collections import OrderedDict
import csv
from timekeeper import Timestamps


class Database:
    def __init__(self, database_file):
        self.db = TinyDB(database_file)
        self.ts = Timestamps()

    def insert(self, dataobj):
        self.db.insert(dataobj)

    def insert_multiple(self, data_list):
        self.db.insert_multiple(data_list)

    def get_records(self, start_date: float = None):
        data = []
        if start_date is not None:
            data.extend(self.db.search(Query()['timestamp'] >= start_date))
        else:
            data = self.db.all()
        if not data:
            return None
        return data

    def get_data_single_field(self, field, value, timestamp=None):
        if timestamp is not None:
            return self.db.search((Query()[field] == value) & (Query()['timestamp'] >= timestamp))
        else:
            return self.db.search(Query()[field] == value)

    def get_data_data_obj(self, dataobj, timestamp=None):
        if timestamp is not None:
            return self.db.search((Query().fragment(dataobj)) & (Query()['timestamp'] >= timestamp))
        return self.db.search(Query().fragment(dataobj))

