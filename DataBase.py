#!/usr/bin/python
# -*-coding:utf-8-*-
import sqlite3


class Dict2DB:
    def __init__(self, db_name,keys,values):
        '''
        :param db_name: name of the datebase.
        '''
        self.conn = sqlite3.connect(db_name)
        self.table_exist = False
        self.create_table(keys)
        self.add_data(keys,values)
        

    def create_table(self,keys):
        try:
            table_string = ','.join(keys)
            create_table = f' CREATE TABLE IF NOT EXISTS USER({table_string});'
            # 设置一个unique字段去重
            create_table = create_table.replace('IP','IP UNIQUE')
            create_table = create_table.replace('HostName','HostName UNIQUE')
            self.conn.execute(create_table)
            self.conn.commit()
            self.table_exist = True
        except:
            print('create table failed')
            return False

    def add_data(self, keys,values):
        '''
        :param keys: A list of columns.
        :param values: A list of values
        '''
        if self.table_exist:
            key_string = ','.join(keys)
            # 将字段值加上引号，避免部分带括号的值导致语句出错
            # 需要处理名字中带引号，双引号事件。（暂时修补单引号）
            value_string = ','.join(['"'+ x +'"' for x in values]) 
            # print(key_string,value_string)
            add_data = f'REPLACE INTO USER ({key_string}) VALUES ({value_string})'
            # print(add_data)
            self.conn.execute(add_data)
            self.conn.commit()

    @classmethod
    def read_data(cls,db_name,keyword):
        '''
        :param keyword: Keyword for search
        :param value: keyword value
         '''
        try:
            statement = f'NickName LIKE "%{keyword}%" OR HostName LIKE "%{keyword}%" OR UserName LIKE "%{keyword}%" OR MakeName LIKE "%{keyword}%";'
            read_data = f'SELECT NickName,HostName,MakeName,IP FROM USER WHERE {statement}'
            conn = sqlite3.connect(db_name)
            cur = conn.cursor()
            cur.execute(read_data)
            data = cur.fetchall()
            conn.commit()
            return data
        except sqlite3.OperationalError as e:
            print("没有保存的数据",e)
            return False
    
    @classmethod
    def count_entry(cls,db_name):
        count_entry = 'SELECT count(*) FROM USER'
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute(count_entry)
        data = cur.fetchall()
        conn.commit()
        return data

    def close(self):
        try:
            self.conn.close()
        except:
            return