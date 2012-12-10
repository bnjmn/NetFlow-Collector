import csv
import utils.settings as Settings

class CSV(object):
    def __init__(self,outFileName):
        self.fileHandle = open(outFileName,"wt")
        fieldnames = Settings.SETTINGS.getlist(Settings.SETTINGS.get("csv","fieldNames"))
        self.csvWriter = csv.DictWriter(self.fileHandle,fieldnames=fieldnames)        
        self.csvWriter.writeheader()
    
    def format(self,row): 
        return {key:getattr(row,key) for key in Settings.SETTINGS.getlist(Settings.SETTINGS.get("csv","fieldNames"))}
   
    def writeRows(self,rows):
        self.csvWriter.writerows(rows)
        
    def writeRow(self,row):
        #print "Final output %s"%repr(row)
        self.csvWriter.writerow(row)
        
    def __del__(self):
        #print "closing CSV"
        self.fileHandle.close()
        
    