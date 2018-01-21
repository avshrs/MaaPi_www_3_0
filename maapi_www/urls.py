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
from maapi.views_Index import MainIndexView, SensorListView , SensorsDetailListView, twenty
from maapi.views_Dev_Charts import devCharts
from maapi.viewsRest import getFromEsp
from django.http import HttpResponse
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^crazyadmin2/', include('admin_honeypot.urls',namespace='admin_honeypot')),
    url(r'^Settings/', admin.site.urls),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logout.html'}, name='logout'),

    url(r'^$', MainIndexView.as_view(), name="index"),
    url(r'^Devices_info/$', SensorListView.as_view(), name="sensor_list_detail"),
    url(r'^twenty2/$', twenty.as_view(), name="twenty"),
    url(r'^Devices_detail_info$', SensorsDetailListView.as_view(), name='DevicesSettings'),

    #1url(r'^Charts/Draw=(?P<pk>[a-zA-Z0-9_.-]+)-Acc=(?P<acc>[0-9]+)-N=(?P<dn>[0-9]+)-Date=(?P<dv>[h|d|m|y|w])$', devCharts, name='devCharts'),
    #2url(r'^Charts/Draw-(?P<pk>[a-zA-Z0-9_.-]+)-Acc-(?P<acc>[0-9]+)-From-(?P<date_from>[0-9 :_-]+)-To-(?P<date_to>[0-9 :_-]+)$', devCharts, name='devCharts'),
    url(r'^Charts/Draw=(?P<pk>[a-zA-Z0-9_,.-]+)/Acc=(?P<acc>[0-9]+)/From=(?P<date_from>[a-z0-9 :_-]+)/To=(?P<date_to>[a-z0-9 :_-]+)$', devCharts, name='devCharts'),
    url(r'^postData/SysName=(?P<postsysname>[a-zA-Z0-9_.-]+)/Id=(?P<postid>[0-9]+)/Value=(?P<postvalue>[0-9.0-9]+)/Idx=(?P<postidx>[0-9]+)$', getFromEsp, name='getFromEsp'),
    url(r'^robots.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain"))
    ]
