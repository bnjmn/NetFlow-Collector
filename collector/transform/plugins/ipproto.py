from collector.base import PluginBase

class IpProto(PluginBase):
    '''
    from rfc5237 http://www.iana.org/assignments/protocol-numbers/protocol-numbers.xml    
    '''
    protocols = {6:"TCP",1:"ICMP",17:"UDP"} #<------add other protocols from http://www.iana.org/assignments/protocol-numbers/protocol-numbers.xml here
    def run(self,inputObject):
        if(inputObject.ip_proto in IpProto.protocols):
            inputObject.ip_proto = IpProto.protocols[inputObject.ip_proto]
        else:
            inputObject.ip_proto = "OTHER"
        print "IP Proto %s"%inputObject.ip_proto 
        
        
        
        
        
        
        