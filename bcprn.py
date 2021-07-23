#!/usr/bin/env python3
from time import sleep
import cups, sys
from zebra import Zebra
import serial
import logging
from zutils import setPrinters
from barcodes import bcr
from labels import lbl
#File for label titles
#lbl_qty,lbl_title
LBL_TITLES='label_titles.txt'
#Label template file
LBL_FILE='lblTemplate.txt'
PRINTER_MODEL='Zebra Technologies ZTC TLP 2824 Plus'
#Set to None to disable watchdog
WATCHDOG_DEV_NAME='/dev/watchdog'
#Symbol to initiate label prefix
PREFIX='#'

#logging.basicConfig(filename='/home/pi/kiosk.log',filemode='w',level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
class zbc(object):
    def __init__(self,printer):
        self._queue = None
        self.running=False
        for q in Zebra().getqueues():
            if q.startswith(printer):
                self._queue=q
                self.running=True
                logging.info('Queue: {} set'.format(q))
            else:
                logging.error('zbc: {} not found'.format(printer))
    def print(self,label):
        if self.running:
            z=Zebra(self._queue)
            #z.reset_default
            z.output(label,encoding='utf-8')
            logging.info('Printing...\n {}'.format(label))

def scanBC(obj_z):
    bcScanner=bcr()
    lbl_prefix=''
    while bcScanner.running:
        bc_buffer=bcScanner.next()
        #Pat wd
        if wd is not None:
            print('1',file = wd, flush = True)
        if len(bc_buffer)>0:
            if bc_buffer[0]==PREFIX:
                lbl_prefix=bc_buffer[1:]
                bc_buffer=''
            else:
                printBC(lbl_prefix+bc_buffer,obj_z)
                lbl_prefix=''
def printBC(bar_code,obj_z):
    if obj_z.running:
        logging.info('Printing label {}'.format(bar_code))
        l=lbl(bar_code,LBL_FILE,LBL_TITLES)
        #print(l.print())
        obj_z.print(l.print())
    else:
        logging.error('{} not accesible...'.format(PRINTER_MODEL))

def startWatchog(name):
    try:
        dev=open(name,'w')
    except:
        dev = None
    logging.info('Watchdog {}'.format('disabled' if dev is None else 'enabled'))
    return(dev)

def main():
    try:
        conn=cups.Connection()
    except cups.IPPError as e:
        logging.error(e)
        return(False)
    if setPrinters(conn):
        logging.debug('{} OK'.format(PRINTER_MODEL))
    else:
        logging.debug('{} not set'.format(PRINTER_MODEL))
        sys.exit(1)
    z=zbc('Zebra')
    scanBC(z)

        
if __name__ == '__main__':
        logging.basicConfig(level=logging.DEBUG)
        #logging.basicConfig(filename='/home/pi/kiosk.log',filemode='w',level=logging.DEBUG)
        wd=startWatchog(WATCHDOG_DEV_NAME)
        try:
            main()
        except KeyboardInterrupt:
            print("\nExiting")
            if wd is not None:
                print('V',file = wd, flush = True)
