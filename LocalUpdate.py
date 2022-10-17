import shutil
from DataBase import *
from Craw import *
import sys
class LocalUpdate():
    '''处理本地的历史文件'''
    def __init__ (self):
        self.db=DataBase()
        self.craw=Craw()
        self.realpath=os.path.dirname(os.path.realpath(__file__))
        piclist=self.db.selectTable('SELECT Picid from Picture WHERE download = "1" AND delet = "0"')
        self.piclist=[str(x[0]) for x in piclist]
        piclist=self.db.selectTable('SELECT Picid from Picture WHERE download = "1"')
        self.txt_piclist=[str(x[0]) for x in piclist]
        self.exist_add_dict={'master':'0','delet':'0','download':'1'}
        self.txt_add_dict={'master':'0','delet':'1','download':'1'}#默认已经删掉了
        self.accepted_format=['jpg','png','jpeg','gif']
    
    def updateDownloaded(self,path,default=1):#default为0为涩图
        '''将一个dir下的全部图片计入数据库'''
        for root, dirs, files in os.walk(path):
            for file in files:
                try:
                    picid=file.split('.')[0]
                    format=file.split('.')[-1]
                except:
                    print('IN FUNCTION updateDownloaded():format error')
                    continue
                if(not picid.isdigit()):#不是纯数字,去除
                    continue
                if(int(picid)<100000):#剔除不是G站图源的图片
                    continue
                if(format not in self.accepted_format):#不是指定格式就跳过
                    continue
                if (picid not in self.piclist):
                    path=os.path.join(root,file)
                    insert_data=self.exist_add_dict.copy()
                    insert_data['local_path']=path
                    if default:insert_data['green']='1'
                    if(tag_dict:=self.craw.getTags(picid)):
                        insert_data=dict(insert_data,**tag_dict)
                        self.db.insertData(**insert_data)
                    else:
                        print('IN FUNCTION updateDownloaded():{}tags get failed'.format(picid))
                        shutil.move(os.path.join(root,file),'err')
                        pass
    
    def updateTxt(self,path='.//txt'):
        '''把之前筛选掉的补上'''
        file_list=os.listdir(path)
        for file in file_list:
            if(file.split('.')[-1]!='txt'):#不是txt文件就跳过
                continue
            filepath=os.path.join(path,file)
            with open(filepath,'r',encoding='utf-8') as f:
                id_list=f.read().split(',')
                for id in id_list:
                    if(id in self.txt_piclist):#已经在表内就不更新
                        continue
                    insert_data=self.txt_add_dict.copy()
                    insert_data['Picid']=id
                    self.db.insertData(**insert_data)
        
    def updatePicPath(self,path):
        '''更新图片路径'''
        for root, dirs, files in os.walk(path):
            # picpath=os.path.join(path,root,)
            for file in files:
                picid=file.split('.')[0]
                realpath=os.path.join(self.realpath,root,file)
                dbpath=self.db.genSelectSql(Tablename='Picture',target=['local_path'],**{'Picid':picid})[0][0]
                if(os.path.exists(dbpath)):
                    continue
                self.db.genUpdateSql(Tablename='Picture',condition={'Picid':picid},**{'local_path':realpath})
                # print(dbpath[0][0])
                # print(realpath)
                #print(os.path.join(root,file))

if __name__=='__main__':
    root_dir=os.path.dirname(os.path.realpath(__file__))
    m=LocalUpdate()
    #m.updateDownloaded('.\\pic')
    #m.updateTxt()
    #m.updateDownloaded("D:\\Users\\admin\Desktop\\机器人\\Yunzai-Bot\plugins\\miao-plugin\\resources\\character-img\\云堇")
    #m.updateDownloaded('.\\download')
    m.updateDownloaded(os.path.join(root_dir,'Pictures'),default='1')
    m.updateTxt()


