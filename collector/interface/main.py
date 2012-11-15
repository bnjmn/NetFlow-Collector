from collector.base import PlugableBase

import utils.settings as Settings

class Interface(PlugableBase):
    def __init__(self):
        self.stage = "interface"
        super(Interface,self).__init__()