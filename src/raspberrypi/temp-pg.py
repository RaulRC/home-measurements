import sys
import time
import RPi.GPIO as GPIO
import Adafruit_DHT
import datetime
import requests

HOST = 'your_host'
PORT = 'your_port'

URL = f"http://{HOST}:{PORT}/sensor-data"

def getSensorData():
   RH, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
   return (str(RH), str(T))

def empty_buffer(buff):
   while len(buff) > 0:
      pl = buff.pop()
      sc = send_request(pl)
      if sc != 200:
         buff.append(pl)
         break
      else:
         print("Empying buffer", sc, pl)
   return buff

def send_request(pl):
   r = requests.post(URL, json=pl, timeout=3)
   return r.status_code

def main():
   print ('Iniciando...')
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
              pl['room'] = "basement"
              pl['timestamp'] = timestamp
              status_code = send_request(pl)
              if status_code == 200:
                 print(f"[{status_code}] {timestamp} {pl}")
                 if len(buff) > 0:
                    buff = empty_buffer(buff)
              else:
                 print("Buffering...", pl, len(buff))
                 buff.append(pl)
           except Exception as e:
               print ('Terminado.' + str(e))
               buff.append(pl)
           finally:
              time.sleep(60)

if __name__ == '__main__':
   main()
