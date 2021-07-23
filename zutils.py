
#!/usr/bin/env python3
from time import sleep
import cups
import logging
PRINTER_MODEL='Zebra Technologies ZTC TLP 2824 Plus'
def delDefPrinter(conn):
    p=conn.getDefault()
    if p is not None:
        try:
            conn.deletePrinter(p)
        except conn.IPPError as e:
            logging.error('Cannot delete printer {}. {}'.format(p,e))
        else:
            logging.info('Printer {} deleted'.format(p))
    else:
        logging.info('No default printer to delete')

def delJobs(conn):
    jobs_pending = conn.getJobs()
    for j in jobs_pending:
        logging.info('Deleting pending print job {}'.format(j))
        conn.cancelJob(j,purge_job=True)
    return(len(jobs_pending))

def addPrinter(conn,printer):
    queue_name=printer.replace(' ','_')
    ppd_file = conn.getPPDs(ppd_make="Raw")
    ppd_file=[f for f in ppd_file][0]
    devs = conn.getDevices(include_schemes=['usb'])
    if len(devs) == 0:
        logging.error('No USB printers found')
        return(None)
    try:
        device = [k for k,v in devs.items() if v['device-info'].startswith(printer)][0]
    except IndexError:
        logging.error('{} not connected'.format(printer))
        return(None)
    #print(device)
    try:
        conn.addPrinter(queue_name,ppdname=ppd_file,device=device,info=printer)
        conn.setDefault(queue_name)
        conn.setPrinterShared(queue_name,False)
        conn.acceptJobs(queue_name)
        conn.enablePrinter(queue_name)
    except conn.IPPError as e:
        logging.error(e)
        return(None)
    logging.info('{} installed on {}'.format(printer,device))
    return(device)

def checkIfConnected(conn,printer):
    #check if connected printer alreay set in CUPS
    avilable_printers=conn.getDevices(include_schemes=['usb'])
    if len(avilable_printers) == 0:
        logging.error('No USB printers')
        return(None)
    connected_printers=conn.getPrinters()
    for cp in ([v['device-uri'] for k,v in connected_printers.items() if k.startswith(printer.replace(' ','_'))]):
        for ap in avilable_printers:
            if ap == cp:
                logging.info('{} connected'.format(printer))
                return(True)
    logging.error('{} not found'.format(printer))
    return False
    
def setPrinters(conn):
    printer_connected=None
    printer_connected=checkIfConnected(conn,PRINTER_MODEL)
    while printer_connected is None:
        sleep(5)
        printer_connected=checkIfConnected(conn,PRINTER_MODEL)
    if not printer_connected:
        delJobs(conn)
        delDefPrinter(conn)
        p = addPrinter(conn,PRINTER_MODEL)
        if p or p is not None:
            logging.info('Printer {} added'.format(p))
            return(True)
        else:
            logging.error('Cannot connect printer {}'.format(p))
            return(False)
    return(True)
def main():
    #logging.basicConfig(filename='/home/pi/kiosk.log',filemode='w',level=logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)
    try:
        conn=cups.Connection()
    except cups.IPPError as e:
        logging.error(e)
        return(False)
    if setPrinters(conn):
        logging.debug('{} OK'.format(PRINTER_MODEL))
    else:
        logging.debug('{} not set'.format(PRINTER_MODEL))

if __name__ == '__main__':
    main()