from .models import Devices, Groups, DevValues
from django.shortcuts import  render
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
import json
from itertools import chain
from django.db import connection
import time

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def devCharts(request,pk,acc,date_from,date_to):
    combined = [] #var with data to graph
    data = []
    dv="d"
    dn=1
    groupname = []
    date_time = datetime.now()
    grouplist = []
    list_of_devices = Devices.objects.all().filter(dev_status = True).filter(dev_hidden = False).order_by('dev_user_id')
    devicesparams = Devices.objects.all().filter(dev_status = True).filter(dev_hidden = False)
    list_of_groups = Groups.objects.values_list('group_id','group_name','group_enabled').order_by('group_user_id').filter(group_enabled=True)
    dataName = []
    acc2 = 1
    vaa = True
    datetime_format = "%Y-%m-%d %H:%M:%S"

    if date_from == '-day':
        date_from_space = datetime.now().replace(microsecond=0) - timedelta(days=1)
    elif date_from == '-hour':
        date_from_space = datetime.now().replace(microsecond=0) - timedelta(hours=1)
    elif date_from == '-month':
        date_from_space = datetime.now().replace(microsecond=0) - timedelta(days=30)
    elif date_from == '-week':
        date_from_space = datetime.now().replace(microsecond=0) - timedelta(days=7)
    elif date_from == '-year':
        date_from_space = datetime.now().replace(microsecond=0) - timedelta(days=365)
    else:
        date_from_space = date_from.encode('ascii')

    if date_to == 'now':
        date_to_space = datetime.now().replace(microsecond=0)
        hour_to_html = "now"
    else:
        date_to_space = date_to.encode('ascii')

        hour_to_html = datetime.strptime(str(date_to_space), datetime_format).hour


    a = datetime.strptime(str(date_from_space), datetime_format)
    b = datetime.strptime(str(date_to_space), datetime_format)
    delta = b - a
    delta_date=delta.days

    date_to_html = datetime.strptime(str(date_to_space), datetime_format)
    date_from_html = datetime.strptime(str(date_from_space), datetime_format)
    hour_from_html = a.hour

    if int(acc) == 1:
        if delta_date != 0:
            acc2 = 2 * delta_date

    if int(acc) > 1:
        if dv == 'h' and int(dn) > 5:
            acc2 = (int(dn)*int(acc))
        elif dv == 'h':
            acc2 = (int(acc))*int(dn)
        elif dv == 'd':
            acc2 = (int(acc))*int(dn)
        elif dv == 'm':
            acc2 = (int(acc))*int(dn)
        elif dv == 'y':
            acc2 = (int(acc))*int(dn)

    avg_per=0
    f_max=0
    f_min=1000000
    f_avg_t=0
    f_avg=0
    dv_dates = {'d':'day', 'h':'hour', 'm':'month', 'y':'year', 'w':'week'}
    devName2 = "dupa"

    data2 = {'pk':pk,'acc':acc,'date_from':date_from,'date_to':date_to}

    ps = []

    if is_number(pk) == True:
        dataName = Devices.objects.filter(dev_id = pk)
        groupname = 'null'
        avg_per=1
        dev_rom_id = Devices.objects.filter(dev_id=pk).values_list('dev_rom_id', flat=True)[0]
        cursor = connection.cursor()
        #cursor.execute("""SELECT  ((seqnum - 1) /{0}) AS id, avg(dev_value) as dev_value, MAX("dev_timestamp") as dev_timestamp FROM ( SELECT  row_number() over (ORDER BY dev_timestamp) AS seqnum, maapi_dev_rom_{1}_values.dev_timestamp, maapi_dev_rom_{1}_values.dev_value FROM maapi_dev_rom_{1}_values  WHERE dev_id={2}  AND dev_timestamp >= '{3}' AND dev_timestamp <= '{4}'  ) maapi_devices_values GROUP BY id ORDER BY id """.format(acc2,dev_rom_id.replace("-","_"),pk,date_from_space,date_to_space))
        #ff = cursor.fetchall()
        cursor.execute("""SELECT  row_number() over (ORDER BY dev_timestamp) as id, dev_value, dev_timestamp from  maapi_dev_rom_{0}_values where dev_timestamp >= '{1}' and dev_timestamp <= '{2}'""".format(dev_rom_id.replace("-","_"),date_from_space,date_to_space))
        dd = cursor.fetchall()
        ff = []
        """ """

        iterr_i=1
        for iterr in dd:
            data_i+=iterr[1]
            if iterr_i is acc2:
                iterr_i=0
                time_i+=iterr[2]
                ff.append([int(calendar.timegm( time_i.timetuple()))*1000, data_i/acc2])
            iterr_i+=1

        """ """

        """for i in dd:
            time_i=0
            data_i=0
            for r in range(acc2):
                if r == 0 :
                    time_i = i[2]
                data_i += i[1]
            ff.append([int(calendar.timegm( time_i.timetuple()))*1000, data_i/acc2])
        """

        grouplist=[pk]
        for f in ff:
            if f_max<=f[1]:
                f_max=f[1]
            if f_min>=f[1]:
                f_min= f[1]
            f_avg_t+= f[1]
        if len(list(ff)) !=0:
            f_avg=f_avg_t/float(len(list(ff)))
        else:
            f_avg=0

        """for f in ff:
            date =0
            value =0
            combined.append([int(calendar.timegm( f[2].timetuple()))*1000,  f[1]])"""
        combined = ff
    else:

        groupname = pk
        ps = pk[1:]

        grouplist = pk.split(",")

    return render(request, '1/_Charts.html', {
                                              'date_to_html': date_to_html,
                                              'hour_to_html':hour_to_html,
                                              'date_from_html': date_from_html,
                                              'hour_from_html':hour_from_html,
                                              'f_min':f_min,
                                              'f_max':f_max,
                                              'f_avg':f_avg,
                                              'avg_per':avg_per,
                                              'dataName':dataName,
                                              'data':json.dumps(combined),
                                              'list_of_groups':list_of_groups,
                                              'list_of_devices':list_of_devices,
                                              'chartPK':pk,
                                              'chartACC':acc ,
                                              'date_time':date_time,
                                              'ps':ps,
                                              'chartDN':dn,
                                              'chartDV':dv,
                                              'loop':range(30),
                                              'loop_hour':range(0,23),
                                              'grouplist':grouplist,
                                              'groupname':groupname,
                                              'devicesparams':devicesparams,
                                              'data2':data2,

                                              })
