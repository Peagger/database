import sqlite3

from matplotlib.table import Table

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
        self.select_sql='select {tar} from {Tablename} where {attribute} ="{values}"'
        self.select_tagid_gelname='select Tagid from Tags where Gelname ="{values}"'
        self.select_tagid_chiname='select Tagid from Tags where Chiname ="{values}"'
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
    
    def genInsertSql(self,Tablename,**dicts):
        '''生成插入的sql语句并执行'''
        base='INSERT INTO {name} ({key}) VALUES ({value})'
        sql_keys=','.join(['{}'.format(i) for i in list(dicts.keys())])
        sql_values=','.join(["'{}'".format(i) for i in dicts.values()])
        
        sql=base.format(name=Tablename,key=sql_keys,value=sql_values)

        if(self.insertTable(sql)):return 1
        return 0 
    
    def genUpdateSql(self,Tablename,condition:dict,**dicts):
        '''生成更新的sql语句并执行'''
        base='UPDATE {name} SET {items} where {condition}'
        sql_items=','.join("{}='{}'".format(i,j) for i,j in dicts.items())
        sql_condition=' AND '.join("{}='{}'".format(i,j)for i,j in condition.items())
        
        sql=base.format(name=Tablename,items=sql_items,condition=sql_condition)
        
        if(self.updateTable(sql)):return 1
        return 0
    
    def genSelectSql(self,Tablename,target:list,**condition):
        '''生成选择的sql语句并执行'''
        base='SELECT {tar} from {Tablename} where {condition}'
        sql_tar=','.join('{}'.format(i) for i in target)
        sql_condition=' AND '.join("{}='{}'".format(i,j) for i,j in condition.items())
        
        sql=base.format(tar=sql_tar,Tablename=Tablename,condition=sql_condition)
        result=self.selectTable(sql)
        if(result):return result
        return 0
    
    def insertTable(self,sql):
        '''插入数据'''
        try:
            self.cur.execute(sql)
            self.connection.commit()
            print('插入数据成功')
            return 1
        except Exception as e:
            print(e)
            print('插入数据失败')
            return 0
    
    def updateTable(self,sql):
        '''更新数据'''
        try:
            self.cur.execute(sql)
            self.connection.commit()
            print('更新数据成功')
            return 1
        except Exception as e:
            print(e)
            print('更新数据失败')
            return 0
    
    def selectTable(self,sql):
        '''查询数据'''
        try:
            self.cur.execute(sql)
            result=self.cur.fetchall()
            return result
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
    # db.createTable(db.createTags_sql)
    # db.dropTable('Tags_Pic')
    # db.createTable(db.createPic_sql)
    # db.createTable(db.createPic_tags_sql)

    # with open('对照表.csv','r',encoding='utf-8-sig') as f:
    #     lines=f.read().split('\n')
    #     for line in lines:
    #         tagdict={}
    #         if(len(line.split(','))>=3):
    #             tagdict['Chiname']=line.split(',')[1]
    #             tagdict['Gelname']=line.split(',')[2]
    #             db.genInsertSql('Tags',**tagdict)
    
    #db.genInsertSql(Tablename='Tags_Pic',**{'Tagid':'4','Picid':'9114514'})
    if(res:=db.genSelectSql(Tablename='Tags',target=['Tagid'],**{'Gelname':'hu_tao'})):
        for line in res:
            Picid=db.genSelectSql(Tablename='Tags_Pic',target=['Picid'],**{'Tagid':line[0]})
            print(Picid)
    else:
        db.genInsertSql(Tablename='Tags',**{'Gelname':'hu_tao'})