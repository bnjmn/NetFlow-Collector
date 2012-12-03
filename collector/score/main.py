from collector.base import PlugableBase

# from subprocess import call
import utils.settings as Settings

class Score(PlugableBase):
    # datadigestDir = str(Settings.SETTINGS.get("score","datadigestDir"))
    
    def __init__(self):
        self.stage = "score"
        # print sys.executable
        # print "ddDIR=%s"%("-Djava.class.path=" + self.datadigestDir )
                
        return super(Score,self).__init__()

if __name__ == '__main__':
    pass