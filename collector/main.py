'''
Created on Oct 22, 2012

@author: rweiss
'''
import utils.settings as settings
import gevent

from gevent.server import DatagramServer

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
        print "Starting Collector process in %s"%os.getcwd()
        print "Gevent Version %s"%gevent.__version__
        
        #TODO: move output file name to config
        fname = "./NetFlow.%s.bin"%str(time.time()*100000)
        
        #WARN: might want to remove this after testing
        self.out = open(fname,"wb")
        
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
        self.out.close()
        #really important to call del on the csv obj to ensure it closes correctly
        del self.csv
    
    def handle(self, rawData, address):
        Collector.x += 1
        #print '%s %s: got %r' % (Collector.x, address[0], data)  
        self.out.write(rawData)
        
        interfacedData = self.interface.run(rawData)
        self.parse.run(interfacedData)
        self.describe.run(interfacedData)
        self.standardize.run(interfacedData)
        self.transform.run(interfacedData)
        self.partition.run(interfacedData)
        self.csv.writeRow(self.csv.format(interfacedData))

if __name__ == '__main__':
    #TODO: move IP and port to config
    server = Collector(("0.0.0.0",6005))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print "Terminating Collector"
        server.done()
        server.stop()
