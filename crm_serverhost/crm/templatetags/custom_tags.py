#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:Xuliwei
# 页面分页栏最小化数字功能模块 导入到前端 数字转大写
from django import template
# 引入模块让前段识别后台写的前端样式
from django.utils.html import format_html
#from django.template.defaultfilters import
#stringfilter

# 自己写个语法并注册到语法库里
register = template.Library()

# 定义装饰器把其注册到语法库并过滤语法并改变样式
@register.filter
#@stringfilter
def xlw_upper(val):
    # 将前端获取的值customer.status | xlw_upper这样传给后端并打印出来
    print("--val from template:",val )
    return val.upper()

# 定义一个装饰器注册一个simple_tag
@register.simple_tag
def guess_page(current_page,loop_num):
#    将前端的判断写入后端
#    {% if page_num == customer_list.number %}
#        <li class="active"><a href="?page={{ page_num }}">{{ page_num }}<span class="sr-only">(current)</span></a></li>
#    {% else %}
#        <li class=""><a href="?page={{ page_num }}">{{ page_num }}<span class="sr-only">(current)</span></a></li>
#    {% endif %}
    offset = abs(current_page - loop_num)
    if offset < 3:
        if current_page == loop_num:
            # 传入的是loop_num 循环的数据
            page_ele = '''<li class="active"><a href="?page=%s">%s<span class="sr-only">(current)</span></a></li>''' %(loop_num,loop_num)
        else:
            page_ele = '''<li class=""><a href="?page=%s">%s<span class="sr-only">(current)</span></a></li>''' %(loop_num,loop_num)
        # 返回样式需用format_html转换格式 django 1.6之后
        return format_html(page_ele)
    # 如果返回不小于3返回个空字符串
    else:
        return ''
