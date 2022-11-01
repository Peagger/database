

artistlist=[]#作者列表
artistlist_len=0

with open('Artist.txt','r') as f:
    artistlist=f.read().split('\n')
    artistlist=[[x]for x in artistlist]
    artistlist_len=len(artistlist)
# total=11
# a=0
# def show():
#     length=20
#     rate=a/total
#     done=int(length*rate)
#     undo=length-done
#     print("当前进度{0:>5.1f}%:[{1}->{2}]{3}/{4}".format(rate*100,'▓'*done,'-'*undo,a,total))

# for i in range(0,12):
#     a=i
#     show()