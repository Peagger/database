from DataBase import *
from Craw import *
import sys
class LocalUpdate():
    
    def __init__ (self):
        self.db=DataBase()
        self.craw=Craw()
        piclist=self.db.selectTable('SELECT Picid from Picture WHERE download = "1"')
        self.piclist=[str(x[0]) for x in piclist]
        self.addict={'master':'0','delet':'0','download':'1'}
    
    def updateDownloaded(self,path):
        for root, dirs, files in os.walk(path):
            for name in files:
                picid=name.split('.')[0]
                if (picid not in self.piclist):
                    path=os.path.join(root,name)
                    self.addict['local_path']=path
                    if(tag_dict:=self.craw.getTags(name.split('.')[0])):
                        insert_data=dict(self.addict,**tag_dict)
                        self.db.insertData(**insert_data)
                    else:
                        print('tags get failed')
                        pass
        
        


if __name__=='__main__':
    m=LocalUpdate()
    m.updateDownloaded('.\\pic')
