'''
Created on Nov 27, 2012

@author: rob
'''
import utils.settings as settings
from collector.base import PluginBase
import utils.pygeoip as pygeoip
import os

class GeoIP(PluginBase):
    missingValue = "UNK"
    
    def __init__(self):
        #print( "GeoIP working dir in %s"%os.getcwd())
        self.db = pygeoip.Database(settings.SETTINGS.get("geoip","database"))
    def run(self,inputObject):
        info = self.db.lookup(inputObject.src_addr)
        inputObject.continent = info.continent
        inputObject.country = info.country
        inputObject.network = info.network
        inputObject.netmask = info.prefix
        
        # Faster analytics will treat "NA" as missing.
        #   missing values themselves should be given specific values as well
        if(inputObject.continent == "NA"):
            inputObject.continent = "NoA"
        if(inputObject.continent == None):
            inputObject.continent = GeoIP.missingValue
        if(inputObject.country == None):
            inputObject.country = GeoIP.missingValue
        # print "Geo Info: %s"%info
        