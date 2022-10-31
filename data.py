

artistlist=[]#作者列表
artistlist_len=0

with open('Artist.txt','r') as f:
    artistlist=f.read().split('\n')
    artistlist=[[x]for x in artistlist]
    artistlist_len=len(artistlist)
