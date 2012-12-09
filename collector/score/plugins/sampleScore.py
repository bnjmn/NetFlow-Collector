from collector.base import ScorePlug
import utils.settings as Settings
import subprocess
import csv
import StringIO

from collector.outputcsv import CSV

class SampleScore(ScorePlug):

    datadigestDir = str(Settings.SETTINGS.get("score","datadigestDir"))
    pyPath = "-Dpython.path=" + str(datadigestDir)
    jythonExe = "./score/JythonBI.py"

#    data_file = "./score/models/out_sample.csv"
    data_file = "./score/models/blah.csv"
    model_file = "./score/models/Skaion_model.bn5"
    outs = ["OUTCOME"]
    thrus = ["OUTCOME"]
    
    outOfInterest = "outcome_malicious"


    def run(self,inputObject):

        self.csv = CSV(self.data_file)
        self.csv.writeRow(self.csv.format(inputObject))
        self.csv.__del__()
        # subprocess.call(["jython", pyPath, jythonExe, data_file, model_file, str(outs), str(thrus)])
        results = subprocess.Popen(["jython", self.pyPath, self.jythonExe, self.data_file, self.model_file, str(self.outs), str(self.thrus)], \
                                   stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()[0]
     
        # print results
        buff = StringIO.StringIO(results)
        header = buff.readline().rstrip('\n').split(',')
        pos = header.index(self.outOfInterest)
#        print header
        for line in buff:
            d = line.rstrip('\n').split(',')
            #TODO: Find a better way to avoid last line with just \n
            if len(d) > 1:
                print "Predicted %s = %s" %(self.outOfInterest, str(d[pos]))
            