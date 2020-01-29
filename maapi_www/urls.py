"""maapi_www URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from maapi.views_Index import MainIndexView, SensorListView , SensorsDetailListView, Pyex
from maapi.views_Dev_Charts import devCharts
from maapi.viewsRest import getFromEsp
from django.http import HttpResponse
from django.contrib.auth import views as auth_views
from django.urls import path

from django.contrib.auth import views as auth_views

urlpatterns = [
   url( r'^login/$',auth_views.LoginView.as_view(template_name="useraccounts/login.html"), name="login"),
]

urlpatterns = [
    
    url(r'^Settings/', admin.site.urls),
    url(r'^login/$',auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    url(r'^logout/$', auth_views.LoginView.as_view(template_name="logout.html"), name="logout"),
    url(r'^$', MainIndexView.as_view(), name="index"),
    url(r'^Devices_info/$', SensorListView.as_view(), name="sensor_list_detail"),
    url(r'^Devices_detail_info$', SensorsDetailListView.as_view(), name='DevicesSettings'),
    url(r'^Charts/Draw=(?P<pk>[a-zA-Z0-9_,.-]+)/Acc=(?P<acc>[0-9]+)/From=(?P<date_from>[a-z0-9 :_-]+)/To=(?P<date_to>[a-z0-9 :_-]+)$', devCharts, name='devCharts'),
    url(r'^postData/SysName=(?P<postsysname>[a-zA-Z0-9_.-]+)/Id=(?P<postid>[0-9]+)/Value=(?P<postvalue>[0-9.0-9]+)/Idx=(?P<postidx>[0-9]+)$', getFromEsp, name='getFromEsp'),
    url(r'^robots.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")),
    path(actionUrl, Pyex),
    ]
