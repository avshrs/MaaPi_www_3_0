#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import date
import sys
from astral import *

from MaaPi_DB_connection_2 import MaaPiDBConnection

class MaaPiExecMath_Verbose(object):

    def __init__(self,message):
        try:
            if sys.argv[1]=="-v":
                print(message)
        except:
            pass


class MaaPiMoonPhase_exec(object):
    def phase(self):
        a = Astral()
        location = a['Warsaw']
        timezone = location.timezone
        moon = location.moon_phase(date=datetime.now())
        """

        0 = New moon
        7 = First quarter
        14 = Full moon
        21 = Last quarter

        """
        d = round(float(moon) / 14 * 100,0)+(moon/100)+0.001
        if d > 100:
            moon_phase = (200 - d)
            print "moon_phase={0}".format(moon_phase)
        else: moon_phase = d

        return moon_phase

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
