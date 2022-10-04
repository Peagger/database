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
            return 1
        except Exception as e:
            print(e)
            return 0
    
    def updateTable(self,sql):
        '''更新数据'''
        try:
            self.cur.execute(sql)
            self.connection.commit()
            return 1
        except Exception as e:
            print(e)
            return 0
    
    def selectTable(self,sql):
        '''查询数据'''
        try:
            self.cur.execute(sql)
            result=self.cur.fetchall()
            return result
        except Exception as e:
            print(e)
            return 0
    
    def updataTags(self):
        '''由根目录下的对照表更新Tags表'''
        with open('对照表.csv','r',encoding='utf-8-sig') as f:
            lines=f.read().split('\n')
            for line in lines:
                tagdict={}
                line_list=line.split(',')
                if(len(line_list)>=3):
                    tagdict['Chiname']=line_list[1]
                    tagdict['Gelname']=line_list[2]
                    if (db.genSelectSql(Tablename='Tags',target=['*'],**{'Gelname':line_list[2]})):
                        db.genUpdateSql(Tablename='Tags',condition={'Gelname':line_list[2]},**tagdict)
                    else:
                        db.genInsertSql(Tablename='Tags',**tagdict)
    
    def insertData(self,**data):
        '''在Picture表插入一条新数据'''
        if(self.genInsertSql('Picture',**data)):
            tags=data['character'].split(',')
            for Gelname in tags:
                tagids=db.genSelectSql(Tablename='Tags',target=['Tagid'],**{'Gelname':Gelname})
                for tagid in tagids:
                    db.genInsertSql(Tablename='Tags_pic',**{'Tagid':tagid[0],'Picid':data['Picid']})
        else:
            Picid=data.pop('Picid')
            self.genUpdateSql(Tablename='Picture',condition={'Picid':Picid},**data)
    
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
    
    db.dropTable('Picture')
    db.createTable(db.createPic_sql)
    # db.dropTable('Tags')
    # db.createTable(db.createTags_sql)
    # db.dropTable('Tags_Pic')
    # db.createTable(db.createPic_tags_sql)
    data={
    'Picid':'6730018',
    'local_path':'./pic/6730018.jpg',
    'master':'0',
    'delet':'0',
    'download':'0',
    'artist':'hiki_niito',
    'character':'ganyu_(genshin_impact)',
    'copyright':'genshin_impact',
    'metadata':'absurdres,highres',
    'tag':'1girl,ahoge,ass,bangs',
    'origin_url':'https://img3.gelbooru.com//samples/d3/c0/sample_d3c04b98e118908fc575fc146a44ec6b.jpg'   
    }
    db.insertData(**data)
    