#!/usr/bin/env python3
import logging

#logging.basicConfig(filename='/home/pi/kiosk.log',filemode='w',level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
TITLES="label_titles.txt"
def readLabelTitles(data):
    l=None
    try:
        with open(data) as f:
            l=f.readlines()
    except FileNotFoundError:
        logging.error('File {} not found'.format(TITLES))
    return(l)

def main():
    d=readLabelTitles(TITLES)
    for l in d:
        print(l.strip().split(','))

if __name__ == "__main__":
    main()