from collector.base import PluginBase
class SamplePlugin(PluginBase):
    def __init__(self):
        #overridden init
        print "Sample Plugin inherited init"
    def run(self):
        print "Sample Plugin overridden run"
        return super(SamplePlugin,self).run()
    def _run(self):
        print "Sample Plugin overridden _run"
        return None