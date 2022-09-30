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
        self.select_sql='select {tar} from {Tablename} where {attribute} ="{values}"'
        self.createPic_sql='''
                create table Picture(
                Picid INTEGER primary key,
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
        self.createTags_sql='''
                create table Tags(
                Tagid INTEGER PRIMARY KEY AUTOINCREMENT,
                Gelname text,
                Chiname text)
        '''
        self.createPic_tags_sql='''
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
    def genInsertSql(self,Tablename,**dict):
        '''生成插入的sql语句'''
        base='INSERT INTO {name} ({key}) VALUES ({value})'
        sql_keys=','.join(['{}'.format(i) for i in list(dict.keys())])
        sql_values=','.join(['?' for i in range(len(list(dict.keys())))])
        
        insert_sql=base.format(name=Tablename,key=sql_keys,value=sql_values)
        values=tuple(dict.values())
        
        self.insert_sql=insert_sql
        self.data=values
        return 1
    def insertTable(self):
        '''无参数,修改对象的sql和data后调用'''
        try:
            self.cur.execute(self.insert_sql,self.data)
            self.connection.commit()
            print('插入数据成功')
            return 1
        except Exception as e:
            print(e)
            print('插入数据失败')
            return 0
    def selectTable(self,sql):
        try:
            self.cur.execute(sql)
            result=self.cur.fetchall()
            for row in result:
                for line in row:
                    print(line,end=' ')
            return 1
        except Exception as e:
            print(e)
            print('查询失败')
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
    
    # db.dropTable('Picture')
    # db.dropTable('Tags')
    # db.dropTable('Tags_Pic')
    # db.createTable(db.createPic_sql)
    # db.createTable(db.createTags_sql)
    # db.createTable(db.createPic_tags_sql)

    # with open('对照表.csv','r',encoding='utf-8-sig') as f:
    #     lines=f.read().split('\n')
    #     for line in lines:
    #         tagdict={}
    #         if(len(line.split(','))>=3):
    #             tagdict['Chiname']=line.split(',')[1]
    #             tagdict['Gelname']=line.split(',')[2]
    #             db.genInsertSql('Tags',**tagdict)
    #             db.insertTable()
    values='hu_tao_(genshin_impact)'
    db.selectTable(db.select_sql.format(tar='Tagid',Tablename='Tags',attribute='Gelname',values=values))