'''
Created on Nov 20, 2012

@author: benjamin
'''
import utils.settings as Settings
from collector.base import PluginBase

class SrcPort(PluginBase):
    # TODO: currently being read in a one string, need to parse to int array 
    # ports = Settings.SETTINGS.getlist(Settings.SETTINGS.get("transform","srcports"))
    ports = [53, 80, 110, 113, 443]
    # print " Approved Source Ports: %s" %ports
    
    def run(self,inputObject):
        if(inputObject.src_port in SrcPort.ports):
            # Do nothing (for now)
            pass
        else:
            inputObject.src_port = "OTHER"
        # print "SRC Port %s"%inputObject.src_port 