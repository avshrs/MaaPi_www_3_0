#!/usr/bin/python2.7
# -*- coding: utf-8 -*-import sys
###############################################################
#
#                          MAAPI 2.0
#                   connection with DB
#
##############################################################


import sys
import psycopg2
import commands
from MaaPi_Settings import *


def select_data(sensor_type):
    try:
        conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(Maapi_dbname,Maapi_user,Maapi_host,Maapi_passwd))
    except:
        print "I am unable to connect to the database"
    else:
        x = conn.cursor()
        """define vars"""
        devices_table_all={}
        devices_id={}
        sensors_table_all={}
        sensor_rows={}
        device_rows={}


        """ get id and name of table """
        x.execute("SELECT id, device_table_name FROM maapi_device_list where device_module_type='{0}'".format(sensor_type))
        maapi_device_list = x.fetchone()

        """ get all from device table """
        x.execute("SELECT * FROM devices ")
        devices_table = x.fetchall()

        """ get all from sensor_type table """
        x.execute("SELECT * FROM {0} ".format(maapi_device_list[1]))
        sensors_type_table = x.fetchall()

        """ get all from sensor_type table """
        x.execute("SELECT column_name FROM information_schema.columns WHERE table_name='{0}' ".format(maapi_device_list[1]))
        sensors_column_names = x.fetchall()

        x.execute("SELECT column_name FROM information_schema.columns WHERE table_name='devices' ")
        devices_column_names = x.fetchall()


        for row_s in sensors_type_table:
            sensor_rows={}
            i=0
            for r_s in row_s:
                sensor_rows[sensors_column_names[i][0]]=r_s
                i+=1
            sensors_table_all[row_s[0]]=sensor_rows


        for row_d in devices_table:
            device_rows={}
            ii=0
            for r_d in row_d:
                device_rows[devices_column_names[ii][0]]=r_d
                ii+=1
            devices_table_all[row_d[0]]=device_rows



        conn.close()
    return  devices_table_all, sensors_table_all, maapi_device_list[0]

def select_single_table_data(table_name):
    try:
        conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(Maapi_dbname,Maapi_user,Maapi_host,Maapi_passwd))
    except:
        print "I am unable to connect to the database"
    else:
        x = conn.cursor()

        x.execute("SELECT * FROM {0}".format(table_name))
        table_all = x.fetchall()

        x.execute("SELECT column_name FROM information_schema.columns WHERE table_name='{0}' ".format(table_name))
        table_column_names = x.fetchall()

        table={}
        for row_s in table_all:
            sensor_rows={}
            i=0
            for r_s in row_s:
                sensor_rows[table_column_names[i][0]]=r_s
                i+=1
            table[row_s[0]]=sensor_rows


        conn.close()
    return  table

def select_last_nr_of_values(table_name,dt_from, dt_to):
    try:
        conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(Maapi_dbname,Maapi_user,Maapi_host,Maapi_passwd))
    except:
        print "I am unable to connect to the database"
    else:
        x = conn.cursor()

        x.execute("SELECT dev_value FROM {0} maapi_dev_rom_{0}_values where dev_timestamp>='{1}' and dev_timestamp<='{2}'".format(table_name.replace("-", "_"),dt_from,dt_to))
        table_all = x.fetchall()

        x.execute("SELECT column_name FROM information_schema.columns WHERE table_name='{0}' ".format(table_name))
        table_column_names = x.fetchall()

        table={}
        for row_s in table_all:
            sensor_rows={}
            i=0
            for r_s in row_s:
                sensor_rows[table_column_names[i][0]]=r_s
                i+=1
            table[row_s[0]]=sensor_rows


        conn.close()
    return  table

def insert_data(senor_id,value,sensor_type,status):
    try:
        conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(Maapi_dbname,Maapi_user,Maapi_host,Maapi_passwd))
    except:
        print "I am unable to connect to the database"
    else:
        x = conn.cursor()

        x.execute("SELECT dev_value, dev_rom_id, dev_collect_values_to_db FROM devices WHERE dev_id='{0}' and dev_status=True".format(senor_id))
        db_data = x.fetchone()
        try:
            x.execute("UPDATE devices SET dev_value_old={0} WHERE dev_id='{1}' and dev_status=True".format(db_data[0],senor_id))
            conn.commit()
        except:
            print "dupa"
        if status:
            """if stst is true, update actual value, date and stat on devices"""
            if value == True:
                x.execute("UPDATE devices SET dev_value={0}, dev_last_update=NOW(),dev_read_error='ok' WHERE dev_id='{1}' and dev_status=True".format(1,senor_id))
                conn.commit()
                if db_data[2]:
                    x.execute("""INSERT INTO maapi_dev_rom_{0}_values VALUES (default,{1},default,{2})""".format(db_data[1].replace("-", "_"), senor_id,1))
                    conn.commit()
                """if dev_collect_values_to_db true - enable write to values table"""
            elif value == False:
                x.execute("UPDATE devices SET dev_value={0}, dev_last_update=NOW(),dev_read_error='ok' WHERE dev_id='{1}' and dev_status=True".format(0,senor_id))
                conn.commit()
                if db_data[2]:
                    x.execute("""INSERT INTO maapi_dev_rom_{0}_values VALUES (default,{1},default,{2})""".format(db_data[1].replace("-", "_"), senor_id,0))
                    conn.commit()
                """if dev_collect_values_to_db true - enable write to values table"""
            else:
                x.execute("UPDATE devices SET dev_value={0}, dev_last_update=NOW(),dev_read_error='ok' WHERE dev_id='{1}' and dev_status=True".format(value,senor_id))
                conn.commit()
                if db_data[2]:
                    x.execute("""INSERT INTO maapi_dev_rom_{0}_values VALUES (default,{1},default,{2})""".format(db_data[1].replace("-", "_"), senor_id,value))
                    conn.commit()

        else:
            x.execute("UPDATE devices SET dev_value={0},dev_read_error='Errorr' WHERE dev_id='{1}' and dev_status=True".format(9999,senor_id))
            conn.commit()
        conn.close()




def update_cron(file_name):
    try:
        conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(Maapi_dbname,Maapi_user,Maapi_host,Maapi_passwd))
    except:
        print "I am unable to connect to the database"
    else:
        x = conn.cursor()
        x.execute("UPDATE maapi_cron SET cron_last_file_exec=NOW() WHERE cron_file_path ='{0}' and cron_where_exec='{1}'".format(file_name,Maapi_location))
        conn.commit()
        conn.close()
