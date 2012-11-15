'''
Created on Nov 13, 2012

@author: rob
'''
from collector.base import PlugableBase

import utils.settings as Settings

class Transform(PlugableBase):
    def __init__(self):
        self.stage = "transform"
        return super(Transform,self).__init__()

if __name__ == '__main__':
    pass