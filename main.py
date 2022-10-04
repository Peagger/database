import random
import re
from time import sleep
import requests
import bs4
class Craw():

    def __init__(self):
        self.headers={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
            'host':'gelbooru.com',
            'referer':'https://gelbooru.com/',
        }
    
    def getResponse(self,url='https://gelbooru.com/index.php?',sleeptime=1,**params):
        try:
            response=requests.get(url,headers=self.headers,params=params)
        except Exception as e:
            print(e)
        sleep(random.randint(0,int(sleeptime))/2)
        return response if (response) else 0

    def getSoup(self,id):
        params={'page': 'post','s': 'view','id':id,}
        if(response:=self.getResponse(**params)):
            html=response.text
            soup=bs4.BeautifulSoup(html,'html.parser')
            self.getTags(soup)
    
    def getTags(self,soup:bs4.BeautifulSoup):
        artist = self.formatTag(soup.select('.tag-type-artist a'))
        char = self.formatTag(soup.select('.tag-type-character a'))
        copyright = self.formatTag(soup.select('.tag-type-copyright a'))
        metadata = self.formatTag(soup.select('.tag-type-metadata a'))
        tag = self.formatTag(soup.select('.tag-type-general a'))
        origin_url=soup.select('.fit-width')[0]['src']
        masterjs=soup.select('script')[-1].text
        master_url=re.findall('image\.attr\(\'src\',\'(.+)\'\);\n',masterjs)[0]
        print(master_url)
    
    def formatTag(self,tags:list[bs4.BeautifulSoup]):
        '''将由beautifulsoup检索来的结果转化为列表'''
        tags=[x.text for x in tags]
        tags=list(set(tags))
        tags.remove('?')
        return tags


        



if __name__=='__main__':
    c=Craw()
    c.getSoup('6730018')