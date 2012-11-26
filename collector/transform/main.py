'''
Created on Nov 13, 2012

@author: rob
'''
from collector.base import PlugableBase

import utils.settings as Settings

class Transform(PlugableBase):
    def __init__(self):
        self.stage = "transform"
        return super(Transform,self).__init__()

    def run(self,inputObject):
        #TODO: need a driver for the parsing routine based on the way that the netflow record is laid out
        #    this should be a plugin that is pluggable to run the field level plugins
        
        for key in self.modInstances:
            self.modInstances[key].run(inputObject)
        return inputObject