'''
Created on Nov 5, 2012

@author: rob
'''
import ConfigParser
import os

CONFIGFILE = "config.ini"

class settings(object):
    def __init__(self):
        print "Initializing Settings"
        self.config = ConfigParser.ConfigParser()
        self.config.read(CONFIGFILE)
        
    def getlist(self,option, sep=',', chars=None):
        return [ chunk.strip(chars) for chunk in option.split(sep) ]
    
    def get(self,section,key):
        try:
            return self.config.get(section,key)
        except ConfigParser.NoSectionError:
            return None
        
SETTINGS = settings()