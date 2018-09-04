#_*_coding:utf-8_*_
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.html import format_html

from django.db import models
# 用户认证加盐认证模块
from django.contrib.auth.models import User

# Create your models here.
# 用户认证加盐认证模块
from django.contrib.auth.models import User

server_type_choices= (('product',u'生产环境'),
                     ('pre',u'域生产环境',),
                     ('test',u'测试环境',),
                     )
# 要用自己的认证先继承django的认证系统
class UserProfile(models.Model):     # 用OneToOneField只允许建唯一一条user信息，建多了不被允许！
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(u"服务器名",max_length=64)
    department = models.ForeignKey('Department',on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        permissions =(('view_server_list',u"可以查看服务器列表"),
                      ('view_server_info',u"可以查看服务器详情"),
                      ('edit_own_server_info',u"可以修改自己的查看服务器信息"),
                      )

class Department(models.Model):
    name = models.CharField(u"部门名称",max_length=128,unique=True)
    addr = models.CharField(u"办公地址",max_length=128)
    city = models.CharField(max_length=64)
    #staffs = models.ManyToManyField('UserProfile',blank=True)       # 一个课程老师可以对应多个校区反向关联等同于school = models.ForeignKey('School')
    def __str__(self):
        return self.name


class Server(models.Model):
    name = models.CharField(u"服务功能名称",max_length=128,unique=True)
#    offline_price = models.IntegerField(u"面授价格")
#    online_price = models.IntegerField(u"网络班价格")
    dell_server = models.CharField(u"dell物理机",max_length=64)
    kaixiang_server = models.CharField(u"凯翔物理机",max_length=64)
    lc_server = models.CharField(u"浪潮物理机",max_length=64)
    esxi_server = models.CharField(u"esxi物理机",max_length=64)
    introduction = models.TextField(u"功能及相关简介")

    def __str__(self):
        return "%s" %(self.name)


class HostServer(models.Model):
    host = models.CharField(u"主机ip",max_length=64,unique=True)
    name = models.CharField(u"主机名",max_length=64,blank=True,null=True)
    phone = models.BigIntegerField(u'联系电话',blank=True,null=True)
    stu_id = models.CharField(u"主机编号",blank=True,null=True,max_length=64)
    #id = models.CharField(u"身份证号",blank=True,null=True,max_length=128)
    source_type_choices = (('yunwei',u"运维人员创建"),
                   ('referral',u"内部冗余备机"),
                   ('chengdu',u"成都创建"),
                   ('guanwu',u"关务开发创建"),
                   ('qingsuan',u"清算开发创建"),
                   ('dbserver',u"数据库开发创建"),
                   ('others',u"其它"),
                   )
    source_type = models.CharField(u'主机创建来源',max_length=64, choices=source_type_choices,default='yunwei')
    # 如果是内部创建关联'self'，内部转自测试，用ForeignKey, 反查自己用related_name="internal_referral"如果不起个名字叫related_name直接Customer="internal_referral"
    referral_from = models.ForeignKey('self',verbose_name=u"转相关备机",help_text=u"若此主机是转备份做其它主机备机用,请在此处选择主机名称",blank=True,null=True,related_name="referraled_who",on_delete=models.CASCADE)

    server = models.ForeignKey(Server,verbose_name=u"主机创建需求",on_delete=models.CASCADE)    # 关联到Server服务器类下的所有内容所以用ForeignKey
    server_type = models.CharField(u"服务器环境类型",max_length=64,choices=server_type_choices,default='test')
    server_memo = models.TextField(u"主机需创建前内容详情",help_text=u"主机需创建前的大概情况,主机信息备注等...")
    status_choices = (('signed',u"运行中"),
                      ('unregistered',u"宕机"),
                      ('working',u"运行中"),
                      ('down-off',u"宕机"),
                      )

    status = models.CharField(u"状态",choices=status_choices,max_length=64,default=u"unregistered",help_text=u"选择服务器主机此时的状态")
    consultant = models.ForeignKey(UserProfile,verbose_name=u"需求人姓名",on_delete=models.CASCADE)
    date = models.DateField(u"提需求日期",auto_now_add=True)

    server_list = models.ManyToManyField('ServerList',verbose_name=u"服务应用类型",blank=True)

    def __str__(self):
        return "%s,%s" %(self.host,self.name )
    # 增加customer表里对用户的权限操作功能(此记录要同步到数据库) 元组dict字典格式必须内层再套() 后与动作关联起来django做了把权限和用户关联并判断有没有权限
    # class Meta:     # 写哪里都一样, 移到customer表
    #    permissions =(('can_del_customer', u"可删除用户"),)

    def colored_status(self):   # 写入admin加入字段
        if self.status == "signed":   # 如果状态时publish的让其闪显示
            format_td = format_html('<span style="padding:2px;background-color:yellowgreen;color:white">运行中</span>')    # format_html()功能帮你在前端转成html格式, 需要导入from django.utils.html import format_html
        elif self.status == "unregistered":
            format_td = format_html('<span style="padding:2px;background-color:red;color:white">宕机</span>')
        elif self.status == "working":
            format_td = format_html('<span style="padding:2px;background-color:green:white">运行中</span>')
        elif self.status == "down-off":
            format_td = format_html('<span style="padding:2px;background-color:red;color:white">宕机</span>')

        return format_td
    colored_status.short_description = 'status'    # 将colored_status改名成status


class HostServer01(models.Model):
    host = models.CharField(u"主机ip",max_length=64,unique=True)
    name = models.CharField(u"主机名",max_length=64,blank=True,null=True)
    phone = models.BigIntegerField(u'联系电话',blank=True,null=True)
    stu_id = models.CharField(u"主机编号",blank=True,null=True,max_length=64)
    #id = models.CharField(u"身份证号",blank=True,null=True,max_length=128)
    source_type_choices = (('yunwei',u"运维人员创建"),
                   ('referral',u"内部冗余备机"),
                   ('chengdu',u"成都创建"),
                   ('guanwu',u"关务开发创建"),
                   ('qingsuan',u"清算开发创建"),
                   ('dbserver',u"数据库开发创建"),
                   ('others',u"其它"),
                   )
    source_type = models.CharField(u'主机创建来源',max_length=64, choices=source_type_choices,default='yunwei')
    # 如果是内部创建关联'self'，内部转自测试，用ForeignKey, 反查自己用related_name="internal_referral"如果不起个名字叫related_name直接Customer="internal_referral"
    referral_from = models.ForeignKey('self',verbose_name=u"转相关备机",help_text=u"若此主机是转备份做其它主机备机用,请在此处选择主机名称",blank=True,null=True,related_name="referraled_who",on_delete=models.CASCADE)

    server = models.ForeignKey(Server,verbose_name=u"主机创建需求",on_delete=models.CASCADE)    # 关联到Server服务器类下的所有内容所以用ForeignKey
    server_type = models.CharField(u"服务器环境类型",max_length=64,choices=server_type_choices,default='test')
    server_memo = models.TextField(u"主机需创建前内容详情",help_text=u"主机需创建前的大概情况,主机信息备注等...")
    status_choices = (('signed',u"运行中"),
                      ('unregistered',u"宕机"),
                      ('working',u"运行中"),
                      ('down-off',u"宕机"),
                      )

    status = models.CharField(u"状态",choices=status_choices,max_length=64,default=u"unregistered",help_text=u"选择服务器主机此时的状态")
    consultant = models.ForeignKey(UserProfile,verbose_name=u"需求人姓名",on_delete=models.CASCADE)
    date = models.DateField(u"提需求日期",auto_now_add=True)

    server_list = models.ManyToManyField('ServerList',verbose_name=u"服务应用类型",blank=True)

    def __str__(self):
        return "%s,%s" %(self.host,self.name )
    # 增加customer表里对用户的权限操作功能(此记录要同步到数据库) 元组dict字典格式必须内层再套() 后与动作关联起来django做了把权限和用户关联并判断有没有权限
    # class Meta:     # 写哪里都一样, 移到customer表
    #    permissions =(('can_del_customer', u"可删除用户"),)

    def colored_status(self):   # 写入admin加入字段
        if self.status == "signed":   # 如果状态时publish的让其闪显示
            format_td = format_html('<span style="padding:2px;background-color:yellowgreen;color:white">运行中</span>')    # format_html()功能帮你在前端转成html格式, 需要导入from django.utils.html import format_html
        elif self.status == "unregistered":
            format_td = format_html('<span style="padding:2px;background-color:red;color:white">宕机</span>')
        elif self.status == "working":
            format_td = format_html('<span style="padding:2px;background-color:green:white">运行中</span>')
        elif self.status == "down-off":
            format_td = format_html('<span style="padding:2px;background-color:red;color:white">宕机</span>')

        return format_td
    colored_status.short_description = 'status'    # 将colored_status改名成status


class HostServer02(models.Model):
    host = models.CharField(u"主机ip",max_length=64,unique=True)
    name = models.CharField(u"主机名",max_length=64,blank=True,null=True)
    phone = models.BigIntegerField(u'联系电话',blank=True,null=True)
    stu_id = models.CharField(u"主机编号",blank=True,null=True,max_length=64)
    #id = models.CharField(u"身份证号",blank=True,null=True,max_length=128)
    source_type_choices = (('yunwei',u"运维人员创建"),
                   ('referral',u"内部冗余备机"),
                   ('chengdu',u"成都创建"),
                   ('guanwu',u"关务开发创建"),
                   ('qingsuan',u"清算开发创建"),
                   ('dbserver',u"数据库开发创建"),
                   ('others',u"其它"),
                   )
    source_type = models.CharField(u'主机创建来源',max_length=64, choices=source_type_choices,default='yunwei')
    # 如果是内部创建关联'self'，内部转自测试，用ForeignKey, 反查自己用related_name="internal_referral"如果不起个名字叫related_name直接Customer="internal_referral"
    referral_from = models.ForeignKey('self',verbose_name=u"转相关备机",help_text=u"若此主机是转备份做其它主机备机用,请在此处选择主机名称",blank=True,null=True,related_name="referraled_who",on_delete=models.CASCADE)

    server = models.ForeignKey(Server,verbose_name=u"主机创建需求",on_delete=models.CASCADE)    # 关联到Server服务器类下的所有内容所以用ForeignKey
    server_type = models.CharField(u"服务器环境类型",max_length=64,choices=server_type_choices,default='test')
    server_memo = models.TextField(u"主机需创建前内容详情",help_text=u"主机需创建前的大概情况,主机信息备注等...")
    status_choices = (('signed',u"运行中"),
                      ('unregistered',u"宕机"),
                      ('working',u"运行中"),
                      ('down-off',u"宕机"),
                      )

    status = models.CharField(u"状态",choices=status_choices,max_length=64,default=u"unregistered",help_text=u"选择服务器主机此时的状态")
    consultant = models.ForeignKey(UserProfile,verbose_name=u"需求人姓名",on_delete=models.CASCADE)
    date = models.DateField(u"提需求日期",auto_now_add=True)

    server_list = models.ManyToManyField('ServerList',verbose_name=u"服务应用类型",blank=True)

    def __str__(self):
        return "%s,%s" %(self.host,self.name )
    # 增加customer表里对用户的权限操作功能(此记录要同步到数据库) 元组dict字典格式必须内层再套() 后与动作关联起来django做了把权限和用户关联并判断有没有权限
    # class Meta:     # 写哪里都一样, 移到customer表
    #    permissions =(('can_del_customer', u"可删除用户"),)

    def colored_status(self):   # 写入admin加入字段
        if self.status == "signed":   # 如果状态时publish的让其闪显示
            format_td = format_html('<span style="padding:2px;background-color:yellowgreen;color:white">运行中</span>')    # format_html()功能帮你在前端转成html格式, 需要导入from django.utils.html import format_html
        elif self.status == "unregistered":
            format_td = format_html('<span style="padding:2px;background-color:red;color:white">宕机</span>')
        elif self.status == "working":
            format_td = format_html('<span style="padding:2px;background-color:green:white">运行中</span>')
        elif self.status == "down-off":
            format_td = format_html('<span style="padding:2px;background-color:red;color:white">宕机</span>')

        return format_td
    colored_status.short_description = 'status'    # 将colored_status改名成status


class HostServer03(models.Model):
    host = models.CharField(u"主机ip",max_length=64,unique=True)
    name = models.CharField(u"主机名",max_length=64,blank=True,null=True)
    phone = models.BigIntegerField(u'联系电话',blank=True,null=True)
    stu_id = models.CharField(u"主机编号",blank=True,null=True,max_length=64)
    #id = models.CharField(u"身份证号",blank=True,null=True,max_length=128)
    source_type_choices = (('yunwei',u"运维人员创建"),
                   ('referral',u"内部冗余备机"),
                   ('chengdu',u"成都创建"),
                   ('guanwu',u"关务开发创建"),
                   ('qingsuan',u"清算开发创建"),
                   ('dbserver',u"数据库开发创建"),
                   ('others',u"其它"),
                   )
    source_type = models.CharField(u'主机创建来源',max_length=64, choices=source_type_choices,default='yunwei')
    # 如果是内部创建关联'self'，内部转自测试，用ForeignKey, 反查自己用related_name="internal_referral"如果不起个名字叫related_name直接Customer="internal_referral"
    referral_from = models.ForeignKey('self',verbose_name=u"转相关备机",help_text=u"若此主机是转备份做其它主机备机用,请在此处选择主机名称",blank=True,null=True,related_name="referraled_who",on_delete=models.CASCADE)

    server = models.ForeignKey(Server,verbose_name=u"主机创建需求",on_delete=models.CASCADE)    # 关联到Server服务器类下的所有内容所以用ForeignKey
    server_type = models.CharField(u"服务器环境类型",max_length=64,choices=server_type_choices,default='test')
    server_memo = models.TextField(u"主机需创建前内容详情",help_text=u"主机需创建前的大概情况,主机信息备注等...")
    status_choices = (('signed',u"运行中"),
                      ('unregistered',u"宕机"),
                      ('working',u"运行中"),
                      ('down-off',u"宕机"),
                      )

    status = models.CharField(u"状态",choices=status_choices,max_length=64,default=u"unregistered",help_text=u"选择服务器主机此时的状态")
    consultant = models.ForeignKey(UserProfile,verbose_name=u"需求人姓名",on_delete=models.CASCADE)
    date = models.DateField(u"提需求日期",auto_now_add=True)

    server_list = models.ManyToManyField('ServerList',verbose_name=u"服务应用类型",blank=True)

    def __str__(self):
        return "%s,%s" %(self.host,self.name )
    # 增加customer表里对用户的权限操作功能(此记录要同步到数据库) 元组dict字典格式必须内层再套() 后与动作关联起来django做了把权限和用户关联并判断有没有权限
    # class Meta:     # 写哪里都一样, 移到customer表
    #    permissions =(('can_del_customer', u"可删除用户"),)

    def colored_status(self):   # 写入admin加入字段
        if self.status == "signed":   # 如果状态时publish的让其闪显示
            format_td = format_html('<span style="padding:2px;background-color:yellowgreen;color:white">运行中</span>')    # format_html()功能帮你在前端转成html格式, 需要导入from django.utils.html import format_html
        elif self.status == "unregistered":
            format_td = format_html('<span style="padding:2px;background-color:red;color:white">宕机</span>')
        elif self.status == "working":
            format_td = format_html('<span style="padding:2px;background-color:green:white">运行中</span>')
        elif self.status == "down-off":
            format_td = format_html('<span style="padding:2px;background-color:red;color:white">宕机</span>')

        return format_td
    colored_status.short_description = 'status'    # 将colored_status改名成status


class HostServer04(models.Model):
    host = models.CharField(u"主机ip",max_length=64,unique=True)
    name = models.CharField(u"主机名",max_length=64,blank=True,null=True)
    phone = models.BigIntegerField(u'联系电话',blank=True,null=True)
    stu_id = models.CharField(u"主机编号",blank=True,null=True,max_length=64)
    #id = models.CharField(u"身份证号",blank=True,null=True,max_length=128)
    source_type_choices = (('yunwei',u"运维人员创建"),
                   ('referral',u"内部冗余备机"),
                   ('chengdu',u"成都创建"),
                   ('guanwu',u"关务开发创建"),
                   ('qingsuan',u"清算开发创建"),
                   ('dbserver',u"数据库开发创建"),
                   ('others',u"其它"),
                   )
    source_type = models.CharField(u'主机创建来源',max_length=64, choices=source_type_choices,default='yunwei')
    # 如果是内部创建关联'self'，内部转自测试，用ForeignKey, 反查自己用related_name="internal_referral"如果不起个名字叫related_name直接Customer="internal_referral"
    referral_from = models.ForeignKey('self',verbose_name=u"转相关备机",help_text=u"若此主机是转备份做其它主机备机用,请在此处选择主机名称",blank=True,null=True,related_name="referraled_who",on_delete=models.CASCADE)

    server = models.ForeignKey(Server,verbose_name=u"主机创建需求",on_delete=models.CASCADE)    # 关联到Server服务器类下的所有内容所以用ForeignKey
    server_type = models.CharField(u"服务器环境类型",max_length=64,choices=server_type_choices,default='test')
    server_memo = models.TextField(u"主机需创建前内容详情",help_text=u"主机需创建前的大概情况,主机信息备注等...")
    status_choices = (('signed',u"运行中"),
                      ('unregistered',u"宕机"),
                      ('working',u"运行中"),
                      ('down-off',u"宕机"),
                      )

    status = models.CharField(u"状态",choices=status_choices,max_length=64,default=u"unregistered",help_text=u"选择服务器主机此时的状态")
    consultant = models.ForeignKey(UserProfile,verbose_name=u"需求人姓名",on_delete=models.CASCADE)
    date = models.DateField(u"提需求日期",auto_now_add=True)

    server_list = models.ManyToManyField('ServerList',verbose_name=u"服务应用类型",blank=True)

    def __str__(self):
        return "%s,%s" %(self.host,self.name )
    # 增加customer表里对用户的权限操作功能(此记录要同步到数据库) 元组dict字典格式必须内层再套() 后与动作关联起来django做了把权限和用户关联并判断有没有权限
    # class Meta:     # 写哪里都一样, 移到customer表
    #    permissions =(('can_del_customer', u"可删除用户"),)

    def colored_status(self):   # 写入admin加入字段
        if self.status == "signed":   # 如果状态时publish的让其闪显示
            format_td = format_html('<span style="padding:2px;background-color:yellowgreen;color:white">运行中</span>')    # format_html()功能帮你在前端转成html格式, 需要导入from django.utils.html import format_html
        elif self.status == "unregistered":
            format_td = format_html('<span style="padding:2px;background-color:red;color:white">宕机</span>')
        elif self.status == "working":
            format_td = format_html('<span style="padding:2px;background-color:green:white">运行中</span>')
        elif self.status == "down-off":
            format_td = format_html('<span style="padding:2px;background-color:red;color:white">宕机</span>')

        return format_td
    colored_status.short_description = 'status'    # 将colored_status改名成status


class HostServer05(models.Model):
    host = models.CharField(u"主机ip",max_length=64,unique=True)
    name = models.CharField(u"主机名",max_length=64,blank=True,null=True)
    phone = models.BigIntegerField(u'联系电话',blank=True,null=True)
    stu_id = models.CharField(u"主机编号",blank=True,null=True,max_length=64)
    #id = models.CharField(u"身份证号",blank=True,null=True,max_length=128)
    source_type_choices = (('yunwei',u"运维人员创建"),
                   ('referral',u"内部冗余备机"),
                   ('chengdu',u"成都创建"),
                   ('guanwu',u"关务开发创建"),
                   ('qingsuan',u"清算开发创建"),
                   ('dbserver',u"数据库开发创建"),
                   ('others',u"其它"),
                   )
    source_type = models.CharField(u'主机创建来源',max_length=64, choices=source_type_choices,default='yunwei')
    # 如果是内部创建关联'self'，内部转自测试，用ForeignKey, 反查自己用related_name="internal_referral"如果不起个名字叫related_name直接Customer="internal_referral"
    referral_from = models.ForeignKey('self',verbose_name=u"转相关备机",help_text=u"若此主机是转备份做其它主机备机用,请在此处选择主机名称",blank=True,null=True,related_name="referraled_who",on_delete=models.CASCADE)

    server = models.ForeignKey(Server,verbose_name=u"主机创建需求",on_delete=models.CASCADE)    # 关联到Server服务器类下的所有内容所以用ForeignKey
    server_type = models.CharField(u"服务器环境类型",max_length=64,choices=server_type_choices,default='test')
    server_memo = models.TextField(u"主机需创建前内容详情",help_text=u"主机需创建前的大概情况,主机信息备注等...")
    status_choices = (('signed',u"运行中"),
                      ('unregistered',u"宕机"),
                      ('working',u"运行中"),
                      ('down-off',u"宕机"),
                      )

    status = models.CharField(u"状态",choices=status_choices,max_length=64,default=u"unregistered",help_text=u"选择服务器主机此时的状态")
    consultant = models.ForeignKey(UserProfile,verbose_name=u"需求人姓名",on_delete=models.CASCADE)
    date = models.DateField(u"提需求日期",auto_now_add=True)

    server_list = models.ManyToManyField('ServerList',verbose_name=u"服务应用类型",blank=True)

    def __str__(self):
        return "%s,%s" %(self.host,self.name )
    # 增加customer表里对用户的权限操作功能(此记录要同步到数据库) 元组dict字典格式必须内层再套() 后与动作关联起来django做了把权限和用户关联并判断有没有权限
    # class Meta:     # 写哪里都一样, 移到customer表
    #    permissions =(('can_del_customer', u"可删除用户"),)

    def colored_status(self):   # 写入admin加入字段
        if self.status == "signed":   # 如果状态时publish的让其闪显示
            format_td = format_html('<span style="padding:2px;background-color:yellowgreen;color:white">运行中</span>')    # format_html()功能帮你在前端转成html格式, 需要导入from django.utils.html import format_html
        elif self.status == "unregistered":
            format_td = format_html('<span style="padding:2px;background-color:red;color:white">宕机</span>')
        elif self.status == "working":
            format_td = format_html('<span style="padding:2px;background-color:green:white">运行中</span>')
        elif self.status == "down-off":
            format_td = format_html('<span style="padding:2px;background-color:red;color:white">宕机</span>')

        return format_td
    colored_status.short_description = 'status'    # 将colored_status改名成status


class HostServer06(models.Model):
    host = models.CharField(u"主机ip",max_length=64,unique=True)
    name = models.CharField(u"主机名",max_length=64,blank=True,null=True)
    phone = models.BigIntegerField(u'联系电话',blank=True,null=True)
    stu_id = models.CharField(u"主机编号",blank=True,null=True,max_length=64)
    #id = models.CharField(u"身份证号",blank=True,null=True,max_length=128)
    source_type_choices = (('yunwei',u"运维人员创建"),
                   ('referral',u"内部冗余备机"),
                   ('chengdu',u"成都创建"),
                   ('guanwu',u"关务开发创建"),
                   ('qingsuan',u"清算开发创建"),
                   ('dbserver',u"数据库开发创建"),
                   ('others',u"其它"),
                   )
    source_type = models.CharField(u'主机创建来源',max_length=64, choices=source_type_choices,default='yunwei')
    # 如果是内部创建关联'self'，内部转自测试，用ForeignKey, 反查自己用related_name="internal_referral"如果不起个名字叫related_name直接Customer="internal_referral"
    referral_from = models.ForeignKey('self',verbose_name=u"转相关备机",help_text=u"若此主机是转备份做其它主机备机用,请在此处选择主机名称",blank=True,null=True,related_name="referraled_who",on_delete=models.CASCADE)

    server = models.ForeignKey(Server,verbose_name=u"主机创建需求",on_delete=models.CASCADE)    # 关联到Server服务器类下的所有内容所以用ForeignKey
    server_type = models.CharField(u"服务器环境类型",max_length=64,choices=server_type_choices,default='test')
    server_memo = models.TextField(u"主机需创建前内容详情",help_text=u"主机需创建前的大概情况,主机信息备注等...")
    status_choices = (('signed',u"运行中"),
                      ('unregistered',u"宕机"),
                      ('working',u"运行中"),
                      ('down-off',u"宕机"),
                      )

    status = models.CharField(u"状态",choices=status_choices,max_length=64,default=u"unregistered",help_text=u"选择服务器主机此时的状态")
    consultant = models.ForeignKey(UserProfile,verbose_name=u"需求人姓名",on_delete=models.CASCADE)
    date = models.DateField(u"提需求日期",auto_now_add=True)

    server_list = models.ManyToManyField('ServerList',verbose_name=u"服务应用类型",blank=True)

    def __str__(self):
        return "%s,%s" %(self.host,self.name )
    # 增加customer表里对用户的权限操作功能(此记录要同步到数据库) 元组dict字典格式必须内层再套() 后与动作关联起来django做了把权限和用户关联并判断有没有权限
    # class Meta:     # 写哪里都一样, 移到customer表
    #    permissions =(('can_del_customer', u"可删除用户"),)

    def colored_status(self):   # 写入admin加入字段
        if self.status == "signed":   # 如果状态时publish的让其闪显示
            format_td = format_html('<span style="padding:2px;background-color:yellowgreen;color:white">运行中</span>')    # format_html()功能帮你在前端转成html格式, 需要导入from django.utils.html import format_html
        elif self.status == "unregistered":
            format_td = format_html('<span style="padding:2px;background-color:red;color:white">宕机</span>')
        elif self.status == "working":
            format_td = format_html('<span style="padding:2px;background-color:green:white">运行中</span>')
        elif self.status == "down-off":
            format_td = format_html('<span style="padding:2px;background-color:red;color:white">宕机</span>')

        return format_td
    colored_status.short_description = 'status'    # 将colored_status改名成status


class HostServer07(models.Model):
    host = models.CharField(u"主机ip",max_length=64,unique=True)
    name = models.CharField(u"主机名",max_length=64,blank=True,null=True)
    phone = models.BigIntegerField(u'联系电话',blank=True,null=True)
    stu_id = models.CharField(u"主机编号",blank=True,null=True,max_length=64)
    #id = models.CharField(u"身份证号",blank=True,null=True,max_length=128)
    source_type_choices = (('yunwei',u"运维人员创建"),
                   ('referral',u"内部冗余备机"),
                   ('chengdu',u"成都创建"),
                   ('guanwu',u"关务开发创建"),
                   ('qingsuan',u"清算开发创建"),
                   ('dbserver',u"数据库开发创建"),
                   ('others',u"其它"),
                   )
    source_type = models.CharField(u'主机创建来源',max_length=64, choices=source_type_choices,default='yunwei')
    # 如果是内部创建关联'self'，内部转自测试，用ForeignKey, 反查自己用related_name="internal_referral"如果不起个名字叫related_name直接Customer="internal_referral"
    referral_from = models.ForeignKey('self',verbose_name=u"转相关备机",help_text=u"若此主机是转备份做其它主机备机用,请在此处选择主机名称",blank=True,null=True,related_name="referraled_who",on_delete=models.CASCADE)

    server = models.ForeignKey(Server,verbose_name=u"主机创建需求",on_delete=models.CASCADE)    # 关联到Server服务器类下的所有内容所以用ForeignKey
    server_type = models.CharField(u"服务器环境类型",max_length=64,choices=server_type_choices,default='test')
    server_memo = models.TextField(u"主机需创建前内容详情",help_text=u"主机需创建前的大概情况,主机信息备注等...")
    status_choices = (('signed',u"运行中"),
                      ('unregistered',u"宕机"),
                      ('working',u"运行中"),
                      ('down-off',u"宕机"),
                      )

    status = models.CharField(u"状态",choices=status_choices,max_length=64,default=u"unregistered",help_text=u"选择服务器主机此时的状态")
    consultant = models.ForeignKey(UserProfile,verbose_name=u"需求人姓名",on_delete=models.CASCADE)
    date = models.DateField(u"提需求日期",auto_now_add=True)

    server_list = models.ManyToManyField('ServerList',verbose_name=u"服务应用类型",blank=True)

    def __str__(self):
        return "%s,%s" %(self.host,self.name )
    # 增加customer表里对用户的权限操作功能(此记录要同步到数据库) 元组dict字典格式必须内层再套() 后与动作关联起来django做了把权限和用户关联并判断有没有权限
    # class Meta:     # 写哪里都一样, 移到customer表
    #    permissions =(('can_del_customer', u"可删除用户"),)

    def colored_status(self):   # 写入admin加入字段
        if self.status == "signed":   # 如果状态时publish的让其闪显示
            format_td = format_html('<span style="padding:2px;background-color:yellowgreen;color:white">运行中</span>')    # format_html()功能帮你在前端转成html格式, 需要导入from django.utils.html import format_html
        elif self.status == "unregistered":
            format_td = format_html('<span style="padding:2px;background-color:red;color:white">宕机</span>')
        elif self.status == "working":
            format_td = format_html('<span style="padding:2px;background-color:green:white">运行中</span>')
        elif self.status == "down-off":
            format_td = format_html('<span style="padding:2px;background-color:red;color:white">宕机</span>')

        return format_td
    colored_status.short_description = 'status'    # 将colored_status改名成status


class HostServer08(models.Model):
    host = models.CharField(u"主机ip",max_length=64,unique=True)
    name = models.CharField(u"主机名",max_length=64,blank=True,null=True)
    phone = models.BigIntegerField(u'联系电话',blank=True,null=True)
    stu_id = models.CharField(u"主机编号",blank=True,null=True,max_length=64)
    #id = models.CharField(u"身份证号",blank=True,null=True,max_length=128)
    source_type_choices = (('yunwei',u"运维人员创建"),
                   ('referral',u"内部冗余备机"),
                   ('chengdu',u"成都创建"),
                   ('guanwu',u"关务开发创建"),
                   ('qingsuan',u"清算开发创建"),
                   ('dbserver',u"数据库开发创建"),
                   ('others',u"其它"),
                   )
    source_type = models.CharField(u'主机创建来源',max_length=64, choices=source_type_choices,default='yunwei')
    # 如果是内部创建关联'self'，内部转自测试，用ForeignKey, 反查自己用related_name="internal_referral"如果不起个名字叫related_name直接Customer="internal_referral"
    referral_from = models.ForeignKey('self',verbose_name=u"转相关备机",help_text=u"若此主机是转备份做其它主机备机用,请在此处选择主机名称",blank=True,null=True,related_name="referraled_who",on_delete=models.CASCADE)

    server = models.ForeignKey(Server,verbose_name=u"主机创建需求",on_delete=models.CASCADE)    # 关联到Server服务器类下的所有内容所以用ForeignKey
    server_type = models.CharField(u"服务器环境类型",max_length=64,choices=server_type_choices,default='test')
    server_memo = models.TextField(u"主机需创建前内容详情",help_text=u"主机需创建前的大概情况,主机信息备注等...")
    status_choices = (('signed',u"运行中"),
                      ('unregistered',u"宕机"),
                      ('working',u"运行中"),
                      ('down-off',u"宕机"),
                      )

    status = models.CharField(u"状态",choices=status_choices,max_length=64,default=u"unregistered",help_text=u"选择服务器主机此时的状态")
    consultant = models.ForeignKey(UserProfile,verbose_name=u"需求人姓名",on_delete=models.CASCADE)
    date = models.DateField(u"提需求日期",auto_now_add=True)

    server_list = models.ManyToManyField('ServerList',verbose_name=u"服务应用类型",blank=True)

    def __str__(self):
        return "%s,%s" %(self.host,self.name )
    # 增加customer表里对用户的权限操作功能(此记录要同步到数据库) 元组dict字典格式必须内层再套() 后与动作关联起来django做了把权限和用户关联并判断有没有权限
    # class Meta:     # 写哪里都一样, 移到customer表
    #    permissions =(('can_del_customer', u"可删除用户"),)

    def colored_status(self):   # 写入admin加入字段
        if self.status == "signed":   # 如果状态时publish的让其闪显示
            format_td = format_html('<span style="padding:2px;background-color:yellowgreen;color:white">运行中</span>')    # format_html()功能帮你在前端转成html格式, 需要导入from django.utils.html import format_html
        elif self.status == "unregistered":
            format_td = format_html('<span style="padding:2px;background-color:red;color:white">宕机</span>')
        elif self.status == "working":
            format_td = format_html('<span style="padding:2px;background-color:green:white">运行中</span>')
        elif self.status == "down-off":
            format_td = format_html('<span style="padding:2px;background-color:red;color:white">宕机</span>')

        return format_td
    colored_status.short_description = 'status'    # 将colored_status改名成status


class HostServerTrackRecord(models.Model):    # 服务器主机需求跟踪表
    hostserver = models.ForeignKey(HostServer,verbose_name=u"服务器主机名称",on_delete=models.CASCADE)
    track_record = models.TextField(u"跟踪记录")
    #track_date = models.Date(u"跟进日期",auto)
    track_date = models.DateTimeField(u"跟进日期",auto_now_add=True)
    follower = models.ForeignKey(UserProfile,verbose_name=u"跟踪人",on_delete=models.CASCADE)
    status_choices = ((1,u"近期无开启计划"),
                      (2,u"2个月内开启"),
                      (3,u"1个月内开启"),
                      (4,u"2周内开启"),
                      (5,u"1周内开启"),
                      (6,u"2天内开启"),
                      (7,u"已开启"),
                      )
    status = models.IntegerField(u"状态",choices=status_choices,help_text=u"选择需求服务器此时的状态")
    def __str__(self):
        return u"%s, %s" %(self.customer,self.status)

    class Meta:
        verbose_name = u'服务器需求主机跟进记录'
        verbose_name_plural = u"服务器需求主机跟进记录"


class ServerList(models.Model):
    server = models.ForeignKey(Server,verbose_name=u"服务环境名称",on_delete=models.CASCADE)     # 服务器名称是一样的需要关联
    server_type = models.CharField(verbose_name=u"服务器环境类型",choices=server_type_choices,max_length=64)
    semester = models.IntegerField(verbose_name=u"开启服务批次")
    start_date = models.DateField(verbose_name=u"开服日期")
    drop_date = models.DateField(verbose_name=u"停服日期",blank=True,null=True)
    # 负责人需要关联到UserProfile
    manager = models.ManyToManyField(UserProfile,verbose_name=u"责任人")
    def __str__(self):
        return "%s(%s)[%s]" %(self.server.name,self.get_server_type_display(),self.semester)
    class Meta:     # 使其在admin中显示中文
        verbose_name = u'服务器主机列表'
        verbose_name_plural = u"服务器主机列表"
        unique_together = ("server","server_type","semester")      # 服务器名　+ 类型 + 第几期批次　并且需要分类是server_type


class ServerRecord(models.Model):
    server_obj = models.ForeignKey(ServerList,verbose_name=u"服务应用名称(环境)",on_delete=models.CASCADE)
    day_num = models.IntegerField(u"第几次",help_text=u"此处填写第几次修改或第几天修改应用...,必须为数字")
    modify_date = models.DateField(auto_now_add=True,verbose_name=u"修改日期")
    manager = models.ForeignKey(UserProfile,verbose_name=u"责任人",on_delete=models.CASCADE)
    def __str__(self):
        return u"%s 第%s天" %(self.server_obj,self.day_num)
    class Meta:
        verbose_name = u'服务器功能修改纪录'
        verbose_name_plural = u"服务器功能修改纪录"
        unique_together = ('server_obj','day_num')


class HostRecord(models.Model):
    server_record = models.ForeignKey(ServerRecord, verbose_name=u"第几次修改主机",on_delete=models.CASCADE)
    server_name = models.ForeignKey(HostServer,verbose_name=u"主机名",on_delete=models.CASCADE)
    record_choices = (('checked', u"已修改"),
                      ('late',u"未修改"),
                      ('noshow',u"无需修改"),
                      ('leave_early',u"任务撤销"),
                      )
    record = models.CharField(u"修改纪录",choices=record_choices,default="checked",max_length=64)
    score_choices = ((100, 'A+'),
                     (90,'A'),
                     (85,'B+'),
                     (80,'B'),
                     (70,'B-'),
                     (60,'C+'),
                     (50,'C'),
                     (40,'C-'),
                     (0,'D'),
                     (-1,'N/A'),
                     (-100,'COPY'),
                     (-1000,'FAIL'),
                     )
    score = models.IntegerField(u"此次修改任务完成进度",choices=score_choices,default=-1)
    date = models.DateTimeField(auto_now_add=True)
    note = models.CharField(u"备注",max_length=255,blank=True,null=True)

    def __str__(self):
        return u"%s,主机名:%s,修改纪录:%s, 完成进度:%s" %(self.server_record,self.server_name.name,self.record,self.get_score_display())

    class Meta:
        verbose_name = u'服务器主机修改纪录'
        verbose_name_plural = u"服务器主机修改纪录"
        #unique_together = ('server_record',' server_name')
        unique_together = ('server_record','server_name')