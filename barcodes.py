#!/usr/bin/env python3
import serial
import logging
import sys
from time import sleep
class bcr(object):
    def __init__(self,port='/dev/ttyACM0',timeout=1):
        self.bc=None
        self.running=False
        try:
            self.bc=serial.Serial(port=port,timeout=timeout)
            self.running=True
        except Exception as e:
            logging.error('{}'.format(e))
    def next(self):
        try:
            buffer=self.bc.readline()
        except Exception as e:
            logging.error(e)
            self.running=False
        return(buffer.decode('UTF-8').strip())
def main():
    b=bcr()
    while b.running:
        print(b.next())
if __name__ == "__main__":
    #logging.basicConfig(filename='/home/pi/kiosk.log',filemode='w',level=logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting")