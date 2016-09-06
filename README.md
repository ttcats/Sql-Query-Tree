# Sql-Query-Tree

功能简介：
  query app 主要是根据ops中sql查询权限控制功能编写。以添加用户关联的databaseid来控制和显示相关数据库树的信息，进行只读或者读写的操作(该功能用户权限到库，到表的权限可以设置有关数据库账号来实现(全局))。
  有四个表：
     Dbmessage
        数据库信息，记录数据库账号和该账号权限的信息(一个数据库实例设置两个账号，一个只读(r),一个读写(rw))
     Databasemessage
        数据库库信息，记录数据库所要查询库的信息，其中db_auth字段为操作该库权限，db_databaid为该库的id，一个数据库库信息需要两条数据(只读(r)和读写(rw))
     Querymessage
        用户权限信息，其中qu_databaid字段关联Databasemessage中的db_databaid字段，用来权限控制
     Sqlmessage
        SQL信息记录，用来记录有关操作的信息
  详情请参考query/models.py



安装
1.django==1.10
     pip install django==1.10
2.MySQL-python
     yum install MySQL-python
3.psycopg2
     pip install psycopg2


配置(根据环境自行配置)：
     settings.py 数据库信息

启动
1.导入数据类型
     python manage.py makemigrations
     python manage.py migrate

2.启动程序
     python manage.py runserver 0.0.0.0:8000

备注:
  当前只有两个数据库类型,MySQL(脚本query/operation_mysql.py)和PostgreSQL(脚本query/operation_postgres.py)
  查询信息中搜索默认可查询user、db、database
