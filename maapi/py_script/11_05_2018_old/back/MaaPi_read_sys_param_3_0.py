#!/usr/bin/python2.7
# -*- coding: utf-8 -*-import sys
###############################################################
#
#                          MAAPI 3_0
#                 Read values by Using linux Commands
#
##############################################################

import sys
import commands
from datetime import datetime
from MaaPi_DB_connection_2 import MaaPiDBConnection
from MaaPi_Settings import Maapi_location

class MaaPiSysParams_Verbose(object):

    def __init__(self,message):
        try:
            if sys.argv[1]=="-v":
                print(message)
        except:
            pass

class MaaPiSysParams_exec(object):
    def __init__(self):
        db_conn = MaaPiDBConnection

        maapi_commandline_table = db_conn.select_table("maapi_commandline",None,None,"cmd_location","SERV")
        #qa(maapi_commandline_table)
        sensor_type="linuxCommand"
        maapi_device_list = db_conn.select_table("maapi_device_list",None,None,None,None)
        qa(maapi_device_list)
        for i in maapi_device_list:
            if maapi_device_list[i]["device_name"] == sensor_type:
                linuxCommand_id = maapi_device_list[i]["id"]
        devices_cmd = db_conn.select_table("devices",None,None,'dev_type_id',linuxCommand_id)

        for cmd in maapi_commandline_table:
            if maapi_commandline_table[cmd]['cmd_update_rom_id']:
                value=commands.getstatusoutput('{}'.format(maapi_commandline_table[cmd]['cmd_command']))
                db_conn.insert_data(maapi_commandline_table[cmd]['cmd_update_rom_id'],value[0],sensor_type,True)

qa=MaaPiSysParams_Verbose
try:
    if sys.argv[1]=="--help":
        print ("MaaPi Senosrs module : Cron Managment\n -v       verbose")
    else:
        qa("try")
        startTime = datetime.now()
        MaaPiSysParams_exec()
        endTime = datetime.now()
        delta = endTime - startTime
        time_s = delta.seconds
        time_ms = delta.microseconds
        d=float(time_ms)/100000
        time = d + float(time_s)
        db_conn = MaaPiDBConnection
        db_conn.update_cron(sys.argv[0],time)

except:
    qa("except")
    startTime = datetime.now()
    MaaPiSysParams_exec()
    endTime = datetime.now()
    delta = endTime - startTime
    time_s = delta.seconds
    time_ms = delta.microseconds
    d=float(time_ms)/100000
    time = d + float(time_s)
    db_conn = MaaPiDBConnection
    db_conn.update_cron(sys.argv[0],time)
