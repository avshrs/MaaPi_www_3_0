from .models import Devices
from django.shortcuts import render
from datetime import datetime, timedelta
# from dateutil.relativedelta import relativedelta
# import calendar
# import json
# from itertools import chain
# from django.db import connection
# import time


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def range_date(range_tf):
    range_name_days = {'now': 0,
                       '-day': 1,
                       '-week': 7,
                       '-2weeks': 14,
                       '-month': 30,
                       '-6month': 180,
                       '-year': 360,
                       }
    range_name_hours = {'-hour': 1,
                        '-3hours': 3,
                        '-6hours': 6,
                        '-12hours': 12,
                        }
    if range_tf in range_name_days:
        return datetime.now().replace(microsecond=0) - timedelta(
            days=range_name_days[range_tf]), range_tf

    elif range_tf in range_name_hours:
        return datetime.now().replace(microsecond=0) - timedelta(
            hours=range_name_hours[range_tf]), range_tf
    else:
        return range_tf, "date"


def devCharts(request, pk, acc, date_from, date_to):
    list_of_devices = Devices.objects.values('dev_id', 'dev_user_name').filter(
        dev_status=True).filter(dev_hidden=False).order_by('dev_user_id')

    groupname = []
    grouplist = []
    dataName = []
    acc2 = 1
    datetime_format = "%Y-%m-%d %H:%M:%S"
    range_from = "date"
    range_to = "now"

    date_from_space, range_from = range_date(date_from)
    date_to_space, range_to = range_date(date_to)

    a = datetime.strptime(str(date_from_space), datetime_format)
    b = datetime.strptime(str(date_to_space), datetime_format)
    delta_date = (b - a).days

    date_to_html = datetime.strptime(str(date_to_space), datetime_format)
    hour_to_html = b.hour
    date_from_html = datetime.strptime(str(date_from_space), datetime_format)
    hour_from_html = a.hour

    inter = Devices.objects.values('dev_id',
                                   'dev_interval',
                                   'dev_interval_unit_id')
    inter_unit = {3: 3600, 2: 60, 1: 1}

    for i in inter:
        if is_number(pk):
            if int(i['dev_id']) == int(pk):
                dev_inter_sec = float(
                    float(i['dev_interval'])*inter_unit[float(
                        i['dev_interval_unit_id'])])

        elif int(i['dev_id']) == int(pk[0]):
            dev_inter_sec = float(
                float(i['dev_interval'])*inter_unit[float(
                    i['dev_interval_unit_id'])])

    if int(acc) == 1:
        if int(delta_date) != 0:
            acc2 = int(int(delta_date) * (60 / (
                dev_inter_sec * dev_inter_sec)) * dev_inter_sec)

    graph_param = {
        'pk': pk,
        'acc': acc2,
        'date_from': date_from_space,
        'date_to': date_to_space,
        'days_delta': delta_date
    }

    if is_number(pk) is True:
        dataName = Devices.objects.values('dev_id', 'dev_user_name',
                                          'dev_value',
                                          'dev_unit_id').filter(dev_id=pk)
        groupname = 'null'
        grouplist = [pk]
    else:
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
            'range_from': range_from,
            'range_to': range_to,
        })
