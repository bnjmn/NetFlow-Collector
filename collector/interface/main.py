from collector.base import PlugableBase

import utils.settings as Settings

'''
    This class's plugins must return an iterable!!! The Collector main line application expects to iterate over
        the results of this class's plugins' .run() result
'''
class Interface(PlugableBase):
    def __init__(self):
        self.stage = "interface"
        super(Interface,self).__init__()