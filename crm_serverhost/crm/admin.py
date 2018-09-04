from django.contrib import admin
from crm import models
# Register your models here.
# Register your models here.
# 增加一个添加入action中对出版书籍状态进行批量更新函数
def make_drop(modelAdmin,request,queryset):    # 传入actions = []
    print('-->',request,queryset)
    queryset.update(status='drop-off')  # 对某个具体字段进行修改
    make_graduated.short_description = "The server has drop-off"

class HostServerAdmin(admin.ModelAdmin):
    list_display = ('id','host','name','phone','stu_id','source_type','referral_from','server','server_type','server_memo','status','consultant','date','colored_status')   # 从models中调入函数字段名
    # 增加搜索框 publisher__name是关联到另外一张表   这样即可以搜名字又可以搜索出版社
    search_fields = ('name','server_type','consultant','server')
    # 增加过滤器
    list_filter = ('name','server_type','consultant','server')
    # 设置book列表页每页最多可以显示几页
    list_per_page = 10
    actions = [make_drop,]


admin.site.register(models.UserProfile)
admin.site.register(models.Department)
admin.site.register(models.Server)
admin.site.register(models.HostServer,HostServerAdmin)
admin.site.register(models.HostServer01,HostServerAdmin)
admin.site.register(models.HostServer02,HostServerAdmin)
admin.site.register(models.HostServer03,HostServerAdmin)
admin.site.register(models.HostServer04,HostServerAdmin)
admin.site.register(models.HostServer05,HostServerAdmin)
admin.site.register(models.HostServer06,HostServerAdmin)
admin.site.register(models.HostServer07,HostServerAdmin)
admin.site.register(models.HostServer08,HostServerAdmin)
admin.site.register(models.HostServerTrackRecord)
admin.site.register(models.ServerList)
admin.site.register(models.ServerRecord)
admin.site.register(models.HostRecord)
