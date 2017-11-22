#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import sys
import psycopg2
import commands
from MaaPi_Settings import *
import sys
from MaaPi_DB_connection_2 import select_table,select_last_nr_of_values



d = select_table("maapi_device_list",None,None,None,None)

for i in d:
    if d[i]["device_name"] == "MoonPhse":
        moonphase_id= d[i]["id"]
s=select_table("devices",None,None,'dev_type_id',moonphase_id)
print s[0]["dev_user_name"]
