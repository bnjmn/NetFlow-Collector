'''
Created on Nov 13, 2012

@author: rob
'''
from collector.base import PlugableBase

import utils.settings as Settings

class Partition(PlugableBase):
    def __init__(self):
        self.stage = "partition"
        return super(Partition,self).__init__()

if __name__ == '__main__':
    pass