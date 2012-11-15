'''
Created on Nov 13, 2012

@author: rob
'''
from collector.base import PlugableBase

import utils.settings as Settings

class Describe(PlugableBase):
    def __init__(self):
        self.stage = "describe"
        return super(Describe,self).__init__()

if __name__ == '__main__':
    pass