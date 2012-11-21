'''
Created on Nov 5, 2012

@author: rob
'''
import ConfigParser
import os
import logging
CONFIGFILE = "config.ini"

class settings(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        
        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # add formatter to ch
        ch.setFormatter(formatter)
        
        # add ch to logger
        self.logger.addHandler(ch) 
        self.logger.info( "Initializing Settings")
        self.config = ConfigParser.ConfigParser()
        self.config.read(CONFIGFILE)
        
    def getlist(self,option, sep=',', chars=None):
        return [ chunk.strip(chars) for chunk in option.split(sep) ]
    
    def get(self,section,key):
        try:
            return self.config.get(section,key)
        except ConfigParser.NoSectionError:
            self.logger.warn("Config.ini has no %s section or section key %s is missing"%(section,key))
            return None
        
SETTINGS = settings()