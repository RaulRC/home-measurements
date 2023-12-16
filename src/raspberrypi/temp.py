#!/usr/bin/python
# Requires pyserial. Install via:
# pip install pyserial

from __future__ import print_function
from serial import Serial, EIGHTBITS, STOPBITS_ONE, PARITY_NONE
import sys
import time
import RPi.GPIO as GPIO
import Adafruit_DHT
import datetime
import requests
import time, struct
import sys
import os
import json



HOST = sys.argv[1]
PORT = sys.argv[2]
AQI_FOLDER = sys.argv[3]

URL = f"http://{HOST}:{PORT}/sensor-data"

def getSensorData():
   """
   Get temperature and humidity data from the DHT22 sensor.

   Returns:
      tuple: A tuple containing the humidity and temperature values.
   """
   RH, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
   return (str(RH), str(T))

def empty_buffer(buff):
   """
   Empty the buffer by sending the buffered data to the server.

   Args:
      buff (list): The buffer containing the data to be sent.

   Returns:
      list: The updated buffer after sending the data.
   """
   while len(buff) > 0:
      pl = buff.pop()
      sc = send_request(pl)
      if sc != 200:
         buff.append(pl)
         break
      else:
         print("Emptying buffer", sc, pl)
   return buff

def send_request(pl):
   """
   Send a POST request to the server with the payload.

   Args:
      pl (dict): The payload to be sent.

   Returns:
      int: The status code of the HTTP response.
   """
   r = requests.post(URL, json=pl, timeout=3)
   return r.status_code

def send_aqi_data():
   """
   Send measurements from every file in the specified folder.

   Args:
      folder_path (str): The path to the folder containing the JSON files.

   Returns:
      None
   """
   for filename in os.listdir(AQI_FOLDER):
      file_path = os.path.join(AQI_FOLDER, filename)
      ff = open(file_path, 'r')
      try:
         data = json.loads(ff.read())
         # Send the data as a request
         result = send_request(data)
         if result == 200:
            ff.close()
            os.remove(file_path)
            print(f"Sent request for file: {filename}")
      except Exception as e:
         print(f"Failed to send request for file: {filename}")
         print(str(e))
   return


def main():
   """
   Main function to collect sensor data and send it to the server.
   """
   print('Initializing...')
   buff = list()
   while True:
      RH, T = getSensorData()
      measures = dict()
      measures['temp'] = str(round(float(T), 2))
      measures['humidity'] = str(round(float(RH), 2))
      timestamp = str(datetime.datetime.now())

      for key in ['temp', 'humidity']:
         try:
            pl = dict()
            pl['key'] = key
            pl['value'] = measures[key]
            pl['place'] = "whitehouse"
            pl['room'] = "main floor"
            pl['timestamp'] = timestamp
            status_code = send_request(pl)
            if status_code == 200:
               print(f"[{status_code}] {timestamp} {pl}")
               if len(buff) > 0:
                  buff = empty_buffer(buff)
               send_aqi_data()
            else:
               print("Buffering...", pl, len(buff))
               buff.append(pl)
         except Exception as e:
            print('Terminated.' + str(e))
            buff.append(pl)
      time.sleep(60)

if __name__ == '__main__':
   main()

# To invoke this script, run the following command in the terminal:
# python temp.py <HOST> <PORT> <AQI_FOLDER>
# Replace <HOST> with the server host and <PORT> with the server port and <AQI_FOLDER> with the path to the folder containing the AQI JSON files.
