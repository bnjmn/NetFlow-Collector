from collector.base import PluginBase

class TcpFlags(PluginBase):
    '''
    hoping that the flags match what snort does
    where fin=1,syn=2,rst=4,psh=8,ack=16,urg=32,ece=64,cwr=128
    
    Flags (6x1 bit): The flags represent additional information:
    URG: if this flag is set to 1 the packet must be processed urgently
    ACK: if this flag is set to 1 the packet is an acknowledgement.
    PSH (PUSH): if this flag is set to 1 the packet operates according to the PUSH method.
    RST: if this flag is set to 1 the connection is reset.
    SYN: The TCP SYN flag indicates a request to establish a connection.
    FIN: if this flag is set to 1 the connection is interrupted.
    '''
    flags = ["FIN","SYN","RST","PSH","ACK","URG","ECE","CWR"]
    def run(self,inputObject):
        #inputObject is a Flow Record at this point
        #l = [((inputObject.tcp_flags >> n)&0x1) for n in range(8)]
        inputObject.tcp_flags = {TcpFlags.flags[n]:((inputObject.tcp_flags >> n)&0x1) for n in range(8)}
        #print "TCP Flags 1: %s %s"%(inputObject.tcp_flags,d)     
        #no need to return anything since we are modding by reference