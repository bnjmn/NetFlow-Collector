from collector.base import PlugableBase

import utils.settings as Settings
class Parse(PlugableBase):
    def __init__(self):
        self.stage = "parse"
        return super(Parse,self).__init__()
    def parse(self):
        pass