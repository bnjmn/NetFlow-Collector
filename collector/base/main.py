import utils.settings as Settings
import os, imp

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

        self.plugins = self.config.get(self.stage,"plugins")       
        mods = self.load_modules(self.config.get(self.stage,"pluginsdir"))
        
        self.mods = {}
        for key in mods.keys():
            self.mods.update(dict([(name, cls) for name, cls in mods[key].__dict__.items() if isinstance(cls, type) and name in self.plugins]))  
        
    def run(self,data):
        #for each mod create a instance and run it
        if self.mods:
            for key in self.mods:
                return self.mods[key]().run(data)
  
class PluginBase(object):
    def __init__(self):
        #override this
        #implement some init code here
        print "PluginBase init"
    def run(self, *args, **kwargs):
        #override this
        #implement some init code here
        print "PluginBase run"
        return self._run()
    def _run(self):
        #override this
        #implement some code here
        print "PluginBase _run"
        return None
        
