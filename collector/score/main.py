from collector.base import PlugableBase

import sys

import utils.settings as Settings

class Score(PlugableBase):
    def __init__(self):
        self.stage = "score"
        print sys.executable 
        return super(Score,self).__init__()

if __name__ == '__main__':
    pass