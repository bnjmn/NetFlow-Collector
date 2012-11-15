import dpkt

class NetFlowV5(object):
    def __init__(self,*args):
        pass
    
    def numIP2strIP(self,ip):
        '''
        this function convert decimal ip to dot notation
        '''
        l = [str((ip >> 8*n) % 256) for n in range(4)]
        l.reverse()
        return ".".join(l)
    
    def run(self,data):
        #do something meaningful
        self.flow = dpkt.netflow.Netflow5(data)
        print self.numIP2strIP(self.flow.data[0].src_addr)
        #return something meaningful
        return self.flow