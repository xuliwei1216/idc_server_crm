#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:xuliwei
#from django.core.urlresolvers import resolve    # 适用1.9
from django.urls import resolve                  # 适用2.0
from django.shortcuts import render,redirect

# 和models里的数据库userprofile用户权限权限信息相关联
perm_dic = {
    'view_hostserver_list': ['hostserver_list','GET',[]],
    'view_hostserver_info': ['hostserver_detail','GET',[]],
    'edit_own_hostserver_info': ['hostserver_detail','POST',['host','name','phone','stu_id','source_type_choices','source_type','referral_from','server','server_type','server_memo','status_choices','status','consultant','date','server_list','colored_status']],
}


def perm_check(*args,**kwargs):
    request = args[0]
    url_resovle_obj = resolve(request.path_info)   # 通过resolve的方法将url路径转换为字符串形式即url中的别名
    current_url_namespace = url_resovle_obj.url_name
    #app_name = url_resovle_obj.app_name #use this name later
    print("url namespace:",current_url_namespace)
    matched_flag = False # find matched perm item
    matched_perm_key = None
    if current_url_namespace is not None:#if didn't set the url namespace, permission doesn't work
        print("find perm...")
        for perm_key in perm_dic:
            perm_val = perm_dic[perm_key]    # perm_val 就是: ['hostserver_list','GET',[]] 冒号后面的值
            if len(perm_val) == 3:#otherwise invalid perm data format  格式必须满足有三个值
                url_namespace,request_method,request_args = perm_val  # 别名方法和参数
                print(url_namespace,current_url_namespace)
                if url_namespace == current_url_namespace: #matched the url   # 三个匹配url相等
                    if request.method == request_method:#matched request method   # 方法相等
                        if not request_args:#if empty , pass        # 先判断参数是否为空， 此处为空直接就匹配上了
                            matched_flag = True
                            matched_perm_key = perm_key             # 参数与数据库相等（皆为从url。py中调views再调数据库）此处前两个已匹配直接赋值matched_perm_key = None
                            print('mtched...')
                            break #no need looking for  other perms
                        else:    # 如果不为空 循环url
                            for request_arg in request_args: #might has many args 循环分页的参数比对
                                # 通过反射取值得到方法
                                request_method_func = getattr(request,request_method) #get or post mostly
                                #print("----->>>",request_method_func.get(request_arg))
                                if request_method_func.get(request_arg) is not None:# 如何可以get到
                                    matched_flag = True # the arg in set in perm item must be provided in request data
                                else:
                                    matched_flag = False
                                    print("request arg [%s] not matched" % request_arg)
                                    break #no need go further
                            # 上面三个参数全匹配上此下再要做次判断 作用是如果全匹配上了就break跳出循环--否则就不执行再重复上面的for循环for perm_key in perm_dic:
                            if matched_flag == True: # means passed permission check ,no need check others
                                print("--passed permission check--")
                                matched_perm_key = perm_key
                                break

    else:#permission doesn't work
        return True   # 默认放过还是拒绝 false为拒绝

    if matched_flag == True:
        #pass permission check
        perm_str = "crm.%s" %(matched_perm_key)    # 类似于拼接成crm.view_hostserver_list
        if request.user.has_perm(perm_str):   # 从crm的函数里判断是否有权限
            print("\033[42;1m--------passed permission check----\033[0m")
            return True
        else:
            print("\033[41;1m ----- no permission ----\033[0m")
            print(request.user,perm_str)
            return False
    else:
        print("\033[41;1m ----- no matched permission  ----\033[0m")


# 装饰器函数必须传入两层第一层func传的是自己，在装饰器里把动作拼起来
def check_permission(func):
    def wrapper(*args,**kwargs):
        print('---start check perm---')
        # 做判断后调用函数，将用户和数据传入先做次检测
        if not perm_check(*args,**kwargs):   # 最终返回到此处，如果没有权限直接跳转到403页面可以写成if perm_check(*args,**kwargs) is not True:
            return render(args[0],'crm/403.html')  # args传过来的值0就是那个request
        # 执行你要装饰的函数
        return func(*args,**kwargs)
    return wrapper
