#!/usr/bin/env python3
import os,sys,socket
import logging
from string import Template

LBL_FILE='lblTemplate.txt'
LBL_TITLES='alabel_titles.txt'

logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(filename='/home/pi/kiosk.log',filemode='w',level=logging.DEBUG)

class lbl(object):
    def __init__(self,barcode,template,title):
        self.barcode=barcode
        self._path=os.path.dirname(os.path.abspath(sys.argv[0]))
        self._content=self._getContent('{}/{}'.format(self._path,template))
        if self._content is None:
            self._content = self._getDefaultContent()
            self._saveLabel('{}/{}'.format(self._path,self._content),self._content)

        self._titles=self._getContent('{}/{}'.format(self._path,title))
        if self._titles is None:
            self._titles='1,EGL'
            self._saveLabel('{}/{}'.format(self._path,title),self._titles)

    def _getContent(self,file):
        t=None
        try:
            with open(file, 'r') as f:
                t=f.read()
            logging.info('File {} found'.format(file))
        except FileNotFoundError:
            logging.error('File {} not found.'.format(file))
        return(t)

    def _getDefaultContent(self):
        t='''
^XA
#label darkness 0-30
~SD10
#label offset width,height
^LH40,10^MTT
^FO0,0
^AS
^FD$lblTitle^FS
^FO0,35
^AQ
^FD$hostName ^FS
^FO30,150
^AS
^FD$barCode^FS
^FO0,65
^GB200,2,2
^FS
^BY2,3,105
^FT20,150
^BCN,80,N,N
^FD>;$barCode^FS
^PQ$numCopies
^XZ
'''
        return(t)

    def _saveLabel(self,file,content):
        try:
            with open(file,'w+') as f:
                f.write(content)
                logging.info('File {} created'.format(file))
        except Exception as e:
            logging.error('{}'.format(e))

    def print(self):
        tmpl=Template(self._content)
        lbl_string=''
        for s in self._titles.splitlines():
            qty=s.split(',')[0]
            title=s.split(',')[1]
            lbl_string=lbl_string+tmpl.substitute(lblTitle=title,hostName=socket.gethostname(),barCode=self.barcode,numCopies=qty)
        return(lbl_string if len(lbl_string)>0 else None)

def main():
    l=lbl('123456789',LBL_FILE,LBL_TITLES)
    print(l.print())
if __name__ == "__main__":
    main()
