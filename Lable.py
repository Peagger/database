import os
import shutil
import cv2
import os.path as op
from DataBase import *
from Craw import *
from LocalUpdate import *


root_dir=os.path.dirname(os.path.realpath(__file__))
os.chdir(root_dir)
class Lable():
    def __init__(self,resize=0.6,path='download',savedir='Pictures'):
        self.accepted_format=['jpg','png','jpeg']
        self.resize=resize
        self.hight=1600*self.resize
        self.width=2560*self.resize
        self.image_list=os.listdir(op.join(root_dir,path))
        self.path=path
        self.savedir=savedir
        self.kind=3
        self.record=[]#记录执行的操作
        self.movedpic=[]
        self.db=DataBase()
        self.craw=Craw()
        self.Update=LocalUpdate()

    def showimage(self):
        '''显示'''
        leftkeys = (81, 110, 65361, 2424832)
        rightkeys = (83, 109, 65363, 2555904)
        i=0
        image_list=self.image_list.copy()
        #print('790715.jpg' in image_list)
        for image in image_list:
            if(image.split('.')[-1] not in self.accepted_format):
                image_list.remove(image)
        length=len(image_list)#图片数量
        if(length==0):print('请在{}文件夹下放入图片'.format(self.path));return
        while True:
            
            i=i%len(image_list)
            if (i in self.movedpic):
                if (len(self.movedpic)!=length):
                    i=i+1;continue
                else:
                    print('好耶,分类完毕!')
                    break
            #读取图片
            image_path=op.join('./',self.path,image_list[i])
            try:
                image=cv2.imread(image_path)
                hight,width = image.shape[:2]
            except:
                i=i+1
                continue
            print('第{}张'.format(i+1))
            cv2.destroyAllWindows()
            #缩放图片比例
            
            ratioOfHight=self.hight/hight
            ratioOfwidth=self.width/width
            ratio=0
            if ratioOfHight<1:      ratio=ratioOfHight
            if ratioOfwidth<ratio:  ratio=ratioOfHight
            if ratio:
                image=cv2.resize(image,(int(width*ratio),int(hight*ratio)),interpolation=cv2.INTER_AREA)
            #窗口设置
            cv2.imshow('classify', image)
            #cv2.moveWindow(image_list[i],100,200)
            pressedKey=cv2.waitKeyEx()
            #print('当前输入: ',pressedKey,pressedKey&0xff)

            if (pressedKey==-1)or(pressedKey&0xff==27):break
            insert_data={'Picid':image_list[i].split('.')[0],'delet':'0','green':'0'}
            if (pressedKey in leftkeys):#撤回
                if(len(self.record)>0):
                    act=self.record.pop()#先入先出
                    i=(i-1+length)%length
                    if(act[0]==-1):
                        continue
                    else:
                        i=act[0]
                        self.movedpic.remove(act[0])
                        insert_data['Picid']=image_list[act[0]].split('.')[0]
                        insert_data['local_path']=op.join(act[2],image_list[act[0]])
                        self.db.insertData(**insert_data)
                        shutil.move(act[1],act[2])
                        continue
                else:
                    i=(i-1+length)%length
                    continue
            if (pressedKey in rightkeys):
                i+=1
                self.record.append([-1])
                continue
            if(pressedKey&0xff==ord(str(3))):   #delet=1
                try:
                    shutil.move(image_path,'.\delet')
                except Exception as e:
                    print(e)
                    break
                self.record.append([i,op.join(root_dir,'.\delet',image_list[i]),op.join(root_dir,self.path)])
                insert_data['delet']='1'
                #insert_data['local_path']=op.join(root_dir,'.\delet',image_list[i])
                self.db.insertData(**insert_data)
                self.movedpic.append(i)
                continue
            if(pressedKey&0xff==ord(str(2))):
                try:
                    shutil.move(image_path,self.savedir)
                    print(image_path,self.savedir)
                except:
                    os.remove(image_path)
                    print('重复,删除')
                else:
                    self.record.append([i,op.join(root_dir,self.savedir,image_list[i]),op.join(root_dir,self.path)])
                    insert_data['local_path']=op.join(root_dir,self.savedir,image_list[i])
                    self.db.insertData(**insert_data)
                finally:
                    self.movedpic.append(i)
                    continue
            if(pressedKey&0xff==ord(str(1))):   #green=1
                try:
                    shutil.move(image_path,self.savedir)
                    print(image_path,self.savedir)
                except:
                    os.remove(image_path)
                    print('重复,删除')
                else:
                    self.record.append([i,op.join(root_dir,self.savedir,image_list[i]),op.join(root_dir,self.path)])
                    insert_data['green']='1'
                    insert_data['local_path']=op.join(root_dir,self.savedir,image_list[i])
                    self.db.insertData(**insert_data)
                finally:
                    self.movedpic.append(i)
                    continue

if __name__=='__main__':
    classify=Lable()
    classify.showimage()
    #print(classify.image_list)
    print('程序结束')


        