from collector.base import DecimalToDotIP

class SrcAddr(DecimalToDotIP):

    def run(self,inputObject):
        #inputObject is a Flow Record at this point
        inputObject.src_addr = self.numIP2strIP(inputObject.src_addr)
        print "Src Addr: %s"%inputObject.src_addr
        #no need to return anything since we are modding by reference