import sqlite3

class Data():
    def __init__(self,**dict):
        self.dict=dict   

    def Mark(self,tar):
        '''下载/原图/删除后标记'''
        self.dict[tar]=1
    
    def updateDic(self,**dict):
        '''更新图片信息'''
        for key,value in dict.items():
            self.dict[key]=value
    def show(self):
        '''打印全部私有变量'''
        print(self.dict)    

class DataBase():
    
    def __init__(self,db='GelPic.db'):
        self.connection=sqlite3.connect(db)
        self.cur=self.connection.cursor()
        self.insert_sql=''
        self.data=''
        self.createPic_sql='''
                create table Picture(
                Picid text primary key,
                local_path text,
                master text,
                delet text,
                download text,
                artist text,
                character text,
                copyright text,
                metadata text,
                tag text,
                origin_url text,
                master_url text)
    '''
        self.createTag_sql='''
                create table Tags(
                Tagid text primary key,
                Gelname text,
                Chiname text)
        '''
        self.createPic_tag_sql='''
                create table Tags_Pic(
                Tagid text,
                Picid text)
        '''
        
    def createTable(self,sql):
        '''创建表'''
        try:
            self.cur.execute(sql)
            print('创建表成功')
            return 1
        except Exception as e:
            print(e)
            print('创建表失败')
            return 0
    def dropTable(self,table_name):
        try:
            self.cur.execute('drop table {}'.format(table_name))
            print('删除表成功')
            return 1
        except Exception as e:
            print(e)
            print('删除表失败')
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
    dict={
    'artist':'hiki niitto',
    'character':'甘雨a',    
    }
    updatadict={
    'character':'甘雨,胡桃',
    'metadata':'highres'
    }

    db=DataBase()
    # db.createTable(db.createPic_sql)
    # db.createTable(db.createTag_sql)
    # db.createTable(db.createPic_tag_sql)
    with open('对照表.csv','r',encoding='utf-8-sig') as f:
        dicts=f.read().split('\n')
