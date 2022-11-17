import random
import re
from time import sleep
from typing import List
import requests
import bs4
import os
from DataBase import *
from data import artistlist,artistlist_len
import time
class Craw():
    root_dir=os.path.dirname(os.path.realpath(__file__))
    def __init__(self,tag='',number=500,imagepath=os.path.join(root_dir,'download'),searchnum=20000):
        self.db=DataBase()
        self.headers={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
            'host':'gelbooru.com',
            'referer':'https://gelbooru.com/',
        }
        self.tag=tag
        self.download_num=number#下载个数
        self.imagecontent=''
        self.imagepath=imagepath
        downloaded=self.db.selectTable('SELECT Picid from Picture WHERE download = "1"')
        self.downloaded=[int(x[0]) for x in downloaded]
        self.search=searchnum
    
    def getResponse(self,url='https://gelbooru.com/index.php?',sleeptime=1,**params):
        '''获取页面内容'''
        try:
            response=requests.get(url,headers=self.headers,params=params)
        except Exception as e:
            print(e)
            return 0
        sleep(random.randint(0,int(sleeptime))/2)
        return response 

    def getSoup(self,id):
        '''生成供解析的soup'''
        params={'page': 'post','s': 'view','id':id,}
        if(response:=self.getResponse(**params)):
            html=response.text
            soup=bs4.BeautifulSoup(html,'html.parser')
            return soup
        return 0
    def formatTag(self,tags:list[bs4.BeautifulSoup]):
        '''将由beautifulsoup检索来的结果转化为列表'''
        tags=[x.text for x in tags]
        tags=list(set(tags))
        if('?' in tags):tags.remove('?')
        return tags
    def getTags(self,id):
        '''由soup获取图片的信息'''
        if(soup:=self.getSoup(id)):
            try:
                artist = self.formatTag(soup.select('.tag-type-artist a'))
                char = self.formatTag(soup.select('.tag-type-character a'))
                copyright = self.formatTag(soup.select('.tag-type-copyright a'))
                metadata = self.formatTag(soup.select('.tag-type-metadata a'))
                tag = self.formatTag(soup.select('.tag-type-general a'))
                origin_url = soup.select('.fit-width')[0]['src']
                masterjs = soup.select('script')[-1].text
                master_url = re.findall('image\.attr\(\'src\',\'(.+)\'\);\n', masterjs)[0]
                tags = {
                    'Picid':id,
                    'artist': ','.join(artist),
                    'character': ','.join(char),
                    'copyright': ','.join(copyright),
                    'metadata': ','.join(metadata),
                    'tag': ','.join(tag),
                    'origin_url': origin_url,
                    'master_url': master_url
                }
                return tags
            except Exception as e:
                #print(e)
                pass
        return 0
    
    def getListSoup(self,pid:str):
        '''生成供解析的soup'''
        tag=' '.join(tag.replace(' ','_') for tag in self.tag)
        params={'page': 'post','s': 'list','tags':tag,'pid':pid}
        if(response:=self.getResponse(**params)):
            html=response.text
            soup=bs4.BeautifulSoup(html,'html.parser')
            return soup
        return 0
    def getPicid(self):
        '''通过tag获取图片id'''
        start=time.time()#时间
        id_list=[]
        pidmax=self.search
        for pid in range(0,pidmax,42):
            soup=self.getListSoup(str(pid))
            if(soup):
                html_list=soup.select('article a')
                html_list=[x['id'][1:] for x in html_list]
                if(len(html_list)==0):break
                id_list+=html_list
        print()
        end=time.time()#时间
        tag=' '.join(tag.replace(' ','_') for tag in self.tag)
        print('标签{}获取{}张图片信息,耗时:{:.2f}s'.format(tag,len(id_list),end-start))#side effect
        return id_list
    
    def makedirs(self,path):
        '''创建文件夹'''
        if not os.path.exists(path):
            os.makedirs(path)

        
    def saveImage(self,name):
        '''保存图片'''
        self.makedirs(self.imagepath)
        path=os.path.join(self.imagepath,name)
        try:
            with open(path,'wb') as f:
                f.write(self.imagecontent)
                return 1
        except:
            return 0
            
    def downLoad(self,insert=True):
        '''下载图片'''
        list=self.getPicid()
        count=0
        for id in list:
            if(int(id) in self.downloaded and insert):#已下载就跳过
                continue
            if(tag_dict:=self.getTags(id)):
                #数据库连接
                url=tag_dict['origin_url']
                name=id+'.'+url.split('.')[-1]
                insert_data=dict(self.db.predownload_dict,**tag_dict)
                self.db.insertData(**insert_data)
                try:#尝试下载
                    res=self.getResponse(url=url)
                    self.imagecontent=res.content
                    self.saveImage(name)
                    insert_data['download']='1'
                    insert_data['local_path']=os.path.join(self.imagepath,name)
                    count+=1
                    if(insert):
                        self.db.insertData(**insert_data)
                except:
                    continue
                if(count>=self.download_num):break
        return count

    def downLoadwithInform(self,insert=True):
        list=self.getPicid()
        templist=[]
        for id in list:
            if((int(id) in self.downloaded) and (insert)):#已下载就跳过
                pass
            else:
                templist.append(id)
        list=templist
        count=0 #下载成功计数
        tried=0 #尝试下载计数
        scheduled_num=len(list)if len(list)<(self.download_num) else self.download_num
        
        def show():
            length=50
            rate=tried/scheduled_num
            done=int(length*rate)
            undo=length-done
            print("当前进度{0:>5.1f}%:[{1}->{2}]{3}/{4}".format(rate*100,'▓'*done,'-'*undo,tried,scheduled_num))
        
        for id in list:
            if(tag_dict:=self.getTags(id)):
                tried+=1
                #数据库连接
                url=tag_dict['origin_url']
                name=id+'.'+url.split('.')[-1]
                insert_data=dict(self.db.predownload_dict,**tag_dict)
                self.db.insertData(**insert_data)
                try:#尝试下载
                    res=self.getResponse(url=url)
                    self.imagecontent=res.content
                    self.saveImage(name)
                    insert_data['download']='1'
                    insert_data['local_path']=os.path.join(self.imagepath,name)
                    count+=1
                    if(insert):
                        self.db.insertData(**insert_data)
                except:
                    continue
                show()
                if(count>=self.download_num):break
        print('结束')
        
    


        



if __name__=='__main__':
    download_one_time=200#单次下载数量
    root_dir=os.path.dirname(os.path.realpath(__file__))
    # c_list:List[Craw]=[]    #存储爬虫对象

    #特地下载
    down_num=200
    c=Craw(['genshin_impact'],number=down_num,searchnum=1000)
    #c.downLoadwithInform()
    
    #更新作者列表作品
    down_num=15
    for artist in artistlist:
        c=Craw(artist,number=down_num)
        c.downLoadwithInform()

