#from Demo1 import *
import os
root_dir=os.path.basename(__file__)
print(root_dir)
# file_path=os.path.join(root_dir,'pic')
# # print(file_path)
# print(os.listdir(root_dir))
# root_absdir = os.path.abspath(os.path.dirname(__file__))
# path=os.path.split(os.path.realpath(__file__))[0]
# print(root_absdir)
# for root,dirs,names in os.walk(root_dir):
#     for filename in names:
#       print(os.path.join(root,filename)) #路径和文件名连接构成完整路径