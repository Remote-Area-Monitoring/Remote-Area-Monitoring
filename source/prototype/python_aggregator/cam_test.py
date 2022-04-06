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
    # 01: 19:11.697 -> 2
    # 01: 19:11.697 -> 16
    # 01: 19:11.697 -> 45
    port.write(b'\x02')
    port.write(b'\x10')
    port.write(b'\x2D')
    data = port.readall()
    print(data.find(b'\xff\xd8'))
    print(data.find(b'\xff\xd9'))
    print(data)
    # file = open('test_img.', 'wb')
    # file.write(data)
    image = bytearray()
    for i in range(data.find(b'\xff\xd8'), data.find(b'\xff\xd9') + 1):
        image.append(data[i])
    print('writing image file')
    with open('test_img2.jpg', 'wb') as file:
        file.write(bytes(image))
    print('done')



if __name__ == "__main__":
    main()