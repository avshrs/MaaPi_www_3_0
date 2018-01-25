#!/usr/bin/python2.7
# -*- coding: utf-8 -*-import sys
###############################################################
#
#                          MAAPI 3.0
#                   connection with DB
#
##############################################################
import psycopg2
from datetime import datetime, timedelta
from MaaPi_Settings import *


class MaaPiDBConnection(object):

    def __init__(self):
        self.filters_ = {}
        self.orders_ = {}
        self.columns_ = {}


    def columns(self, *args):
        if len(args) != 1:
            raise ValueError(
                ".order_by('column name') should only have a column name")
        self.columns_ = args
        return self

    def filters_eq(self, **kwargs):
        self.filters_ = kwargs
        return self

    def order_by(self, *args):
        self.orders_ = args
        return self

    def if_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    def exec_query_select(self, query, name):
        try:
            conn = psycopg2.connect(
                "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(
                    Maapi_dbname, Maapi_user, Maapi_host, Maapi_passwd))
        except:
            raise IOError(
                "Can not open connection with DB {0}".format(Maapi_dbname))
        else:
            table_data_dict = {}
            x = conn.cursor()
            try:
                x.execute(query)
                table_data = x.fetchall()
                x.execute(
                    "SELECT column_name FROM information_schema.columns WHERE table_name='{0}' ".
                    format(name))
                table_names = x.fetchall()
            except (Exception, psycopg2.DatabaseError) as error:
                pass
            else:
                for row_s in range(len(table_data)):
                    sensor_rows = {}
                    i = 0
                    for r_s in table_data[row_s]:
                        sensor_rows[table_names[i][0]] = r_s
                        i += 1
                    table_data_dict[table_data[row_s][0]] = sensor_rows
            conn.close()
        return table_data_dict

    def get_table(self, *args):
        if len(args) != 1:
            raise ValueError(
                ".get_table('table name') should only have a table name")
        if self.columns_:
            c_len = len(self.columns_)
            c_i = 1
            columns = " "
            for c in self.columns_:
                if c_len > 1:
                    columns += "{0}".format(c)
                    if c_i < c_len:
                        columns += ", "
                    c_i += 1
                else:
                    columns += "{0}".format(c)
        else:
            columns = "*"
        query = "SELECT {0} FROM {1} ".format(columns, args[0])

        if self.filters_:
            f_len = len(self.filters_)
            f_i = 1
            query += "WHERE "
            for i in self.filters_:
                if f_i == 1:
                    if self.if_number(self.filters_[i]):
                        query += " {0} = {1}".format(i, self.filters_[i])
                    else:
                        query += " {0} = '{1}'".format(i, self.filters_[i])
                else:
                    query += " and "
                    if self.if_number(self.filters_[i]):
                        query += " {0} = {1}".format(i, self.filters_[i])
                    else:
                        query += " {0} = '{1}'".format(i, self.filters_[i])
                f_i += 1
        if self.orders_:
            try:
                self.orders_[1]
            except:
                query += " ORDER BY {0}".format(self.orders_[0])
            else:
                if self.orders_[1] == "asc" or self.orders_[1] == "ASC" or self.orders_[1] == "desc" or self.orders_[1] == "DESC":
                    query += " ORDER BY {0} {1}".format(self.orders_[0],
                                                        self.orders_[1])
                else:
                    raise ValueError(
                        "order_by Second Value should be empty or ASC or DESC but get: '{0}'".
                        format(self.orders_[1]))
        query += ";"
        data = self.exec_query_select(query, args[0])

        return data

    def select_last_nr_of_values(self, dev_id, range_nr):
        try:
            conn = psycopg2.connect(
                "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(
                    Maapi_dbname, Maapi_user, Maapi_host, Maapi_passwd))
        except:
            print "I am unable to connect to the database"
        else:
            x = conn.cursor()
            try:
                x.execute(
                    "SELECT dev_rom_id FROM devices where dev_id={0}".format(
                        dev_id))
                dev_rom_id = x.fetchone()[0]
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                values_history_error = True
            else:
                date_now_a = datetime.now().replace(second=0, microsecond=0)
                date_now_b = datetime.now().replace(
                    second=0, microsecond=0) - timedelta(minutes=range_nr)
                try:
                    x.execute(
                        """SELECT dev_value, dev_timestamp from maapi_dev_rom_{0}_values where dev_timestamp>='{1}' and dev_timestamp<='{2}' order by dev_timestamp desc""".
                        format(
                            dev_rom_id.replace("-", "_"), date_now_b,
                            date_now_a))
                    values_history_temp = x.fetchall()
                except:
                    values_history_error = True
                for i in range(range_nr):
                    date_now_a = datetime.now().replace(second=0) - timedelta(
                        minutes=i)
                    date_now_b = datetime.now().replace(second=0) - timedelta(
                        minutes=i + 1)
                    if values_history_temp[i][1] >= date_now_b and values_history_temp[i][1] <= date_now_a:
                        values_history[i] = values_history_temp[i][0]
                    else:
                        values_history[i] = None
            conn.close()
        return values_history, values_history_error

    def insert_data(self, senor_id, value, sensor_type, status):
        """
        Update Date of execution in cron table
        log date of last execution
        file_name - whole path with file name e.g. /home/user/file.py

        """
        try:
            conn = psycopg2.connect(
                "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(
                    Maapi_dbname, Maapi_user, Maapi_host, Maapi_passwd))
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        else:
            x = conn.cursor()
            x.execute(
                "SELECT dev_value, dev_rom_id, dev_collect_values_to_db FROM devices WHERE dev_id='{0}' and dev_status=True".
                format(senor_id))
            db_data = x.fetchone()
            try:
                x.execute(
                    "UPDATE devices SET dev_value_old={0} WHERE dev_id='{1}' and dev_status=True".
                    format(db_data[0], senor_id))
                conn.commit()
            except:
                pass
            if status is True:
                """if stst is true, update actual value, date and stat on devices"""
                if value == True:
                    x.execute(
                        "UPDATE devices SET dev_value={0}, dev_last_update=NOW(),dev_read_error='ok' WHERE dev_id='{1}' and dev_status=True".
                        format(1, senor_id))
                    conn.commit()
                    if db_data[2]:
                        x.execute(
                            """INSERT INTO maapi_dev_rom_{0}_values VALUES (default,{1},default,{2})""".
                            format(db_data[1].replace("-", "_"), senor_id, 1))
                        conn.commit()
                    """if dev_collect_values_to_db true - enable write to values table"""
                elif value == False:
                    x.execute(
                        "UPDATE devices SET dev_value={0}, dev_last_update=NOW(),dev_read_error='ok' WHERE dev_id='{1}' and dev_status=True".
                        format(0, senor_id))
                    conn.commit()
                    if db_data[2]:
                        x.execute(
                            """INSERT INTO maapi_dev_rom_{0}_values VALUES (default,{1},default,{2})""".
                            format(db_data[1].replace("-", "_"), senor_id, 0))
                        conn.commit()
                    """if dev_collect_values_to_db true - enable write to values table"""
                else:
                    x.execute(
                        "UPDATE devices SET dev_value={0}, dev_last_update=NOW(),dev_read_error='ok' WHERE dev_id='{1}' and dev_status=True".
                        format(value, senor_id))
                    conn.commit()
                    if db_data[2]:
                        x.execute(
                            """INSERT INTO maapi_dev_rom_{0}_values VALUES (default,{1},default,{2})""".
                            format(db_data[1].replace("-", "_"), senor_id,
                                   value))
                        conn.commit()
            else:
                x.execute(
                    "UPDATE devices SET dev_value={0},dev_read_error='Errorr' WHERE dev_id='{1}' and dev_status=True".
                    format(9999, senor_id))
                conn.commit()
            conn.close()

    def update_cron(self, file_name, time):
        """
        Update Date of execution in cron table
        log date of last execution
        file_name - whole path with file name e.g. /home/user/file.py

        """
        try:
            conn = psycopg2.connect(
                "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(
                    Maapi_dbname, Maapi_user, Maapi_host, Maapi_passwd))
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        else:
            x = conn.cursor()
            x.execute(
                "UPDATE maapi_cron SET cron_last_file_exec=NOW(), cron_time_of_exec={1} WHERE cron_file_path ='{2}' and cron_where_exec='{3}'".
                format(datetime.now(), time, file_name, Maapi_location))
            conn.commit()
            conn.close()
