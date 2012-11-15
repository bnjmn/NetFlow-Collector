'''
Created on Nov 13, 2012

@author: rob
'''
from collector.base import PlugableBase

import utils.settings as Settings

class Standardize(PlugableBase):
    def __init__(self):
        self.stage = "standardize"
        return super(Standardize,self).__init__()

if __name__ == '__main__':
    pass