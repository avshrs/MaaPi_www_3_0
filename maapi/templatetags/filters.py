from django import template
from maapi.models import Locations, Units, Groups, Devices, DevValues, MainScreen, BackgroudListModel, BusTypes
from django.db.models import F, Count
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import json
import time
import calendar
import humanize
from django.db import connection
from rdp import rdp
import numpy as np
from simplification.cutil import simplify_coords, simplify_coords_vw, simplify_coords_vwp
register = template.Library()


@register.filter
def choice_list(dictionary, key):
    if dictionary is None:
        return 'null'
    else:
        group_values = Groups.objects.values_list(
            key, flat=True).order_by('id')
        value = group_values[dictionary]
        return value


@register.filter
def split_text(dictionary, key):
    asd = "cout{0}".format(key)
    return asd


@register.filter
def units(dictionary):
    unit = Units.objects.filter(unit_id=dictionary).values_list(
        'unit_sign', flat=True)[0]
    return unit


@register.filter
def avg(dictionary):
    avg = sum(dictionary)
    return avg


@register.filter
def locations(dictionary):
    dev_kind = Locations.objects.filter(location_id=dictionary).values_list(
        'location_name', flat=True)[0]
    return dev_kind


@register.filter
def trigger(dictionary):
    sens = BusTypes.objects.filter(bus_type='GpioSwitch').values_list(
        'id', flat=True)[0]
    dev_kind = Devices.objects.filter(dev_id=dictionary).values_list(
        'dev_type', flat=True)[0]
    if dev_kind == sens:
        state = Devices.objects.filter(dev_id=dictionary).values_list(
            'dev_value', flat=True)[0]
    else:
        state = " "
    return state


@register.filter
def group(dictionary):
    dev_kind = Groups.objects.filter(group_id=dictionary).values_list(
        'group_name', flat=True)[0]
    return dev_kind


@register.filter
def isTrue(dictionary):
    if dictionary is True:
        dev_kind = u'\u2713'
    else:
        dev_kind = u'\u2011'
    return dev_kind


@register.filter
def trend(dictionary):
    value = Devices.objects.filter(dev_id=dictionary).values_list(
        'dev_value', flat=True)[0]
    value_old = Devices.objects.filter(dev_id=dictionary).values_list(
        'dev_value_old', flat=True)[0]
    if value > value_old:
        dev_kind = u'\u2197'
    elif value < value_old:
        dev_kind = u'\u2198'
    elif value == value_old:
        dev_kind = u'\u2192'
    return dev_kind


@register.filter
def unit_by_id(dictionary):
    unit_id = Devices.objects.filter(dev_id=dictionary).values_list(
        'dev_unit', flat=True)[0]
    unit = Units.objects.filter(unit_id=unit_id).values_list(
        'unit_sign', flat=True)[0]
    return unit


@register.filter
def name_by_id(dictionary):
    name = Devices.objects.filter(dev_id=dictionary).values_list(
        'dev_user_name', flat=True)[0]
    return name


@register.filter
def value_by_id(dictionary):
    value = Devices.objects.filter(dev_id=dictionary).values_list(
        'dev_value', flat=True)[0]
    return value


@register.filter
def presure(dictionary):
    press = dictionary / 100
    return press


@register.filter
def adjust(dictionary):
    value = Devices.objects.filter(dev_id=dictionary).values_list(
        'dev_value', flat=True)[0]
    adjust = Devices.objects.filter(dev_id=dictionary).values_list(
        'dev_adjust', flat=True)[0]
    value_finale = value + adjust
    return value_finale


@register.filter
def backgroud_main(dictionary):
    name = MainScreen.objects.filter(pk=1).values_list(
        'main_backgroud', flat=True)[0]
    back_name = BackgroudListModel.objects.filter(pk=name).values_list(
        'bg_name', flat=True)[0]
    return back_name


@register.filter(name='data_chart')
def data_chart(dictionary, key):
    start_graph = datetime.now()
    acc2 = key['acc']
    date_from_space = key['date_from']
    date_to_space = key['date_to']
    pk_d = dictionary
    dev_rom_id = Devices.objects.filter(dev_id=pk_d).values_list(
        'dev_rom_id', flat=True)[0]
    combined = []
    cursor = connection.cursor()
    query = ("SELECT "
             "((seqnum - 1) /{acc2}) AS id, "
             "avg(dev_value) as dev_value, "
             "MAX(dev_timestamp) as dev_timestamp "
             "FROM "
             "( SELECT  row_number() over (ORDER BY dev_timestamp) AS seqnum, "
             "maapi_dev_rom_{rom_id}_values.dev_timestamp, "
             "maapi_dev_rom_{rom_id}_values.dev_value "
             "FROM maapi_dev_rom_{rom_id}_values  "
             "WHERE "
             "dev_id={id} "
             "AND dev_timestamp >= '{date_from_space}' "
             "AND dev_timestamp <= '{date_to_space}' ) "
             "maapi_devices_values "
             "GROUP BY id ORDER BY id ".format(
                acc2=acc2,
                rom_id=dev_rom_id.replace("-", "_"),
                id=pk_d,
                date_from_space=date_from_space,
                date_to_space=date_to_space
                )
             )
    cursor.execute(query)
    ff = cursor.fetchall()
    t_value = []

    if len(list(ff)) <= 0:
        return (0, 0)
    else:
        for f in ff:
            date = int(calendar.timegm((f[2]).timetuple())) * 1000
            value = round(f[1], 2)
            t_value.append(value)
            combined.append([date, value])
        f_max = max(t_value)
        f_min = min(t_value)
        f_avg = sum(t_value) / len(t_value)
        stop_graph = datetime.now()
        start_stop = ((stop_graph - start_graph).microseconds) / 1000
        st = start_stop
        return json.dumps(combined), start_stop, st, f_min, f_max, round(f_avg, 2)


@register.filter(name='data_chart2')
def data_chart2(dictionary, key):
    start_graph = datetime.now()

    acc2 = key['acc']
    date_from_space = key['date_from']
    date_to_space = key['date_to']
    days_delta = key['days_delta']
    pk_d = dictionary
    dev_rom_id = Devices.objects.filter(dev_id=pk_d).values_list(
        'dev_rom_id', flat=True)[0]
    combined = []
    cursor = connection.cursor()



    query = ("SELECT "
            "maapi_dev_rom_{rom_id}_values.dev_timestamp, "
            "maapi_dev_rom_{rom_id}_values.dev_value "
            "FROM maapi_dev_rom_{rom_id}_values  "
            "WHERE "
            "dev_id={id} "
            "AND dev_timestamp >= '{date_from_space}' "
            "AND dev_timestamp <= '{date_to_space}'  ".format(
                acc2 = acc2,
                rom_id = dev_rom_id.replace("-", "_"),
                id = pk_d,
                date_from_space = date_from_space,
                date_to_space = date_to_space
                )
            )
    cursor.execute(query)

    ff = cursor.fetchall()
    f_max = -1000000000000000
    f_min = 100000000000000
    f_avg = 0
    stop_graph = datetime.now()
    start_graph2= datetime.now()
    if len(list(ff)) <= 0:
        return (0, 0)
    else:
        for f in ff:
            date = int(calendar.timegm((f[0]).timetuple())) * 1000
            value = round(f[1], 1)
            if f_max <= value: f_max = value
            if f_min >= value: f_min = value
            f_avg += value
            combined.append([int(date),value])
        stop_graph2 = datetime.now()
        start_stop = ((stop_graph - start_graph).microseconds) / 1000
        st = ((stop_graph2 - start_graph2).microseconds) /1000
        fff= simplify_coords(combined, 0.1)
        print(fff)
        return json.dumps(fff), start_stop, st, f_min, f_max, round(
                f_avg / len(list(ff)), 2)





@register.filter(name='chart_data')
def chart_data(dictionary):
    data = DevValues.objects.raw(
        "SELECT  ROW_NUMBER() OVER() as id, dev_value, dev_timestamp  FROM (SELECT *, ROW_NUMBER() OVER() as row from maapi_devices_values where dev_id={0} and dev_timestamp > now() - interval '12 hours'  ORDER BY dev_timestamp )as foo where mod(row,1)=0 ".
        format(dictionary))
    return data
