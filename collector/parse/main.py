from collector.base import PlugableBase

import utils.settings as Settings

class Parse(PlugableBase):
    def __init__(self):
        self.stage = "parse"
        super(Parse,self).__init__()
        
        #create running instances; forces singleton
        self.modInstances={}
        for key in self.mods:
            self.modInstances[key]= self.mods[key]()
    
    def run(self,inputObject):
        #TODO: need a driver for the parsing routine based on the way that the netflow record is laid out
        #    this should be a plugin that is pluggable to run the field level plugins
        
        #1. iterate over the data portion of the flow record calling the plugins for each record.
        for flowRecord in inputObject.data:
            print "Flow Record %s"%repr(flowRecord)
            for key in self.modInstances:
                self.modInstances[key].run(flowRecord)
        print "Parsed Input %s"%repr(inputObject)
        return inputObject
