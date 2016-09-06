#coding=utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Dbmessage(models.Model):
    '''
        数据库的信息,db_auth设置为r(只读)或者rw(读写),和Databasemessage库的db_auth匹配使用
    '''
    db_id = models.AutoField(primary_key=True)
    db_title = models.CharField(max_length=60,verbose_name="实例名")
    db_type = models.CharField(max_length=60,verbose_name="数据库类型")
    db_ip = models.GenericIPAddressField()
    db_port = models.IntegerField()
    db_user = models.CharField(max_length=60)
    db_passwd = models.CharField(max_length=60)
    db_auth = models.CharField(max_length=60)
    db_envname = models.CharField(max_length=100,verbose_name="实例信息")
    db_ctime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '数据库类型:%s 实例:%s 用户权限:%s'   %(self.db_type,self.db_title,self.db_auth)


class Databasemessage(models.Model):
    '''
        数据库库的信息
    '''
    db_databaid = models.AutoField(primary_key=True)
    db_type = models.CharField(max_length=60)
    db_title = models.CharField(max_length=60)
    db_databa = models.CharField(max_length=60)
    db_auth = models.CharField(max_length=60)
    db_databaenvname = models.CharField(max_length=100)
    db_ctime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '实例:%s 数据库:%s 数据库ID:%s 权限:%s' %(self.db_title, self.db_databa,self.db_databaid,self.db_auth)


class Querymessage(models.Model):
    '''
        当前用户权限设置,qu_databaid和Databasemessage库的db_databaid匹配使用
    '''
    qu_uname = models.CharField(max_length=60)
    qu_databaid= models.IntegerField()
    qu_ctime = models.DateTimeField(auto_now_add=True)


    def __unicode__(self):
        return '用户:%s 数据库ID:%s' %(self.qu_uname,self.qu_databaid)


class Sqlmessage(models.Model):
    '''
       SQL信息记录
    '''
    sql_id = models.AutoField(primary_key=True)
    sql_user = models.CharField(max_length=60)
    sql_dbtitle = models.CharField(max_length=60)
    sql_dbdataba = models.CharField(max_length=60)
    sql_info = models.CharField(max_length=255)
    sql_ctime = models.DateTimeField(auto_now_add=True)
    
    

