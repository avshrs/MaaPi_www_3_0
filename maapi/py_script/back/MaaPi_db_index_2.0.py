#!/usr/bin/python2.7
# -*- coding: utf-8 -*-import sys
###############################################################
#
#                          MAAPI 2.0
#                 reindex tabels with data
#
##############################################################


import psycopg2
from MaaPi_Settings import *
import sys
from datetime import datetime


class MaaPiSysParams_Verbose(object):
    def __init__(self,message):
        try:
            if sys.argv[1]=="-v":
                print(message)
        except:
            pass
class __init__(object):
    try:
        conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(Maapi_dbname,Maapi_user,Maapi_host,Maapi_passwd))
    except:
        print "I am unable to connect to the database"
    else:
        qa=MaaPiSysParams_Verbose
        startTime = datetime.now()
        qa("connection to db established")
        #create cursor to database
        x = conn.cursor()
        #update in database date of exec this file
        x.execute("UPDATE maapi_cron SET cron_last_file_exec=now() WHERE cron_file_path ='{0}' and cron_where_exec='{1}'".format(sys.argv[0],Maapi_location))
        conn.commit()
        #get all rom id in database
        x.execute("SELECT dev_rom_id from devices order by dev_id")
        rom_id = x.fetchall()
        #get all dev id from database
        x.execute("SELECT dev_id from devices order by dev_id")
        dev_id = x.fetchall()
        #count devices
        x.execute("SELECT COUNT(*) FROM devices ")
        counter = x.fetchone()


        for i in xrange(0,counter[0]):
            #run query reindex all tabes
            qa("REINDEX TABLE maapi_dev_rom_{0}_values".format(rom_id[i][0].replace("-", "_")))
            x.execute( """ REINDEX TABLE maapi_dev_rom_{0}_values""".format(rom_id[i][0].replace("-", "_")))
            conn.commit()

        qa("Reindex on table maapi_devices_values commited")
        #close connection
        endTime = datetime.now()
        delta = endTime - startTime
        time_s = delta.seconds
        time_ms = delta.microseconds
        d=float(time_ms)/100000
        time = d + float(time_s)
        qa("UPDATE maapi_cron SET cron_last_file_exec=now(), cron_time_of_exec={0}  WHERE cron_file_path ='{1}' and cron_where_exec='{2}'".format(time,sys.argv[0],Maapi_location))
        x.execute("UPDATE maapi_cron SET cron_last_file_exec=now(), cron_time_of_exec={0}  WHERE cron_file_path ='{1}' and cron_where_exec='{2}'".format(time,sys.argv[0],Maapi_location))
        conn.commit()

        conn.close()
