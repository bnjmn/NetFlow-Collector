from collector.base import DecimalToDotIP

class NextHop(DecimalToDotIP):

    def run(self,inputObject):
        #inputObject is a Flow Record at this point
        try:
            inputObject.next_hop = self.numIP2strIP(inputObject.next_hop)
            print "next_hop: %s"%inputObject.next_hop
        except AttributeError:
            print "Next hop empty"
        #no need to return anything since we are modding by reference