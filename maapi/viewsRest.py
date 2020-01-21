#!/usr/bin/python2.7
# -*- coding: utf-8 -*-import sys
###############################################################
#
#                          MAAPI 2.0
#                REST API to get data from devices
#
##############################################################

from maapi.models import Devices, DevValues
from django.shortcuts import  render
from time import mktime
import calendar
from itertools import chain
from datetime import datetime
from django.db import connection


def getFromEsp(request,postsysname,postid,postvalue,postidx):
    if request.method == "POST":
        pass
    if request.method == "GET" :
           #get old value
           old=Devices.objects.filter(dev_id = int(postid)).values_list('dev_value', flat=True)[0]
           #assign in table correct sensor
           devValueUpdate = Devices.objects.get(dev_id = int(postid))
           # update old value
           devValueUpdate.dev_value_old = float(old)
           # update value
           devValueUpdate.dev_value = float(postvalue)
           # update tile of updete value
           devValueUpdate.dev_last_update = datetime.now()
           #update status
           devValueUpdate.dev_read_error="ok"
           #save row
           devValueUpdate.save()
           #get rom id from table where dev_id is
           dev_rom_id = Devices.objects.filter(dev_id=int(postid)).values_list('dev_rom_id', flat=True)[0]
           #cursor to not define in model database
           cursor = connection.cursor()
           #exec query - insert value in table
           cursor.execute("""INSERT INTO maapi_dev_rom_{0}_values VALUES (default,{1},default,{2})""".format(dev_rom_id.replace("-", "_"), int(postid),float(postvalue)))


    return render(request, 'rest.html', {})
