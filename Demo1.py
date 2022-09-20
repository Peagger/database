import sqlite3
class DataBase:
    


    

    #初始化，连接数据库得到游标
    def __init__(self,db='pic.db'):
        self.connection=sqlite3.connect(db)
        self.cur=self.connection.cursor()
        self.id=0    
        self.source=''       #来源
        self.url=""          #高清图链接
        self.path=''         #本地路径
        self.hash=''         #sha256值
        self.artist=''       #作者
        self.copyright=''    #版权
        self.character=''    #角色
        self.craw=0          #是否爬取成功
        self.exist=0         #是否存在
        self.r18=0           #是否r18
        self.pre=1           #是否为高清大图
        self.stars=1         #评分
        self.other_tags=""   #其它标签
    
    def getDict(self):
        dict={
        'id':self.id,    
        'source':self.source,       
        'url':self.url,          
        'path':self.path,         
        'hash':self.hash,         
        'artist':self.artist,       
        'copyright':self.copyright,   
        'character':self.character,    
        'craw':self.craw,        
        'exist':self.exist,         
        'r18':self.r18,           
        'pre':self.pre,           
        'stars':self.stars,         
        'other_tags':self.other_tags 
        }
        return dict
    
    def createTable(self,sql):
        try:
            self.cur.execute(sql)
            print('创建表成功')
            return 1
        except Exception as e:
            print(e)
            print('创建表失败')
            return 0
    def dropTable(self,sql):
        try:
            self.cur.execute(sql)
            print('删除表成功')
            return 1
        except Exception as e:
            print(e)
            print('删除表失败')
            return 0
    
    def insertTable(self,sql,data):
        try:
            self.cur.execute(sql,data)
            self.connection.commit()
            print('插入数据成功')
            return 1
        except Exception as e:
            print(e)
            print('插入数据失败')
            return 0
    
    def selectTable(self,sql,target):
        try:
            self.cur.execute(sql.format(target))
            result=self.cur.fetchall()
            for row in result:
                for line in row:
                    print(line,end=',')
            return 1
        except Exception as e:
            print(e)
            print('查询失败')
            return 0
    
    def generateSql(self,item: dict,table_name='Picture'):
        sql_base = """INSERT INTO {table_name} ({key}) VALUES ({value})"""  # 主体sql

        sql_field = ','.join(['{}'.format(i) for i in list(item.keys())])
        sql_value = ','.join(['?' for i in range(len(list(item.keys())))])

        # 插入sql
        insert_sql = sql_base.format(table_name=table_name, key=sql_field, value=sql_value)

        # # 保存的数据
        save_data = tuple(item.values())

        # # 插入并更新数据 sql
        # update_sql = """ ON DUPLICATE KEY UPDATE {}"""
        # update_sql_field = ', '.join(['`{}`=VALUES(`{}`)'.format(i, i) for i in list(item.keys())])
        # update_sql = insert_sql + update_sql.format(update_sql_field)
        # insert_sql += ';'
        # update_sql += ';'

        # # print(insert_sql)
        # # print(update_sql)
        # # print(save_data)

        return insert_sql,save_data

    #析构函数，断开连接
    def __del__(self):
        self.cur.close()
        self.connection.close()
        #print('芝士析构函数')


sql_createTable='''create table Picture(
                id integer primary key,
                source text,
                url text,
                path text,
                hash text,
                artist text,
                copyright text,
                character text,
                craw integer CHECK(craw in (0,1)),
                exist integer CHECK(exist in (0,1)),
                r18 integer CHECK(r18 in (0,1)),
                pre integer CHECK(pre in (0,1)),
                stars integer CHECK(stars >=0),
                other_tags text
                )'''
sql_dropTable='drop table Picture'
sql_insertTable='insert into Picture(id,source,hash) values(?,?,?)'
sql_selectTable='select path from Picture where {0} in (artist or copyright or character)'
sql_updateTable=''
sql_deleteTable=''

# picDatabase=DataBase()
# # picDatabase.dropTable(sql_dropTable)
# # picDatabase.createTable(sql_createTable)

# dict={
# 'id':1131,
# 'artist':'猫1雷',
# 'source':'P站',
# 'hash':'114514'
# }
# dict=picDatabase.getDict()
# sql=picDatabase.generateSql(dict)
# print(sql)
# picDatabase.insertTable(sql[0],sql[1])