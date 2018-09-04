#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:Xuliwei
# 引入form表单格式
from django.forms import Form,ModelForm
from crm import models

class HostServerModelForm(ModelForm):
    class Meta:
        model = models.HostServer
        exclude = ()
    # 重写modelForm类的初始化方法：
    def __init__(self,*args,**kwargs):
        super(HostServerModelForm,self).__init__(*args,**kwargs)
        # 以下写入自己的样式  下面一段为重写加入新样试 只能给一个字段加样式
        #self.fields['qq'].widget.attrs["class"] = "form-control"
        # 以下为给所有字段加入样式
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            # 可以修改update中的多个属性  给所有字段加上相同属性
            field.widget.attrs.update({'class':'form-control'})    # 要变表单保存去hostserver_detail.html中操作
