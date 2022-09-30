import sqlite3

class Data():
    def __init__(self,id,**dict):
        self.id=id
        self.master     =0  #是否为原图
        self.download   =0  #下载是否成功
        self.dict       =dict   #图片标签
        # self.origin_url =dict.get('origin_url')
        # self.artist     =dict.get('artist')
        # self.character  =dict.get('character')
        # self.metadata   =dict.get('matadata')
        # self.tag        =dict.get('tag')
    def downloadMark(self):
        '''下载成功后标记'''
        self.download=1
    def masterMark(self):
        '''下载原图后标记'''
        self.master=1
    def updateDic(self,**dict):
        '''更新图片标签'''
        for key,value in dict.items():
            self.dict[key]=value
    def show(self):
        '''打印全部私有变量'''
        print("id:{}".format(self.id),end=' ')
        print("是否原图:{},是否下载成功{}".format(self.master,self.download))
        print(self.dict)    

class DataBase():
    
    def __init__(self,db='GelPic.db'):
        self.connection=sqlite3.connect(db)
        self.cur=self.connection.cursor()
        self.insert_sql=''
        self.create_sql='''
                create table Picture(
                id integer primary key,
                local_path text,
                master text,
                download text,
                artist text,
                character text,
                copyright text,
                metadata text,
                tag text,
                origin_url text,
                master_url text)
    '''
        self.data=''
        
    def createTable(self):
        '''创建表'''
        try:
            self.cur.execute(self.create_sql)
            print('创建表成功')
            return 1
        except Exception as e:
            print(e)
            print('创建表失败')
            return 0
    def genInsertSql(self,**dict):
        '''生成插入的sql语句'''
        base='INSERT OR IGNORE INTO Picture ({key}) VALUES ({value})'
        sql_keys=','.join(['{}'.format(i) for i in list(dict.keys())])
        sql_values=','.join(['?' for i in range(len(list(dict.keys())))])
        
        insert_sql=base.format(key=sql_keys,value=sql_values)
        values=tuple(dict.values())
        
        self.insert_sql=insert_sql
        self.data=values
        return 1
    def insertTable(self):
        try:
            self.cur.execute(self.insert_sql,self.data)
            self.connection.commit()
            print('插入数据成功')
            return 1
        except Exception as e:
            print(e)
            print('插入数据失败')
            return 0
    
    def __del__(self):
        '''析构函数'''
        self.cur.close()
        self.connection.close()

if __name__=='__main__':
    dict=\
    {
    'artist':'hiki niitto',
    'character':'甘雨a',    
    }
    updatadict=\
    {
    'character':'甘雨,胡桃',
    'metadata':'highres'
    }
    a=Data('1',**dict)
    # a.show()
    #a.updateDic(**updatadict)
    # a.show()
    db=DataBase()
    db.genInsertSql(**a.dict,**{'id':a.id,'master':a.master,'download':a.download})
    print(db.insert_sql,db.data)
    db.insertTable()
