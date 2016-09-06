# -*- coding: utf-8 -*-
import MySQLdb
import MySQLdb.cursors

class db_operate:
    
    def __init__(self,host,user,passwd,db,port,sql):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = port
        self.sql = sql

    def mysql_command(self):
        try:
            ret = []
            conn=MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db,port=self.port,charset="utf8",cursorclass=MySQLdb.cursors.DictCursor)
            cursor = conn.cursor()
            cursor.execute(self.sql)
            conn.commit()
            print cursor.rowcount
            for row in cursor.fetchall():
                ret.append(row)
        except MySQLdb.Error,e:
            conn.rollback()
            ret.append(e)

        return ret
