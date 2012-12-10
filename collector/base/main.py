import utils.settings as Settings
import os, imp, datetime
  
class PlugableBase(object):
   
    def load_modules(self,path):       
        mods = {}
        if path:
            dir_list = os.listdir(path)
            for fname in dir_list:
                name, ext = os.path.splitext(fname)
                if ext == '.py' and not name == '__init__':
                    f, filename, descr = imp.find_module(name, [path])
                    mods[name] = imp.load_module(name, f, filename, descr)
        return mods

    def __init__(self, *args, **kwargs):
        self.config = Settings.SETTINGS

        self.plugins = self.config.getlist(self.config.get(self.stage,"plugins"))       
        mods = self.load_modules(self.config.get(self.stage,"pluginsdir"))
        
        self.mods = {}
        for key in mods.keys():
            self.mods.update(dict([(name, cls) for name, cls in mods[key].__dict__.items() if isinstance(cls, type) and name in self.plugins]))  
            
        #create running instances; forces singleton
        self.modInstances={}
        for key in self.mods:
            self.modInstances[key]= self.mods[key]()
        
    def run(self,dataObject):
        for key in self.modInstances:
            self.modInstances[key].run(dataObject)
        return dataObject
  
class PluginBase(object):
    def __init__(self):
        #override this
        #implement some init code here
        #print "PluginBase init"
        pass
    def run(self, *args, **kwargs):
        #override this
        #implement some init code here
        #print "PluginBase run"
        return self._run()
    def _run(self):
        #override this
        #implement some code here
        #print "PluginBase _run"
        return None

class DecimalToDotIP(PluginBase):
    def numIP2strIP(self,ip):
        '''
        this function convert decimal ip to dot notation
        '''
        l = [str((ip >> 8*n) % 256) for n in range(4)]
        l.reverse()
        return ".".join(l)
    
class DateTimeSinceEpoch(PluginBase):
    def getDateTime(self,secsSinceEpoch):
        return datetime.datetime.utcfromtimestamp(secsSinceEpoch)

#TODO: expand with more dynamic methods
class ScorePlug(PluginBase):
    datadigestDir = str(Settings.SETTINGS.get("score","datadigestDir"))
    pyPath = "-Dpython.path=" + str(datadigestDir)
    jythonExe = "./score/JythonBI.py"
        
    def runBatchInference(self, inputObject):
        #print "Hello runBatchInference"
        pass
