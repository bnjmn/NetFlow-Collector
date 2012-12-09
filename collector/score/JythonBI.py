import sys
import ast
import java

from jarray import array, zeros
from java.lang import System
from java.io import PrintStream, OutputStream

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)
#count = 0 
#for arg in sys.argv:
#    print "ARG[%s]="%count + arg + " : CLASS=%s"%arg.__class__
#    count += 1

#Assuming args as: {file.py, data.csv, model.bn5, ['outs'], ['thrus']}
#TODO: add more robust input checks
if len(sys.argv) < 5:
    print 'Not enough args'

class NoOutputStream(OutputStream):
    def write(self, b, off, len): pass

data = sys.argv[1]
model = sys.argv[2]
outs = ast.literal_eval(sys.argv[3])
thrus = ast.literal_eval(sys.argv[4])

oldOut = System.out
System.setOut(PrintStream(NoOutputStream()))
import datadigest.inference.BatchInferenceFacade as BatchInferenceFacade
bi = BatchInferenceFacade(data, model, outs, thrus)
results = bi.runBatchInference()
length = results.available()
buff = zeros(length, 'b')
results.read(buff)
theChars = ''
for i in range(1,length+1):
    theChars += chr(buff[i-1])
print (str(theChars))