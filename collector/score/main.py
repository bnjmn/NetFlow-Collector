from collector.base import PlugableBase

import sys
import jpype

import utils.settings as Settings

class Score(PlugableBase):
    
    
    def __init__(self):
        self.stage = "score"
        self.datadigestDir = str(Settings.SETTINGS.get("score","datadigestDir"))
        # print sys.executable
        # print "ddDIR=%s"%("-Djava.class.path=" + self.datadigestDir )
        
        model_file = "Skaion_model.bn5"
        data_file = "out_sample.csv"
        output_vars = "OUTCOME"
        thru_vars = "OUTCOME"
                   
        jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=" + self.datadigestDir)

        blah = (jpype.JArray(jpype.JString)([output_vars]))
        print blah
        print dir(blah)
        print blah.__class__
       
        # Load DataDigest Package
        dataDigest = jpype.JPackage('datadigest')
        # Create reference to BatchInferenceFacade class
        BatchInferenceFacade = dataDigest.inference.BatchInferenceFacade
        biInstance = BatchInferenceFacade(jpype.JString(data_file), jpype.JString(model_file), blah, blah)
      
        ### TODO: Fix errors initializing BIF instance; No matching overloads. Cannot get types correct.    
        jpype.shutdownJVM()
        
        return super(Score,self).__init__()

if __name__ == '__main__':
    pass