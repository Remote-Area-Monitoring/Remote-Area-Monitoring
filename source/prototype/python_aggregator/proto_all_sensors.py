from tinydb import TinyDB
from tinydb import Query
from timekeeper import Timestamps
import sys
import glob
import time
import serial
import json

DEBUG = True

def main():
    port = serial.Serial('COM3', 115200, timeout=1)
    time.sleep(2)
    ts = Timestamps()
    while True:
        line = port.readline()
        line = line.decode()
        if 'node_id' in line:
            try:
                data = json.loads(line)
                data['timestamp'] = ts.get_timestamp()
                print(data)
                for key, value in data.items():
                    print(key, ':', value)
            except Exception as e:
                print(e)
        elif DEBUG:
            print(line)


if __name__ == "__main__":
    main()