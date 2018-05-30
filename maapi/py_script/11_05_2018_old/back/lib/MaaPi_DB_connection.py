#!/usr/bin/python2.7
# -*- coding: utf-8 -*-import sys
###############################################################
#
#                          MAAPI 3.1
#                   connection with DB
#
##############################################################
import psycopg2
from datetime import datetime, timedelta
from MaaPi_Settings import *

class MaaPiDBConnection(object):

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

    def table(self, *args):
        if len(args) != 1:
            raise ValueError(
                ".get_table('table name') should only have a table name")
        self.table_ = args[0]
        return self

    def get(self):
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
        query = "SELECT {0} FROM {1} ".format(columns, self.table_)

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
        data = self.exec_query_select(query, self.table_)

        return data

    def __init__(self):
        self.filters_ = {}
        self.orders_ = {}
        self.columns_ = {}
        self.table_ = {}

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
