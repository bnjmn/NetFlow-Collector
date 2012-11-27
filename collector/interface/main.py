from collector.base import PlugableBase

import utils.settings as Settings

'''
    This class's plugins must return an iterable!!! The Collector main line application expects to iterate over
        the results of this class's plugins' .run() result
'''
class Interface(PlugableBase):
    def __init__(self):
        self.stage = "interface"
        super(Interface,self).__init__()
        
    def run(self,inputObject):
        #HACK: this assumes 1 plugin for the interface
        #        this needs to be fixed
        for key in self.modInstances:
            return self.modInstances[key].run(inputObject)