#!/usr/bin/python2.7
# -*- coding: utf-8 -*-import sys
###############################################################
#
#                          MAAPI 2.1
#                 Read values by Using linux Commands
#
##############################################################

import sys
import psycopg2
import commands
from MaaPi_Settings import *
import sys

def qa(message):
    try:
        if sys.argv[1]=="-v":
            print message
    except:
        pass

def run():
    try:
        conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(Maapi_dbname,Maapi_user,Maapi_host,Maapi_passwd))
    except:
        print "I am unable to connect to the database"
    else:
        x = conn.cursor()
        x.execute("SELECT id from maapi_bustypes where bus_enabled=True AND bus_type='linuxCommand'")
        bus_id= x.fetchone()[0]

        x.execute("UPDATE maapi_cron SET cron_last_file_exec=now() WHERE cron_file_path ='{0}' and cron_where_exec='{1}'".format(sys.argv[0],Maapi_location))
        conn.commit()

        x.execute("SELECT COUNT(*) FROM maapi_commandline WHERE cmd_enabled=True AND cmd_location='{0}'".format(Maapi_location))
        counter = x.fetchone()

        x.execute("SELECT cmd_update_rom_id FROM maapi_commandline WHERE cmd_enabled=True AND cmd_location='{0}'".format(Maapi_location))
        cmd_id = x.fetchall()

        x.execute("SELECT cmd_command FROM maapi_commandline WHERE cmd_enabled=True AND cmd_location='{0}'".format(Maapi_location))
        cmd_command = x.fetchall()

        for i in xrange(0,counter[0]):
            #get last value from devices table
            x.execute("SELECT dev_bus_type_id FROM devices WHERE dev_id='{0}' ".format(cmd_id[i][0]))
            dev_bus_type_id = x.fetchone()[0]
            if dev_bus_type_id == bus_id:
                x.execute("SELECT dev_value FROM devices WHERE dev_id='{0}' ".format(cmd_id[i][0]))
                old_value = x.fetchone()
                value=commands.getstatusoutput('{}'.format(cmd_command[i][0]))
                #put old value to devices table
                try:
                    x.execute("UPDATE devices SET dev_value_old='{0}' WHERE dev_id='{1}'".format(float(old_value[0]),cmd_id[i][0]))
                    qa("execute")
                except psycopg2.IntegrityError:
                    conn.rollback()
                    qa("rollback - sql error - writeing old value to devices")
                    x.execute("INSERT INTO logs VALUES (default,default,'ERROR' , 'serv Maapi_read_sys_param.py' , 'sql error - writeing old value to devices' , 'IntegrityError')")
                    conn.commit()
                else:
                    conn.commit()
                    qa("commit")


                try:
                    x.execute("SELECT dev_rom_id FROM devices WHERE dev_id='{0}' ".format(cmd_id[i][0]))
                    dev_rom_id = x.fetchone()[0]
                    x.execute("""INSERT INTO maapi_dev_rom_{0}_values VALUES (default,{1},default,{2})""".format(dev_rom_id.replace("-", "_"), cmd_id[i][0],float(value[1])))
                    qa("execute")
                except psycopg2.IntegrityError:
                    conn.rollback()
                    qa("rollback - sql error - writeing value to dev_value")
                    x.execute("INSERT INTO logs VALUES (default,default,'ERROR' , 'serv Maapi_read_sys_param.py' , 'sql error - writeing value to dev_value' , 'IntegrityError')")
                    conn.commit()
                else:
                    conn.commit()
                    qa("commit")


                try:
                    x.execute("UPDATE devices SET dev_value='{0}', dev_last_update=NOW(), dev_read_error='{1}' WHERE dev_id='{2}'".format(float(value[1]),'ok',cmd_id[i][0]))
                    qa("execute")
                except psycopg2.IntegrityError:
                    conn.rollback()
                    qa("rollback - sql error - sql error - writeing new value to devices")
                    x.execute("INSERT INTO logs VALUES (default,default,'ERROR' , 'serv Maapi_read_sys_param.py' , 'sql error - writeing new value devices' , 'IntegrityError')")
                    conn.commit()
                else:
                    conn.commit()
                    qa("commit")


        conn.close()


try:
    if sys.argv[1]=="--help":
        print "MaaPi Senosrs module : Cron Managment\n -v       verbose"
    else:
        run()
except:
    run()
