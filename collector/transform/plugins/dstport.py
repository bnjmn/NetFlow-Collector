'''
Created on Nov 28, 2012

@author: benjamin
'''
import utils.settings as Settings
from collector.base import PluginBase

class DstPort(PluginBase):
    # TODO: currently being read in a one string, need to parse to int array 
    #  create a PortPlug base for SrcPort and DstPort to inherit from
    # ports = Settings.SETTINGS.getlist(Settings.SETTINGS.get("transform","srcports"))
    ports = [53, 80, 110, 25, 443]
    # print " Approved Source Ports: %s" %ports
    
    def run(self,inputObject):
        if(inputObject.dst_port in DstPort.ports):
            # Do nothing (for now)
            pass
        else:
            inputObject.dst_port = "OTHER"
        # print "SRC Port %s"%inputObject.src_port 