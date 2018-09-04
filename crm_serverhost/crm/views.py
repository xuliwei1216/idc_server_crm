from django.shortcuts import render,redirect
from crm import models
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from crm import forms
from crm import check01_up_down
from crm import check02_up_down
import math
from crm.permissions import check_permission

# Create your views here.
count_page = 10

def dashboard(request):
    return render(request,'crm/hostserver.html')

# 通过装饰器实现用户权限关联
#@check_permission
def hostserver(request):
    #check01_up_down.check()
    hostserver_list = models.HostServer.objects.all()
    paginator = Paginator(hostserver_list,count_page)
    page = request.GET.get('page')     # 前端请求传入
    try:
        hostserver_objs = paginator.page(page)
    except PageNotAnInteger:     # 如果输入的不是数字的话  等同于第一次打开页面就跳转到第一页面
        hostserver_objs = paginator.page(1)     # 输入错误返回第一页
    except EmptyPage:     # 如果输入超出范围
        hostserver_objs = paginator.page(paginator.num_pages)      # 一共多少页就返回最后那页面
    
    
    return render(request,'crm/hostserver.html',{'hostserver_list':hostserver_objs})

@check_permission
def hostserver_detail(request,hostserver_id):
    # 两种情况 一种是获取客户详细信息 另一种是修改客户详细信息 同过前端传入hostserver_id根据其取值
    hostserver_obj = models.HostServer.objects.get(id=hostserver_id)
    if request.method == "POST":
        # 根据前端提交过来的值进行验证 request.POST把用户提交的数据传入 需要修改的是instance=hostserver_obj
        form = forms.HostServerModelForm(request.POST,instance=hostserver_obj)
        print(request.POST)
        if form.is_valid():
            form.save()
            # 需要通过redirect进行动态跳转
            print('url:', request.path)  # 获取当前页面的url
            a = "/".join(request.path.split("/")[-2])
            b = math.ceil(int(a) / int(count_page))
            print(a)
            print(b)
            #base_url = "/".join(request.path.split("/")[0:-2])  # 以"/"分割取需要字段去除id
            base_url = "/".join(request.path.split("/")[0:-2]) + "/?page=" + "%s" %(b)      # 以"/"分割取需要字段去除id
            print(base_url)
            print('url:', base_url)
            return redirect(base_url)
    else:
        # 将hostserver_obj读到的数据装入form(instance=hostserver_obj)
        form = forms.HostServerModelForm(instance=hostserver_obj)
    return render(request,'crm/hostserver_detail.html',{'hostserver_form':form})

###############################################################################################################################################################

#@check_permission
def hostserver01(request):
    #check02_up_down.check()
    hostserver_list = models.HostServer01.objects.all()
    paginator = Paginator(hostserver_list, count_page)
    page = request.GET.get('page')  # 前端请求传入
    try:
        hostserver_objs = paginator.page(page)
    except PageNotAnInteger:  # 如果输入的不是数字的话  等同于第一次打开页面就跳转到第一页面
        hostserver_objs = paginator.page(1)  # 输入错误返回第一页
    except EmptyPage:  # 如果输入超出范围
        hostserver_objs = paginator.page(paginator.num_pages)  # 一共多少页就返回最后那页面

    return render(request, 'crm/hostserver01.html', {'hostserver_list': hostserver_objs})


@check_permission
def hostserver_detail01(request, hostserver_id):
    # 两种情况 一种是获取客户详细信息 另一种是修改客户详细信息 同过前端传入hostserver_id根据其取值
    hostserver_obj = models.HostServer01.objects.get(id=hostserver_id)
    if request.method == "POST":
        # 根据前端提交过来的值进行验证 request.POST把用户提交的数据传入 需要修改的是instance=hostserver_obj
        form = forms.HostServer01ModelForm(request.POST, instance=hostserver_obj)
        print(request.POST)
        if form.is_valid():
            form.save()
            # 需要通过redirect进行动态跳转
            print('url:', request.path)  # 获取当前页面的url
            a = "/".join(request.path.split("/")[-2])
            b = math.ceil(int(a) / int(count_page))
            print(a)
            print(b)
            # base_url = "/".join(request.path.split("/")[0:-2])  # 以"/"分割取需要字段去除id
            base_url = "/".join(request.path.split("/")[0:-2]) + "/?page=" + "%s" % (b)  # 以"/"分割取需要字段去除id
            print(base_url)
            print('url:', base_url)
            return redirect(base_url)
    else:
        # 将hostserver_obj读到的数据装入form(instance=hostserver_obj)
        form = forms.HostServer01ModelForm(instance=hostserver_obj)
    return render(request, 'crm/hostserver_detail01.html', {'hostserver_form': form})

######################################################################################################################################

#@check_permission
def hostserver02(request):
    hostserver_list = models.HostServer02.objects.all()
    paginator = Paginator(hostserver_list, count_page)
    page = request.GET.get('page')  # 前端请求传入
    try:
        hostserver_objs = paginator.page(page)
    except PageNotAnInteger:  # 如果输入的不是数字的话  等同于第一次打开页面就跳转到第一页面
        hostserver_objs = paginator.page(1)  # 输入错误返回第一页
    except EmptyPage:  # 如果输入超出范围
        hostserver_objs = paginator.page(paginator.num_pages)  # 一共多少页就返回最后那页面

    return render(request, 'crm/hostserver02.html', {'hostserver_list': hostserver_objs})


@check_permission
def hostserver_detail02(request, hostserver_id):
    # 两种情况 一种是获取客户详细信息 另一种是修改客户详细信息 同过前端传入hostserver_id根据其取值
    hostserver_obj = models.HostServer02.objects.get(id=hostserver_id)
    if request.method == "POST":
        # 根据前端提交过来的值进行验证 request.POST把用户提交的数据传入 需要修改的是instance=hostserver_obj
        form = forms.HostServer02ModelForm(request.POST, instance=hostserver_obj)
        print(request.POST)
        if form.is_valid():
            form.save()
            # 需要通过redirect进行动态跳转
            print('url:', request.path)  # 获取当前页面的url
            a = "/".join(request.path.split("/")[-2])
            b = math.ceil(int(a) / int(count_page))
            print(a)
            print(b)
            # base_url = "/".join(request.path.split("/")[0:-2])  # 以"/"分割取需要字段去除id
            base_url = "/".join(request.path.split("/")[0:-2]) + "/?page=" + "%s" % (b)  # 以"/"分割取需要字段去除id
            print(base_url)
            print('url:', base_url)
            return redirect(base_url)
    else:
        # 将hostserver_obj读到的数据装入form(instance=hostserver_obj)
        form = forms.HostServer02ModelForm(instance=hostserver_obj)
    return render(request, 'crm/hostserver_detail02.html', {'hostserver_form': form})

######################################################################################################################################

#@check_permission
def hostserver03(request):
    hostserver_list = models.HostServer03.objects.all()
    paginator = Paginator(hostserver_list, count_page)
    page = request.GET.get('page')  # 前端请求传入
    try:
        hostserver_objs = paginator.page(page)
    except PageNotAnInteger:  # 如果输入的不是数字的话  等同于第一次打开页面就跳转到第一页面
        hostserver_objs = paginator.page(1)  # 输入错误返回第一页
    except EmptyPage:  # 如果输入超出范围
        hostserver_objs = paginator.page(paginator.num_pages)  # 一共多少页就返回最后那页面

    return render(request, 'crm/hostserver03.html', {'hostserver_list': hostserver_objs})


@check_permission
def hostserver_detail03(request, hostserver_id):
    # 两种情况 一种是获取客户详细信息 另一种是修改客户详细信息 同过前端传入hostserver_id根据其取值
    hostserver_obj = models.HostServer03.objects.get(id=hostserver_id)
    if request.method == "POST":
        # 根据前端提交过来的值进行验证 request.POST把用户提交的数据传入 需要修改的是instance=hostserver_obj
        form = forms.HostServer03ModelForm(request.POST, instance=hostserver_obj)
        print(request.POST)
        if form.is_valid():
            form.save()
            # 需要通过redirect进行动态跳转
            print('url:', request.path)  # 获取当前页面的url
            a = "/".join(request.path.split("/")[-2])
            b = math.ceil(int(a) / int(count_page))
            print(a)
            print(b)
            # base_url = "/".join(request.path.split("/")[0:-2])  # 以"/"分割取需要字段去除id
            base_url = "/".join(request.path.split("/")[0:-2]) + "/?page=" + "%s" % (b)  # 以"/"分割取需要字段去除id
            print(base_url)
            print('url:', base_url)
            return redirect(base_url)
    else:
        # 将hostserver_obj读到的数据装入form(instance=hostserver_obj)
        form = forms.HostServer03ModelForm(instance=hostserver_obj)
    return render(request, 'crm/hostserver_detail03.html', {'hostserver_form': form})

################################################################################################################################

#@check_permission
def hostserver04(request):
    hostserver_list = models.HostServer04.objects.all()
    paginator = Paginator(hostserver_list, count_page)
    page = request.GET.get('page')  # 前端请求传入
    try:
        hostserver_objs = paginator.page(page)
    except PageNotAnInteger:  # 如果输入的不是数字的话  等同于第一次打开页面就跳转到第一页面
        hostserver_objs = paginator.page(1)  # 输入错误返回第一页
    except EmptyPage:  # 如果输入超出范围
        hostserver_objs = paginator.page(paginator.num_pages)  # 一共多少页就返回最后那页面

    return render(request, 'crm/hostserver04.html', {'hostserver_list': hostserver_objs})


@check_permission
def hostserver_detail04(request, hostserver_id):
    # 两种情况 一种是获取客户详细信息 另一种是修改客户详细信息 同过前端传入hostserver_id根据其取值
    hostserver_obj = models.HostServer04.objects.get(id=hostserver_id)
    if request.method == "POST":
        # 根据前端提交过来的值进行验证 request.POST把用户提交的数据传入 需要修改的是instance=hostserver_obj
        form = forms.HostServer04ModelForm(request.POST, instance=hostserver_obj)
        print(request.POST)
        if form.is_valid():
            form.save()
            # 需要通过redirect进行动态跳转
            print('url:', request.path)  # 获取当前页面的url
            a = "/".join(request.path.split("/")[-2])
            b = math.ceil(int(a) / int(count_page))
            print(a)
            print(b)
            # base_url = "/".join(request.path.split("/")[0:-2])  # 以"/"分割取需要字段去除id
            base_url = "/".join(request.path.split("/")[0:-2]) + "/?page=" + "%s" % (b)  # 以"/"分割取需要字段去除id
            print(base_url)
            print('url:', base_url)
            return redirect(base_url)
    else:
        # 将hostserver_obj读到的数据装入form(instance=hostserver_obj)
        form = forms.HostServer04ModelForm(instance=hostserver_obj)
    return render(request, 'crm/hostserver_detail04.html', {'hostserver_form': form})

###################################################################################################################################################

#@check_permission
def hostserver05(request):
    hostserver_list = models.HostServer05.objects.all()
    paginator = Paginator(hostserver_list, count_page)
    page = request.GET.get('page')  # 前端请求传入
    try:
        hostserver_objs = paginator.page(page)
    except PageNotAnInteger:  # 如果输入的不是数字的话  等同于第一次打开页面就跳转到第一页面
        hostserver_objs = paginator.page(1)  # 输入错误返回第一页
    except EmptyPage:  # 如果输入超出范围
        hostserver_objs = paginator.page(paginator.num_pages)  # 一共多少页就返回最后那页面

    return render(request, 'crm/hostserver05.html', {'hostserver_list': hostserver_objs})


@check_permission
def hostserver_detail05(request, hostserver_id):
    # 两种情况 一种是获取客户详细信息 另一种是修改客户详细信息 同过前端传入hostserver_id根据其取值
    hostserver_obj = models.HostServer05.objects.get(id=hostserver_id)
    if request.method == "POST":
        # 根据前端提交过来的值进行验证 request.POST把用户提交的数据传入 需要修改的是instance=hostserver_obj
        form = forms.HostServer05ModelForm(request.POST, instance=hostserver_obj)
        print(request.POST)
        if form.is_valid():
            form.save()
            # 需要通过redirect进行动态跳转
            print('url:', request.path)  # 获取当前页面的url
            a = "/".join(request.path.split("/")[-2])
            b = math.ceil(int(a) / int(count_page))
            print(a)
            print(b)
            # base_url = "/".join(request.path.split("/")[0:-2])  # 以"/"分割取需要字段去除id
            base_url = "/".join(request.path.split("/")[0:-2]) + "/?page=" + "%s" % (b)  # 以"/"分割取需要字段去除id
            print(base_url)
            print('url:', base_url)
            return redirect(base_url)
    else:
        # 将hostserver_obj读到的数据装入form(instance=hostserver_obj)
        form = forms.HostServer05ModelForm(instance=hostserver_obj)
    return render(request, 'crm/hostserver_detail05.html', {'hostserver_form': form})

###################################################################################################################################

#@check_permission
def hostserver06(request):
    hostserver_list = models.HostServer06.objects.all()
    paginator = Paginator(hostserver_list, count_page)
    page = request.GET.get('page')  # 前端请求传入
    try:
        hostserver_objs = paginator.page(page)
    except PageNotAnInteger:  # 如果输入的不是数字的话  等同于第一次打开页面就跳转到第一页面
        hostserver_objs = paginator.page(1)  # 输入错误返回第一页
    except EmptyPage:  # 如果输入超出范围
        hostserver_objs = paginator.page(paginator.num_pages)  # 一共多少页就返回最后那页面

    return render(request, 'crm/hostserver06.html', {'hostserver_list': hostserver_objs})


@check_permission
def hostserver_detail06(request, hostserver_id):
    # 两种情况 一种是获取客户详细信息 另一种是修改客户详细信息 同过前端传入hostserver_id根据其取值
    hostserver_obj = models.HostServer06.objects.get(id=hostserver_id)
    if request.method == "POST":
        # 根据前端提交过来的值进行验证 request.POST把用户提交的数据传入 需要修改的是instance=hostserver_obj
        form = forms.HostServer06ModelForm(request.POST, instance=hostserver_obj)
        print(request.POST)
        if form.is_valid():
            form.save()
            # 需要通过redirect进行动态跳转
            print('url:', request.path)  # 获取当前页面的url
            a = "/".join(request.path.split("/")[-2])
            b = math.ceil(int(a) / int(count_page))
            print(a)
            print(b)
            # base_url = "/".join(request.path.split("/")[0:-2])  # 以"/"分割取需要字段去除id
            base_url = "/".join(request.path.split("/")[0:-2]) + "/?page=" + "%s" % (b)  # 以"/"分割取需要字段去除id
            print(base_url)
            print('url:', base_url)
            return redirect(base_url)
    else:
        # 将hostserver_obj读到的数据装入form(instance=hostserver_obj)
        form = forms.HostServer06ModelForm(instance=hostserver_obj)
    return render(request, 'crm/hostserver_detail06.html', {'hostserver_form': form})

######################################################################################################################################

#@check_permission
def hostserver07(request):
    hostserver_list = models.HostServer07.objects.all()
    paginator = Paginator(hostserver_list, count_page)
    page = request.GET.get('page')  # 前端请求传入
    try:
        hostserver_objs = paginator.page(page)
    except PageNotAnInteger:  # 如果输入的不是数字的话  等同于第一次打开页面就跳转到第一页面
        hostserver_objs = paginator.page(1)  # 输入错误返回第一页
    except EmptyPage:  # 如果输入超出范围
        hostserver_objs = paginator.page(paginator.num_pages)  # 一共多少页就返回最后那页面

    return render(request, 'crm/hostserver07.html', {'hostserver_list': hostserver_objs})


@check_permission
def hostserver_detail07(request, hostserver_id):
    # 两种情况 一种是获取客户详细信息 另一种是修改客户详细信息 同过前端传入hostserver_id根据其取值
    hostserver_obj = models.HostServer07.objects.get(id=hostserver_id)
    if request.method == "POST":
        # 根据前端提交过来的值进行验证 request.POST把用户提交的数据传入 需要修改的是instance=hostserver_obj
        form = forms.HostServer07ModelForm(request.POST, instance=hostserver_obj)
        print(request.POST)
        if form.is_valid():
            form.save()
            # 需要通过redirect进行动态跳转
            print('url:', request.path)  # 获取当前页面的url
            a = "/".join(request.path.split("/")[-2])
            b = math.ceil(int(a) / int(count_page))
            print(a)
            print(b)
            # base_url = "/".join(request.path.split("/")[0:-2])  # 以"/"分割取需要字段去除id
            base_url = "/".join(request.path.split("/")[0:-2]) + "/?page=" + "%s" % (b)  # 以"/"分割取需要字段去除id
            print(base_url)
            print('url:', base_url)
            return redirect(base_url)
    else:
        # 将hostserver_obj读到的数据装入form(instance=hostserver_obj)
        form = forms.HostServer07ModelForm(instance=hostserver_obj)
    return render(request, 'crm/hostserver_detail07.html', {'hostserver_form': form})

########################################################################################################################################

#@check_permission
def hostserver08(request):
    hostserver_list = models.HostServer08.objects.all()
    paginator = Paginator(hostserver_list, count_page)
    page = request.GET.get('page')  # 前端请求传入
    try:
        hostserver_objs = paginator.page(page)
    except PageNotAnInteger:  # 如果输入的不是数字的话  等同于第一次打开页面就跳转到第一页面
        hostserver_objs = paginator.page(1)  # 输入错误返回第一页
    except EmptyPage:  # 如果输入超出范围
        hostserver_objs = paginator.page(paginator.num_pages)  # 一共多少页就返回最后那页面

    return render(request, 'crm/hostserver08.html', {'hostserver_list': hostserver_objs})


@check_permission
def hostserver_detail08(request, hostserver_id):
    # 两种情况 一种是获取客户详细信息 另一种是修改客户详细信息 同过前端传入hostserver_id根据其取值
    hostserver_obj = models.HostServer08.objects.get(id=hostserver_id)
    if request.method == "POST":
        # 根据前端提交过来的值进行验证 request.POST把用户提交的数据传入 需要修改的是instance=hostserver_obj
        form = forms.HostServer08ModelForm(request.POST, instance=hostserver_obj)
        print(request.POST)
        if form.is_valid():
            form.save()
            # 需要通过redirect进行动态跳转
            print('url:', request.path)  # 获取当前页面的url
            a = "/".join(request.path.split("/")[-2])
            b = math.ceil(int(a) / int(count_page))
            print(a)
            print(b)
            # base_url = "/".join(request.path.split("/")[0:-2])  # 以"/"分割取需要字段去除id
            base_url = "/".join(request.path.split("/")[0:-2]) + "/?page=" + "%s" % (b)  # 以"/"分割取需要字段去除id
            print(base_url)
            print('url:', base_url)
            return redirect(base_url)
    else:
        # 将hostserver_obj读到的数据装入form(instance=hostserver_obj)
        form = forms.HostServer08ModelForm(instance=hostserver_obj)
    return render(request, 'crm/hostserver_detail08.html', {'hostserver_form': form})
