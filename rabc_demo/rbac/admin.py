#coding:utf-8
from django.contrib import admin

# Register your models here.


from .models import *


class PerConfig(admin.ModelAdmin):
    """
     默认情况下，admin后台只显示类里面定义的__str__或__unicode__
    可以通过list_display扩展显示
    """

    list_display = ["title","url","group","action"]

class UserConfig(admin.ModelAdmin):
    list_display = ['name','pwd']


admin.site.register(User,UserConfig)
admin.site.register(Role)
admin.site.register(Permission,PerConfig)
admin.site.register(PermissionGroup)
