from DataBase import *
from Craw import *
import sys
class Main():
    
    def __init__ (self):
        self.db=DataBase()
        self.craw=Craw()
        piclist=self.db.selectTable('SELECT Picid from Picture')
        self.piclist=[str(x[0]) for x in piclist]
        self.addict={'master':'0','delet':'0','download':'1'}
    
    def updateDownloaded(self,path):
        for root, dirs, files in os.walk(path):
            for name in files:
                picid=name.split('.')[0]
                if (picid not in self.piclist):
                    path=os.path.join(root,name)
                    self.addict['Picid']=int(picid)
                    self.addict['local_path']=path
                    tag_dict=self.craw.getTags(name.split('.')[0])
                    combine=dict(self.addict,**tag_dict)
                    self.db.insertData(**combine)
        
        


if __name__=='__main__':
    m=Main()
    m.updateDownloaded('.\\pic')
