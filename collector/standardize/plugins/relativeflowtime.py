'''
Created on Nov 27, 2012

@author: benjamin
'''
from collector.base import PluginBase
from collector.base import DateTimeSinceEpoch

class RelativeFlowTime(DateTimeSinceEpoch):
    '''
    Get Time in seconds of Flow from start_time to end_time
    TODO: Fix Time ingestion. 
        Check SoftFlowd. Does not seem to be TimeSinceEpoch. Ranges are too big and everything is in year 2073
        Same packets generate different times when rerun; Is this what we want
    '''
    def run(self,inputObject):
        # print "endtime =  %s"%self.getDateTime(inputObject.end_time)
        # print "starttime =  %s"%self.getDateTime(inputObject.start_time)
        diff_time = (self.getDateTime(inputObject.end_time) - self.getDateTime(inputObject.start_time)).total_seconds()
        # print "difftime.secs =  %s"%diff_time
        
        inputObject.__setattr__("flow_time", str(diff_time))
        # temp = inputObject.end_time - inputObject.start_time
        
        
    