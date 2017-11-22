#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import sys
from MaaPi_DB_connection_2 import MaaPiDBConnection

class MaaPiExecMath_Verbose(object):

    def __init__(self,message):
        try:
            if sys.argv[1]=="-v":
                print(message)
        except:
            pass


class MaaPiMoonPhase_exec(object):

    def moon_phase(self,month, day, year):
        ages = [18, 0, 11, 22, 3, 14, 25, 6, 17, 28, 9, 20, 1, 12, 23, 4, 15, 26, 7]
        offsets = [-1, 1, 0, 1, 2, 3, 4, 5, 7, 7, 9, 9]
        if day == 31:
            day = 1

        days_into_phase = ((ages[(year + 1) % 19] +
                            ((day + offsets[month-1]) % 30) +
                            (year < 1900)) % 30)
        light = int(2 * days_into_phase * 100/29)

        if light > 100:
            light = light - 200;

        return light

    def phase(self,year=None, month=None, day=None):
        d=datetime.now()
        hour_v = d.hour
        hour=0.04166666 * hour_v
        month = d.month
        day = d.day + hour
        year = d.year
        light = self.moon_phase(month, day, year)
        return light

    def __init__(self):
        db_con = MaaPiDBConnection()
        

        sensor_type="MoonPhse"
        maapi_device_list = db_con.select_table("maapi_device_list",None,None,None,None)
        for i in maapi_device_list:
            if maapi_device_list[i]["device_name"] == "MoonPhse":
                moonphase_id = maapi_device_list[i]["id"]
        MoonPhse_dev = db_con.select_table("devices",None,None,'dev_type_id',moonphase_id)
        dev_id = 0
        for x in MoonPhse_dev:
            dev_id=MoonPhse_dev[x]["dev_id"]
            db_con.insert_data(dev_id,self.phase(),sensor_type,True)


try:
    if sys.argv[1]=="--help":
        print("MaaPi Senosrs module : Cron Managment\n -v       verbose")
    else:
        startTime = datetime.now()
        MaaPiMoonPhase_exec()
        endTime = datetime.now()
        delta = endTime - startTime
        time_s = delta.seconds
        time_ms = delta.microseconds
        d=float(time_ms)/100000
        time = d + float(time_s)
        db_conn = MaaPiDBConnection
        db_conn.update_cron(sys.argv[0],time)
except:
    startTime = datetime.now()
    MaaPiMoonPhase_exec()
    endTime = datetime.now()
    delta = endTime - startTime
    time_s = delta.seconds
    time_ms = delta.microseconds
    d=float(time_ms)/100000
    time = d + float(time_s)
    db_conn = MaaPiDBConnection
    db_conn.update_cron(sys.argv[0],time)
