from collector.base import ScorePlug
import utils.settings as Settings

import subprocess
import csv
import StringIO

from collector.outputcsv import CSV

class SampleScore(ScorePlug):
    def __init__(self):
        self.data_file = "./blah.csv"
        #self.model_file = "./score/models/Skaion_model.bn5"
        self.model_file = "./score/models/Geo 5b5 AS Query Using NoA Binning All Parts.bn5"        
        self.outs = ["bytes_sent",
                     "continent",
                     "dst_port",
                     "ip_proto",
                     "netmask",
                     "pkts_sent",
                     "src_port",
                     "tcp_flag_ACK",
                     "tcp_flag_FIN",
                     "tcp_flag_PSH",
                     "tcp_flag_RST",
                     "tcp_flag_SYN",
                     "tcp_flag_URG"] 
        self.thrus = self.outs
    
        self.outOfInterest = "ip_proto_udp"
    
    # TODO: Move this to ScorePlug, Complains 'module' not iterable    
    def createCSV(self, inputObject):
        self.csv = CSV(self.data_file)
        self.csv.writeRow(self.csv.format(inputObject))
        self.csv.__del__() # close file
    def getResults(self):
        results = subprocess.Popen(["jython", ScorePlug.pyPath, ScorePlug.jythonExe, self.data_file, self.model_file, str(self.outs), str(self.thrus)], \
                                   stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()[0]
        return results 

    def run(self,inputObject):
        
        self.runBatchInference(inputObject)       
        self.createCSV(inputObject)
        results = self.getResults()
        #print results
        
        f = open("./blahInf.csv", "w")
        f.write(results)
        f.close()
        
        realResults = subprocess.Popen(["Rscript", "./score/similarityscore.R", "./blahInf.csv", self.model_file], \
                                   stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()[0]     
        print realResults
        buff = StringIO.StringIO(realResults)
        header = buff.readline().rstrip('\n').split(',')
        #pos = header.index(self.outOfInterest)
        pos = header.index("TOTAL_SCORE")
#        print header
        for line in buff:
            d = line.rstrip('\n').split(',')
            #TODO: Find a better way to avoid last line with just \n
            if len(d) > 1:
                #print "Predicted %s = %s" %(self.outOfInterest, str(d[pos]))
                print "AS Model Similarity Score = %s" %(str(d[pos]))
            