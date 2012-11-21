'''
Created on Oct 22, 2012

@author: rweiss
'''

import utils.settings as settings

import gevent
from gevent.server import DatagramServer

import logging

from interface import Interface
from outputcsv import CSV
from parse import Parse
from standardize import Standardize
from transform import Transform
from partition import Partition
from describe import Describe

import os,time

class Collector(DatagramServer):
    x = 0
    def __init__(self,args):

        # create logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        
        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # add formatter to ch
        ch.setFormatter(formatter)
        
        # add ch to logger
        self.logger.addHandler(ch)        
        self.logger.debug( "Starting Collector process in %s"%os.getcwd())
        self.logger.debug( "Gevent Version %s"%gevent.__version__)
        
        #TODO: move output file name to config
        #fname = "./NetFlow.%s.bin"%str(time.time()*100000)
        
        #WARN: might want to remove this after testing
        #self.out = open(fname,"wb")
        
        #create tool instances
        self.interface = Interface()
        self.parse = Parse()
        self.describe = Describe()
        self.standardize = Standardize()
        self.transform = Transform()
        self.partition = Partition()
        
        #TODO: move csv name to config
        self.csv = CSV("output.csv")
        
        return super(Collector,self).__init__(args)
    
    def done(self):
        #self.out.close()
        #really important to call del on the csv obj to ensure it closes correctly
        del self.csv
    
    def handle(self, rawData, address):
        Collector.x += 1
        #print '%s %s: got %r' % (Collector.x, address[0], data)  
        #self.out.write(rawData)
        
        interfacedData = self.interface.run(rawData)
        #once the rawData is "interfaced" we are passing it around by reference
        # interfaced data must be iterable
        try:
            for record in interfacedData:
                self.parse.run(record)
                self.describe.run(record)
                self.standardize.run(record)
                self.transform.run(record)
                self.partition.run(record)
                self.csv.writeRow(self.csv.format(record))
        except Exception as e:
            self.logger.error("Interfaced data is not iterable %s"%(str(e)))

if __name__ == '__main__':
    #TODO: move IP and port to config
    server = Collector(("0.0.0.0",6005))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print "Terminating Collector"
        server.done()
        server.stop()
