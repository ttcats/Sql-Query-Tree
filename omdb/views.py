# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


import sys
reload(sys)
sys.setdefaultencoding('utf8')


@login_required(login_url="/login/")
def index(request):
    user = request.session.get('username', 'anybody')
    return render_to_response('index.html',locals())

@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        print user
        if user is not None:
            auth.login(request, user)
            request.session['username'] = username
            request.session.get_expiry_age()
            request.session.get_expire_at_browser_close()
            print request.session
            return HttpResponseRedirect('/db/query_tree/')
        else:
            return render_to_response('login.html')
    return render_to_response('login.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')

@login_required(login_url="/login/")
def host_list(request):
    user = request.session.get('username', 'anybody')
    return render_to_response('host_list.html',locals())
