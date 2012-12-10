from collector.base import ScorePlug
import utils.settings as Settings

import subprocess
import csv
import StringIO

from collector.outputcsv import CSV

class ContinentBasedSimilarityModel(ScorePlug):
    def __init__(self):
        self.data_file = "./score/models/blah.csv"
        self.inf_file = "./score/models/blahInf.csv"
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
        
        f = open(self.inf_file, "w")
        f.write(results)
        f.close()
        
        realResults = subprocess.Popen(["Rscript", "./score/similarityscore.R", self.inf_file, self.model_file], \
                                   stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()[0]     
        print "AS Model Similarity Score = %s " %(str(realResults).strip())
        print "Observed actual value is %s" %str(inputObject.continent)
            
