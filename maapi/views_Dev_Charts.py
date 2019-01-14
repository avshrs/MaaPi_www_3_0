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
    groupname = []
    grouplist = []
    list_of_devices = Devices.objects.values('dev_id', 'dev_user_name').filter(
        dev_status=True).filter(dev_hidden=False).order_by('dev_user_id')
    dataName = []
    acc2 = 1
    datetime_format = "%Y-%m-%d %H:%M:%S"


    if date_from == '-day':
        date_from_space = datetime.now().replace(microsecond=0) - timedelta(
            days=1)
    elif date_from == '-6hours':
        date_from_space = datetime.now().replace(microsecond=0) - timedelta(
            hours=6)
    elif date_from == '-hour':
        date_from_space = datetime.now().replace(microsecond=0) - timedelta(
            hours=1)
    elif date_from == '-12hours':
        date_from_space = datetime.now().replace(microsecond=0) - timedelta(
            hours=12)
    elif date_from == '-month':
        date_from_space = datetime.now().replace(microsecond=0) - timedelta(
            days=30)
    elif date_from == '-6month':
        date_from_space = datetime.now().replace(microsecond=0) - timedelta(
            days=180)
    elif date_from == '-week':
        date_from_space = datetime.now().replace(microsecond=0) - timedelta(
            days=7)
    elif date_from == '-2weeks':
        date_from_space = datetime.now().replace(microsecond=0) - timedelta(
            days=14)
    elif date_from == '-year':
        date_from_space = datetime.now().replace(microsecond=0) - timedelta(
            days=365)
    else:
        date_from_space = date_from.encode('ascii')

    if date_to == 'now':
        date_to_space = datetime.now().replace(microsecond=0)
        hour_to_html = "now"
    else:
        date_to_space = date_to.encode('ascii')
        hour_to_html = datetime.strptime(str(date_to_space),
                                         datetime_format).hour

    a = datetime.strptime(str(date_from_space), datetime_format)
    b = datetime.strptime(str(date_to_space), datetime_format)
    delta_date = (b - a).days

    date_to_html = datetime.strptime(str(date_to_space), datetime_format)
    date_from_html = datetime.strptime(str(date_from_space), datetime_format)
    hour_from_html = a.hour

    if int(acc) == 1:
        if delta_date != 0:
            acc2 = 2 * delta_date
    print acc2
    graph_param = {
        'pk': pk,
        'acc': acc2,
        'date_from': date_from_space,
        'date_to': date_to_space
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
        })
