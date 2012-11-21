'''
Created on Nov 20, 2012

@author: benjamin
'''
from collector.base import PluginBase

class SrcPort(PluginBase):
    # Use a static list of approved ports for now
    # TODO: Make this more dynamic, maybe pull array from shared memory or config file
    ports = [53, 80, 110, 113, 443] #<---- These ports are currently being used as examples based on LS' research
    def run(self,inputObject):
        if(inputObject.src_port in SrcPort.ports):
            # Do nothing (for now)
            pass
        else:
            inputObject.src_port = "OTHER"
        print "SRC Port %s"%inputObject.src_port 
        
