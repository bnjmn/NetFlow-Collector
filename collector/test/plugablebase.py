from collector.base import PlugableBase
import utils.settings as Settings

class a(PlugableBase):
    def __init__(self):
        self.stage = "parse"
        super(a,self).__init__()

def main():
    print repr(Settings)
    myA = a()
    myA.run()
    
    
if __name__ == '__main__':
    main()