from collector.base import PlugableBase

import utils.settings as Settings

class Score(PlugableBase):
    def __init__(self):
        self.stage = "score"
        return super(Score,self).__init__()

if __name__ == '__main__':
    pass