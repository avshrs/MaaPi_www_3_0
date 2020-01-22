from .models import Devices, Groups, DevValues
from django.shortcuts import render
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
#import calendar
#import json
#from itertools import chain
from django.db import connection
import time


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def devCharts(request, pk, acc, date_from, date_to):
    pk22 = pk
    groupname = []
    grouplist = []
    list_of_devices = Devices.objects.values('dev_id', 'dev_user_name').filter(
        dev_status=True).filter(dev_hidden=False).order_by('dev_user_id')
    dataName = []
    acc2 = 1
    datetime_format = "%Y-%m-%d %H:%M:%S"

    rangee="date"
    range_to="now"
    if date_from == '-day':
        date_from_space = datetime.now().replace(microsecond=0) - timedelta(
            days=1)
        rangee=date_from
    elif date_from == '-6hours':
        date_from_space = datetime.now().replace(microsecond=0) - timedelta(
            hours=6)
        rangee=date_from
    elif date_from == '-hour':
        date_from_space = datetime.now().replace(microsecond=0) - timedelta(
            hours=1)
        rangee=date_from
    elif date_from == '-12hours':
        date_from_space = datetime.now().replace(microsecond=0) - timedelta(
            hours=12)
        rangee=date_from
    elif date_from == '-month':
        date_from_space = datetime.now().replace(microsecond=0) - timedelta(
            days=30)
        rangee=date_from
    elif date_from == '-6month':
        date_from_space = datetime.now().replace(microsecond=0) - timedelta(
            days=180)
        rangee=date_from
    elif date_from == '-week':
        date_from_space = datetime.now().replace(microsecond=0) - timedelta(
            days=7)
        rangee=date_from
    elif date_from == '-2weeks':
        date_from_space = datetime.now().replace(microsecond=0) - timedelta(
            days=14)
        rangee=date_from
    elif date_from == '-year':
        date_from_space = datetime.now().replace(microsecond=0) - timedelta(
            days=365)
        rangee=date_from
    else:
        date_from_space = date_from

    if date_to == 'now':
        date_to_space = datetime.now().replace(microsecond=0)
        hour_to_html = "now"
        range_to = "now"
    elif date_to == '-day':
        date_to_space = datetime.now().replace(microsecond=0) - timedelta(
            days=1)
        range_to=date_to
    elif date_to == '-6hours':
        date_to_space = datetime.now().replace(microsecond=0) - timedelta(
            hours=6)
        range_to=date_to
    elif date_to == '-hour':
        date_to_space = datetime.now().replace(microsecond=0) - timedelta(
            hours=1)
        range_to=date_to
    elif date_to == '-12hours':
        date_to_space = datetime.now().replace(microsecond=0) - timedelta(
            hours=12)
        range_to=date_to
    elif date_to == '-month':
        date_to_space = datetime.now().replace(microsecond=0) - timedelta(
            days=30)
        range_to=date_to
    elif date_to == '-6month':
        date_to_space = datetime.now().replace(microsecond=0) - timedelta(
            days=180)
        range_to=date_to
    elif date_to == '-week':
        date_to_space = datetime.now().replace(microsecond=0) - timedelta(
            days=7)
        range_to=date_to
    elif date_to == '-2weeks':
        date_to_space = datetime.now().replace(microsecond=0) - timedelta(
            days=14)
        range_to=date_to
    elif date_to == '-year':
        date_to_space = datetime.now().replace(microsecond=0) - timedelta(
            days=365)
        range_to=date_to
    else:
        date_to_space = date_to
        #hour_to_html = datetime.strptime(date_to_space,
        #                                 datetime_format).hour

    a = datetime.strptime(str(date_from_space), datetime_format)
    b = datetime.strptime(str(date_to_space), datetime_format)
    delta_date = (b - a).days

    date_to_html = datetime.strptime(str(date_to_space), datetime_format)
    date_from_html = datetime.strptime(str(date_from_space), datetime_format)
    hour_from_html = a.hour
    hour_to_html = b.hour



    inter = Devices.objects.values('dev_id', 'dev_interval',
                                          'dev_interval_unit_id')
    inter_unit = {3: 3600,
                  2: 60,
                  1: 1,
            }

    for i in inter:
        if int(i['dev_id']) == int(pk):
            dev_inter_sec = float(float(i['dev_interval'])*inter_unit[float(i['dev_interval_unit_id'])])
            #print(dev_inter_sec)

    if int(acc) == 1:
        if int(delta_date) != 0:
            acc2 =  int(int(delta_date) * (60 / (dev_inter_sec * dev_inter_sec)) * dev_inter_sec)
            print("accuracy",acc2)   
    
    graph_param = {
        'pk': pk,
        'acc': acc2,
        'date_from': date_from_space,
        'date_to': date_to_space,
        'days_delta':delta_date
    }

    if is_number(pk) == True:
        dataName = Devices.objects.values('dev_id', 'dev_user_name',
                                          'dev_value',
                                          'dev_unit_id').filter(dev_id=pk)
        groupname = 'null'
        #dev_rom_id = Devices.objects.filter(dev_id=pk).values_list(            'dev_rom_id', flat=True)[0]
        grouplist = [pk]
    else:
        ff = []
        groupname = pk
        grouplist = pk.split(",")
    date_time = datetime.now()
    return render(
        request, '1/_Charts.html', {
            'date_to_html': date_to_html,
            'hour_to_html': hour_to_html,
            'date_from_html': date_from_html,
            'hour_from_html': hour_from_html,
            'dataName': dataName,
            'list_of_devices': list_of_devices,
            'chartACC': acc,
            'date_time': date_time,
            'loop': range(30),
            'loop_hour': range(0, 23),
            'grouplist': grouplist,
            'groupname': groupname,
            'graph_param': graph_param,
            'rangee': rangee,
            'range_to':range_to,
        })
