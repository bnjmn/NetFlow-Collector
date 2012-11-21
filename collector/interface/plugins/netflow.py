import dpkt

class NetFlowV5(object):
    
    def run(self,data):
        nf = dpkt.netflow.Netflow5(data) 
        #we are not using the header portion of the NetFlow Flow, only the NetFlow records
        #    so we are just returning the array of NetFlow Records, which is an iterable
        return nf.data      