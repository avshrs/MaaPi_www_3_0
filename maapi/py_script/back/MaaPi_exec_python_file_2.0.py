#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import psycopg2
import commands
from MaaPi_Settings import *
import subprocess

def stringToList(self):
    command_list=[]
    command_text=""
    for i in self:
        if i.isspace():
            command_list.append(command_text)
            command_text=""
            continue
        command_text+=i
    command_list.append(command_text)
    return command_list

try:
    conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(Maapi_dbname,Maapi_user,Maapi_host,Maapi_passwd))
except:
    print "I am unable to connect to the database"
else:
    x = conn.cursor()

    x.execute("SELECT COUNT(*) FROM maapi_port_listener WHERE pl_location='{0}'".format(Maapi_location))
    counter = x.fetchone()[0]
    x.execute("UPDATE maapi_cron SET cron_last_file_exec=now() WHERE cron_file_path ='{0}' and cron_where_exec='{1}'".format(sys.argv[0],Maapi_location))
    conn.commit()
    x.execute("SELECT pl_command_start FROM maapi_port_listener WHERE  pl_location='{0}'".format(Maapi_location))
    pl_command_start = x.fetchall()

    x.execute("SELECT id FROM maapi_port_listener WHERE  pl_location='{0}'".format(Maapi_location))
    ps_id = x.fetchall()

    x.execute("SELECT pl_command_stop FROM maapi_port_listener WHERE pl_location='{0}'".format(Maapi_location))
    pl_command_stop = x.fetchall()

    x.execute("SELECT pl_running FROM maapi_port_listener WHERE pl_location='{0}'".format(Maapi_location))
    pl_running = x.fetchall()

    x.execute("SELECT pl_enabled FROM maapi_port_listener WHERE pl_location='{0}'".format(Maapi_location))
    pl_enabled = x.fetchall()


    for i in xrange(counter):
        print i
        print pl_command_start[i][0]
        print pl_running[i][0]
        print pl_command_stop[i][0]
        command_start=stringToList(pl_command_start[i][0])
        command_stop=stringToList(pl_command_stop[i][0])
        if pl_enabled[i][0] is True :
            if pl_running[i][0] is not True :
                print "in if"
                x.execute("UPDATE maapi_port_listener SET pl_running=True WHERE id={0}".format(ps_id[i][0]))
                conn.commit()
                process = subprocess.Popen(command_start)
                print process.pid
        else:
            if pl_running[i][0] is True :
                print "else"
                x.execute("UPDATE maapi_port_listener SET pl_running=False WHERE id={0}".format(ps_id[i][0]))
                conn.commit()
                print "commited"
                process = subprocess.Popen(command_stop)
