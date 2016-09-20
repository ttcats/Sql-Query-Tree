# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response,render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers.json import DjangoJSONEncoder

import json
import os


from .models import *
from .operation_mysql import db_operate
from .operation_postgres import postgre


import sys
reload(sys)
sys.setdefaultencoding('utf8')


# Create your views here.


@login_required(login_url="/login/")
def query_tree(request):
    user = request.session.get('username', 'anybody')
    Dbs = Dbmessage.objects.values('db_type')
    dbtypes = []
    for db in Dbs:
        dbtypes.append(db['db_type'])
    dbtypes = list(set(dbtypes))
    print dbtypes
    return render_to_response('query_tree.html',locals())

@login_required(login_url="/login/")
def db_choose(request):
    user = request.session.get('username', 'anybody')
    tree_id = request.GET['id'].split('_D_')
    dbs_id = request.GET['dbs']
    t=[] 
    print len(tree_id),"len tree_id"

    # user auth messages
    qu_usermessage = Querymessage.objects.filter(qu_uname=user)
    qu_user_authdatabaid = [ x.qu_databaid  for x in qu_usermessage ]

    # 打印相关实例
    if len(tree_id) == 1 and tree_id[0] == '#':
        datanames = []
        dataname = Databasemessage.objects.filter(db_type=dbs_id)
        dataids = [ x.db_databaid for x in dataname]
        for dataid in qu_user_authdatabaid:
            if dataid in dataids:
                dataname = Databasemessage.objects.get(db_databaid=dataid,db_type=dbs_id)
                datanames.append(dataname.db_title)
        datanames = list(set(datanames))
        for dataname in datanames:
            fid =  dataname
            t.append({"id":fid,"text":dataname,"children":True,"icon":"/static/img/host.png"})
                
    # 打印相关数据库
    elif len(tree_id) == 1 and tree_id[0] != '#':
        dbtitle = tree_id[0]
        query_dbs = Databasemessage.objects.filter(db_type=dbs_id,db_title=dbtitle)
        qu_dbtitles = []
        for query_db in query_dbs:
            if query_db.db_databaid in qu_user_authdatabaid:
                qu_dbtitles.append(query_db.db_databa)
        print qu_dbtitles
        qu_dbtitles = list(set(qu_dbtitles))
        for qu_dbtitle in qu_dbtitles:
            #_D_用以区分参数
            fid = dbtitle + '_D_' + qu_dbtitle
            t.append({"id":fid,"text":qu_dbtitle,"children":True,"icon":"/static/img/database.png"})
    # 打印相关表
    elif len(tree_id) == 2:
        dbtitle = tree_id[0]
        database = tree_id[1]
        dbmessage = Dbmessage.objects.get(db_type=dbs_id,db_title=dbtitle,db_auth='r')
        if dbs_id == 'mysql':
            sql = 'show tables;'
            db_connect = db_operate(dbmessage.db_ip,dbmessage.db_user,dbmessage.db_passwd,database,dbmessage.db_port,sql)
            comms = db_connect.mysql_command()
        elif dbs_id == 'pgsql':
            sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
            comms = postgre(dbmessage.db_ip,dbmessage.db_user,dbmessage.db_passwd,database,dbmessage.db_port,sql)

        for comm in comms:
            fid = dbtitle + '_D_' + database + '_D_' + comm.values()[0]
            t.append({"id":fid,"text":comm.values()[0],"children":True,"icon":"/static/img/table.png"})

    #打印字段和索引树分支
    elif len(tree_id) == 3:
        dbtitle = tree_id[0]
        database = tree_id[1]
        table = tree_id[2]

        fid_field = dbtitle + '_D_' + database + '_D_' + table + '_D_' +'field'
        fid_index = dbtitle + '_D_' + database + '_D_' + table + '_D_' +'index'
        t=[{"id":fid_field,"text":"field","children":True,"icon":"/static/img/field_index.png"},{"id":fid_index,"text":"index","children":False,"icon":"/static/img/field_index.png"}]

    # 打印字段名
    elif len(tree_id) == 4:
        dbtitle = tree_id[0]
        database = tree_id[1]
        table = tree_id[2]
        info = tree_id[3]
        dbmessage = Dbmessage.objects.get(db_type=dbs_id,db_title=dbtitle,db_auth='r')
        if dbs_id == 'mysql' and info == 'field':
            sql = "desc %s;" % table
            db_connect = db_operate(dbmessage.db_ip,dbmessage.db_user,dbmessage.db_passwd,database,dbmessage.db_port,sql)
            comms = db_connect.mysql_command()
            comms_list = [ x['Field'] for x in comms]
        elif dbs_id == 'pgsql' and info == 'field':
            sql = "SELECT column_name FROM information_schema.columns WHERE table_name = '%s';" % table
            comms = postgre(dbmessage.db_ip,dbmessage.db_user,dbmessage.db_passwd,database,dbmessage.db_port,sql)
            comms_list = [ x['column_name'] for x in comms]
        #elif info == 'index':
        #    t.append({'ERROR':'NOT INDEX'})
             
        for comm in comms_list:
            fid = dbtitle + '_D_' + database + '_D_' + table + '_D_' + info + '_D_' + comm
            t.append({"id":fid,"text":comm,"children":False,"icon":"/static/img/field_index.png"})
    
    print t
    s=json.dumps(t,indent=4)
    return HttpResponse(s)


@login_required(login_url="/login/")
@csrf_exempt
def query_sql(request):
    user = request.session.get('username', 'anybody')
    if request.method == "POST":
        #用户权限信息
        qu_usermessage = Querymessage.objects.filter(qu_uname=user)
        qu_user_authdatabaid = [ x.qu_databaid for x in qu_usermessage ]

        print request.POST
        dbtreeid = request.POST.get('treeid')
        sql = request.POST.get('text')
        db = request.POST.get('db')
        print dbtreeid,sql,db
        t = dbtreeid.split('_D_')
        if len(t) != 2:
            return HttpResponse('<p class="bg-warning">Please choose database!</p>')
        else:
            data_auth = Databasemessage.objects.filter(db_type=db,db_title=t[0],db_databa=t[1])
            db_auths = [ x.db_auth for x in data_auth]
            print db_auths
            if len(list(set(db_auths))) == 2 and 'rw' in db_auths:
                db_auth = 'rw'
            elif len(db_auths) == 1:
                db_auth = db_auths[0]
            else:
                db_auth = 'r'
            print db,t,db_auth
            dbmessage = Dbmessage.objects.get(db_type=db,db_title=t[0],db_auth=db_auth)
            print dbmessage.db_user 
            if db == "mysql":
                db_connect = db_operate(dbmessage.db_ip,dbmessage.db_user,dbmessage.db_passwd,t[1],dbmessage.db_port,sql)
                comms = db_connect.mysql_command()
            elif db == "pgsql":
                comms = postgre(dbmessage.db_ip,dbmessage.db_user,dbmessage.db_passwd,t[1],dbmessage.db_port,sql)

            #记录Sql信息
            Sqlmessage.objects.create(sql_user=user,sql_dbtitle=t[0],sql_dbdataba=t[1],sql_info=sql)

            try:
                #显示排版
                table_tds = ''
                for comm in comms:
                    titles = comm.keys()
                    titles.reverse() 
                    table_td = ''
                    for c_key in titles:
                        c_value = "<td>" + str(comm[c_key]) + "</td>"
                        table_td = c_value + table_td
                    table_tds = "<tr>" + table_td + "</tr>" + table_tds
                table_ths = ''
                for c_key in titles:
                    table_th = "<th>" + str(c_key) + "</th>"
                    table_ths = table_th + table_ths
                table_html = "<table > <tr>%s</tr>%s</table>" % (table_ths,table_tds)
            except:
                table_html = "<p class='bg-warning'>" + str(comms) + "</p>"
            
            return HttpResponse(table_html)

#django的分页方法
@login_required(login_url="/login/")
def query_message(request):
    user = request.session.get('username', 'anybody')
    contact_list = Sqlmessage.objects.all()
    paginator = Paginator(contact_list, 25)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'query_message.html', {'contacts': contacts,'user':user})

#bootstrap table 显示
@login_required(login_url="/login/")
def query_table_message(request):
    user = request.session.get('username', 'anybody')
    return render_to_response('query_table_message.html',locals())


@login_required(login_url="/login/")
@csrf_exempt
def query_table(request):
    print request.POST,"POST"
    if 'search' in request.GET.keys():
        search = request.GET['search']
    else:
        search = ''
    if 'limit' in request.GET.keys():
        limit = request.GET['limit']
    else:
        limit = 20
    if 'offset' in request.GET.keys():
        offset = request.GET['offset']
    else:
        offset = 0
    print limit,offset,search
    limits = int(limit) + int(offset)

    contact_list = Sqlmessage.objects.all()
    messages,messages_search = [],[]
    for contact in contact_list:
        messages.append({"id":contact.sql_id,"user":contact.sql_user,"db":contact.sql_dbtitle,"database":contact.sql_dbdataba,"sql":contact.sql_info,"ctime":contact.sql_ctime})
    #设置可查询类型
    for message in messages:
        if search in str(message['user']):
            messages_search.append(message)
        elif search in str(message['db']):
            messages_search.append(message)
        elif search in str(message['database']):
            messages_search.append(message)
        
    total = len(messages_search)
    messages_all = messages_search[int(offset):int(limits)]
    s = {"total":total,"rows":messages_all}

    t=json.dumps(s,indent=4,cls=DjangoJSONEncoder)
    return HttpResponse(t)
