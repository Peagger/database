

artistlist=[]#作者列表
artistlist_len=0

with open('Artist.txt','r') as f:
    artistlist=f.read().split('\n')
    artistlist=[[x]for x in artistlist]
    artistlist_len=len(artistlist)
# j=['a','b','c',1,2,3]
# k=['a','b','c']
# for i in j:
#     print(i)
#     if(i in k):j.remove(i)
# print(j)
