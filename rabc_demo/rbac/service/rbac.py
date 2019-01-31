#coding:utf-8
import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import  HttpResponse,redirect


def check_permission_flag(request,current_path):
    # 校验权限方案1(permission_list)
    permission_list = request.session.get("permission_list", [])
    flag = False
    for permission in permission_list:
        permission = "^%s$" % permission
        ret = re.match(permission, current_path)
        if ret:
            flag = True
            break
    return flag

def check_has_permission(request,current_path):
    permission_dict = request.session.get("permission_dict")
    # print permission_dict.values()

    for item in permission_dict.values():
        urls = item['urls']
        for reg in urls:
            reg = "^%s$" % reg

            ret = re.match(reg, current_path)
            # print '%s-%s=====%s' % (reg, current_path,ret)

            if ret:
                # print reg,ret.group()
                # print("in rabc.py file:actions",item['actions'])
                request.actions = item['actions']
                return None
    return HttpResponse("没有访问权限oo！")

class ValidPermission(MiddlewareMixin):

    def process_request(self,request):

        # 当前访问路径
        current_path = request.path_info

        # 检查是否属于白名单
        valid_url_list=["/login/","/reg/","/admin/.*","/logout/","^/$"]
        for valid_url in valid_url_list:
            ret=re.match(valid_url,current_path)
            if ret:
                return None


        # 校验用户是否登录
        user_id=request.session.get("user_id")
        if not user_id:
            return redirect("/login/")


        # # 校验权限方案1(permission_list)
        # permission_list = request.session.get("permission_list",[])  # ['/users/', '/users/add', '/users/delete/(\\d+)', 'users/edit/(\\d+)']
        # flag=check_permission_flag(request,current_path)
        #
        # if not flag:
        #     return HttpResponse("没有访问权限！")
        #
        # return None

        ##校验权限2
        check_has_permission(request, current_path)


