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
    try:
        port = serial.Serial('COM3', 115200, timeout=1)
    except:
        port = serial.Serial('/dev/tty.usbserial-0001', 115200, timeout=1)
    time.sleep(2)
    ts = Timestamps()
    while True:
        line = port.readline()
        try:
            line = line.decode()
        except Exception as e:
            print(e)
            print(line)
        if 'node_id' in line:
            try:
                data = json.loads(line)
                data['timestamp'] = ts.get_timestamp()
                print('')
                print(data)
                for key, value in data.items():
                    print(key, ':', value)
            except Exception as e:
                print(e)
        elif DEBUG:
            print(line)


if __name__ == "__main__":
    main()