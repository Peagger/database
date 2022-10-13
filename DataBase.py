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
    
    def __init__(self,db='db/GelPic.db'):
        self.predownload_dict={'master':'0','delet':'0','download':'0'}
        self.download_dict={'master':'0','delet':'0','download':'1'}
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
        sql_values=','.join(["'{}'".format(str(i).replace('\'','\'\'')) for i in dicts.values()])
        
        sql=base.format(name=Tablename,key=sql_keys,value=sql_values)

        if(self.insertTable(sql)):return 1#插入成功返回1
        return 0 
    
    def genUpdateSql(self,Tablename,condition:dict,**dicts):
        '''生成更新的sql语句并执行'''
        base='UPDATE {name} SET {items} where {condition}'
        sql_items=','.join("{}='{}'".format(i,str(j).replace('\'','\'\'')) for i,j in dicts.items())
        sql_condition=' AND '.join("{}='{}'".format(i,str(j).replace('\'','\'\''))for i,j in condition.items())
        
        sql=base.format(name=Tablename,items=sql_items,condition=sql_condition)
        
        if(self.updateTable(sql)):return 1
        return 0
    
    def genSelectSql(self,Tablename,target:list,**condition):
        '''生成选择的sql语句并执行'''
        base='SELECT {tar} from {Tablename} where {condition}'
        sql_tar=','.join('{}'.format(i) for i in target)
        sql_condition=' AND '.join("{} = '{}'".format(i,str(j).replace('\'','\'\'')) for i,j in condition.items())
        
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
            #print(e)
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
                    if (self.genSelectSql(Tablename='Tags',target=['*'],**{'Gelname':line_list[2]})):#能找到同Gelname的更新,不能的插入
                        self.genUpdateSql(Tablename='Tags',condition={'Gelname':line_list[2]},**tagdict)
                    else:
                        self.genInsertSql(Tablename='Tags',**tagdict)
    
    def insertData(self,**data):
        '''在Picture表插入一条新数据'''
        if(self.genInsertSql('Picture',**data)):#插入不了就更新
            if(character_list:=data.get('character',0)):#插入的数据含有角色信息就更新Tags_Pic的对应关系
                tags=character_list.split(',')
                for Gelname in tags:
                    tagids=self.genSelectSql(Tablename='Tags',target=['Tagid'],**{'Gelname':Gelname})
                    if(tagids):
                        for tagid in tagids:
                            self.genInsertSql(Tablename='Tags_pic',**{'Tagid':tagid[0],'Picid':data['Picid']})
                    else:
                        self.genInsertSql(Tablename='Tags',**{'Gelname':Gelname})
                        tagid=self.genSelectSql(Tablename='Tags',target=['Tagid'],**{'Gelname':Gelname})
                        if(tagid):
                            tagid=tagid[0][0]
                            self.genInsertSql(Tablename='Tags_pic',**{'Tagid':tagid,'Picid':data['Picid']})
                        else:
                            print("插入新tag:{}并更新失败".format(Gelname))
        else:
            Picid=data.pop('Picid')
            self.genUpdateSql(Tablename='Picture',condition={'Picid':Picid},**data)
    def updateTagPicRelation():
        #todo 
        #依据Picture表character的对应关系
        pass
    def __del__(self):
        '''析构函数'''
        self.cur.close()
        self.connection.close()

if __name__=='__main__':
    db=DataBase()
    '''删表重建'''
    db.dropTable('Picture')
    db.createTable(db.createPic_sql)
    db.dropTable('Tags')
    db.createTable(db.createTags_sql)
    db.dropTable('Tags_Pic')
    db.createTable(db.createPic_tags_sql)

    db.updataTags()
