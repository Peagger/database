import random
import re
from time import sleep
import requests
import bs4
import os
from DataBase import *
import time
class Craw():

    def __init__(self,tag='',imagepath='.\\download',number=500):
        self.db=DataBase()
        self.headers={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
            'host':'gelbooru.com',
            'referer':'https://gelbooru.com/',
        }
        self.tag=tag
        self.search_number=number#检索个数
        self.imagecontent=''
        self.imagepath=imagepath
        self.downloaded=self.db.selectTable('SELECT Picid from Picture WHERE download = "1"')
    
    def getResponse(self,url='https://gelbooru.com/index.php?',sleeptime=1,**params):
        '''获取页面内容'''
        try:
            response=requests.get(url,headers=self.headers,params=params)
        except Exception as e:
            print(e)
            pass
        sleep(random.randint(0,int(sleeptime))/2)
        return response if (response) else 0

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
            except:
                #print(Exception)
                pass
        return 0
    
    def getListSoup(self,pid:str):
        '''生成供解析的soup'''
        tag=self.tag.replace(' ','_')
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
        for pid in range(0,self.search_number,42):
            soup=self.getListSoup(str(pid))
            if(soup):
                html_list=soup.select('article a')
                html_list=[x['id'][1:] for x in html_list]
                id_list+=html_list
        print()
        end=time.time()#时间
        print('{}张图片信息,耗时:{:.2f}s'.format(len(id_list),end-start))#side effect
        return id_list
    
    def makedirs(self,path):
        '''创建文件夹'''
        if not os.path.exists(path):
            os.makedirs(path)

        
    def saveImage(self,name):
        '''保存图片'''
        self.makedirs(self.imagepath)
        path=os.path.join(self.imagepath,name)
        with open(path,'wb') as f:
            f.write(self.imagecontent)
            return 1
        return 0
            
    def downLoad(self):
        '''下载图片'''
        list=self.getPicid()
        for id in list:
            if(id in self.downloaded):#已下载就跳过
                continue
            if(tag_dict:=self.getTags(id)):
                #数据库连接
                url=tag_dict['origin_url']
                name=id+'.'+url.split('.')[-1]
                insert_data=dict(self.db.predownload_dict,**tag_dict)
                self.db.insertData(**insert_data)
                try:
                    res=self.getResponse(url=url)
                    insert_data['download']='1'
                    insert_data['local_path']=os.path.join(self.imagepath,name)
                    self.db.insertData(**insert_data)
                except:
                    continue
                self.imagecontent=res.content
                self.saveImage(name)

        
    


        



if __name__=='__main__':
    c=Craw('genshin impact',number=300)
    c.downLoad()