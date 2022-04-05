from tinydb import TinyDB
from tinydb import Query
from timekeeper import Timestamps
import sys
import glob
import time
import serial
import json


def main():
    port = serial.Serial('COM3', 115200, timeout=1)
    time.sleep(2)
    port.write(b'0\r\n')
    bmp = port.readall()
    file = open('test_img.bmp', 'wb')
    file.write(bmp)
    print('done')

if __name__ == "__main__":
    main()