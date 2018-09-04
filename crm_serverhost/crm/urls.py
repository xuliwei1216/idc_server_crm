from django.conf.urls import url
from crm import views
urlpatterns = [
    url(r'^$', views.dashboard ),
    url(r'^hostservers/$', views.hostserver,name="hostserver_list" ),
    url(r'^hostservers01/$', views.hostserver01,name="hostserver_list" ),
    url(r'^hostservers02/$', views.hostserver02,name="hostserver_list" ),
    url(r'^hostservers03/$', views.hostserver03,name="hostserver_list" ),
    url(r'^hostservers04/$', views.hostserver04,name="hostserver_list" ),
    url(r'^hostservers05/$', views.hostserver05,name="hostserver_list" ),
    url(r'^hostservers06/$', views.hostserver06,name="hostserver_list" ),
    url(r'^hostservers07/$', views.hostserver07,name="hostserver_list" ),
    url(r'^hostservers08/$', views.hostserver08,name="hostserver_list" ),
    url(r'^hostservers/(\d+)/$', views.hostserver_detail,name="hostserver_detail" ), #别名name
    url(r'^hostservers01/(\d+)/$', views.hostserver_detail01,name="hostserver_detail01" ),
    url(r'^hostservers02/(\d+)/$', views.hostserver_detail02,name="hostserver_detail02" ),
    url(r'^hostservers03/(\d+)/$', views.hostserver_detail03,name="hostserver_detail03" ),
    url(r'^hostservers04/(\d+)/$', views.hostserver_detail04,name="hostserver_detail04" ),
    url(r'^hostservers05/(\d+)/$', views.hostserver_detail05,name="hostserver_detail05" ),
    url(r'^hostservers06/(\d+)/$', views.hostserver_detail06,name="hostserver_detail06" ),
    url(r'^hostservers07/(\d+)/$', views.hostserver_detail07,name="hostserver_detail07" ),
    url(r'^hostservers08/(\d+)/$', views.hostserver_detail08,name="hostserver_detail08" ),
]
