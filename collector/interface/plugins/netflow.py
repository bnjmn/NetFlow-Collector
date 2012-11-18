import dpkt

class NetFlowV5(object):
    
    def run(self,data):
        #do something meaningful
        return dpkt.netflow.Netflow5(data)       