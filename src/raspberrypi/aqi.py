#!/usr/bin/python

# Requires pyserial. Install via:
# pip install pyserial

from __future__ import print_function
import argparse
from serial import Serial, EIGHTBITS, STOPBITS_ONE, PARITY_NONE
import time, struct, datetime, json
import argparse

parser = argparse.ArgumentParser(description='AQI measurement script')
parser.add_argument('--path', type=str, default="/home/pi/measurements/", help='Path to save measurement files')
parser.add_argument('--port', type=str, default="/dev/ttyUSB0", help='Serial port')
parser.add_argument('--place', type=str, default="whitehouse", help='Serial port')
parser.add_argument('--room', type=str, default="main floor", help='Serial port')

parser.add_argument('--baudrate', type=int, default=9600, help='Baudrate')
args = parser.parse_args()

PATH = args.path
port = args.port
baudrate = args.baudrate


def main():
    # Prepare serial connection.
    ser = Serial(port, baudrate=baudrate, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE)
    ser.flushInput()

    HEADER_BYTE = b"\xAA"
    COMMANDER_BYTE = b"\xC0"
    TAIL_BYTE = b"\xAB"

    byte, previousbyte = b"\x00", b"\x00"

    while True:
        previousbyte = byte
        byte = ser.read(size=1)
        
        # We got a valid packet header.
        if previousbyte == HEADER_BYTE and byte == COMMANDER_BYTE:
            packet = ser.read(size=8) # Read 8 more bytes
            
            # Decode the packet - little endian, 2 shorts for pm2.5 and pm10, 2 ID bytes, checksum.
            readings = struct.unpack('<HHcccc', packet)
            
            # Measurements.
            pm_25 = readings[0]/10.0
            pm_10 = readings[1]/10.0
            
            # ID
            id = packet[4:6]
            
            # Prepare checksums.
            checksum = readings[4][0]
            calculated_checksum = sum(packet[:6]) & 0xFF
            checksum_verified = (calculated_checksum == checksum)
            
            # Message tail.
            tail = readings[5]
            
            if tail == TAIL_BYTE and checksum_verified:
                timestamp = str(datetime.datetime.now())
                for item, value in zip(['pm_25', 'pm_10'], [pm_25, pm_10]):
                    result = dict()
                    result['timestamp'] = timestamp
                    result['key'] = item
                    result['value'] = value
                    result['place'] = args.place
                    result['room'] = args.room
                    
                    with open(f"{PATH}{timestamp}-{item}.json", 'w') as fp:
                        json.dump(result, fp)
                        print(result)

if __name__ == "__main__":
    main()
