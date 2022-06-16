import json
import time
import serial
import json


def parse_data(data):
    print(data)
    data_string = '['
    data = data.decode('utf-8')
    start = data.find('{"')
    end = data.find('0\r\n')
    for i in range(start, end):
        data_string += data[i]
        if data[i] == '}' and (i + 1) < end:
            data_string += ','
    data_string += ']'
    print(data_string)
    return json.loads(data_string)


def get_pixel_data(packet_data):
    pixel_data = bytearray()
    pixels = []
    packets = sorted(packet_data, key=lambda d: d['packet_number'])
    print(packets)
    for packet in packets:
        print(packet)
        print(len(packet['pixels']))
        pixels.extend(packet['pixels'])
    pixel_data = bytearray(pixels)
    print(pixels)
    print(pixel_data)
    print(pixel_data.find(b'\xff\xd8'))
    print(pixel_data.find(b'\xff\xd9'))
    return pixel_data


def main():
    try:
        port = serial.Serial('COM3', 115200, timeout=10)
    except:
        port = serial.Serial('/dev/tty.usbserial-0001', 115200, timeout=1)

    time.sleep(2)

    port.write('1\r\n'.encode('utf-8'))
    data = port.readall()
    print(data.find(b'\xff\xd8'))
    print(data.find(b'\xff\xd9'))
    print(data)
    packets = parse_data(data)
    pixels = get_pixel_data(packets)
    print(pixels)
    print(len(pixels))
    print(pixels.find(b'\xff\xd8'))
    print(pixels.find(b'\xff\xd9'))
    # image = bytearray()
    image = pixels
    for i in range(pixels.find(b'\xff\xd8'), pixels.find(b'\xff\xd9') + 1):
        image.append(pixels[i])
    print('writing image file')
    with open('test_img6.jpg', 'wb') as file:
        file.write(bytes(image))
    print('done')


if __name__ == '__main__':
    main()
