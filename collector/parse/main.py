from collector.base import PlugableBase

import utils.settings as Settings

class Parse(PlugableBase):
    def __init__(self):
        self.stage = "parse"
        super(Parse,self).__init__()
         
    def run(self,inputObject):
        #TODO: need a driver for the parsing routine based on the way that the netflow record is laid out
        #    this should be a plugin that is pluggable to run the field level plugins
        
        for key in self.modInstances:
            self.modInstances[key].run(inputObject)
        print "Parsed Input %s"%repr(inputObject)
        return inputObject
