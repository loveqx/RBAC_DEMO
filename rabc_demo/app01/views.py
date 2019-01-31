#coding:utf-8
#导入系统模块
import re

#导入django模块
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import logout

#导入第三方模块
from rbac.models import *
from app01.models import Book
from rbac.service.perssions import *


class Per(object):
    def __init__(self,actions):
        self.actions=actions
    def add(self):
        return "add" in self.actions
    def delete(self):
        return "delete" in self.actions
    def edit(self):
        return "edit" in self.actions
    def list(self):
        return "list" in self.actions


def users(request):

    user_list=User.objects.all()

    # permission_list=request.session.get("permission_list")
    #print(permission_list)

    # 查询当前登录人得名字

    id=request.session.get("user_id")
    user=User.objects.filter(id=id).first()

    per=Per(request.actions)

    return render(request, "rbac/users.html", locals())



def add_user(request):
    return HttpResponse('add user')


def del_user(request,id):
    return HttpResponse("del user"+id)


def edit_user(request,id):
    return HttpResponse("edit user"+id)

def roles(request):
    # 查询当前登录人得名字
    id = request.session.get("user_id")
    user = User.objects.filter(id=id).first()
    role_list=Role.objects.all()

    per = Per(request.actions)
    return render(request, "rbac/roles.html", locals())


def add_role(request):
    print request.actions
    return HttpResponse('add role')


def del_role(request,id):
    return HttpResponse("del role"+id)


def edit_role(request,id):
    return HttpResponse("edit role"+id)


def login(request):

    if  request.method=="POST":

        user=request.POST.get("user")
        pwd=request.POST.get("pwd")

        user=User.objects.filter(name=user,pwd=pwd).first()
        if user:
            ############################### 在session中注册用户ID######################
            request.session["user_id"]=user.pk

            ###############################在session注册权限列表##############################



            # 查询当前登录用户的所有角色
            # ret=user.roles.all()
            # print(ret)# <QuerySet [<Role: 保洁>, <Role: 销售>]>

            # 查询当前登录用户的所有权限，注册到session中
            initial_session(user,request)


            #return HttpResponse("登录成功！")
            #登录成功后判断当前用户是否有权限，如果没有任何权限，则无法登录，给与用户提示。
            user_permission  = request.session.get('permission_dict')
            for permission_dic in user_permission.values():
                if permission_dic['urls']:
                    return redirect(permission_dic['urls'][0])
                else:
                    return HttpResponse('当前你没有任何权限，请联系管理员授予权限！')

    return render(request,"login.html")

def logout(request):
    return redirect("/login/")

def books(request):
    # 查询当前登录人得名字
    id = request.session.get("user_id")
    user = User.objects.filter(id=id).first()

    book_list=Book.objects.all()

    per = Per(request.actions)

    return render(request, "books.html", locals())

def add_book(request):
    return HttpResponse('add book')

def del_book(request,id):
    return HttpResponse("del book"+id)

def edit_book(request,id):
    return HttpResponse("edit book"+id)