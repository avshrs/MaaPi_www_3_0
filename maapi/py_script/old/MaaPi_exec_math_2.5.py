#!/usr/bin/python2.7
# -*- coding: utf-8 -*-import sys
###############################################################
#
#                          MAAPI 2.5
#                   Calculate Math Sentens
#
##############################################################
import sys
import commands
from MaaPi_Settings import *
from MaaPi_DB_connection_2 import select_table, insert_data, update_cron

def qa(message):
    try:
        if sys.argv[1]=="-v":
            print message
    except:
        pass

def run():
        device_type='PythonMath'
        math_table =select_table("maapi_math","id","asc","math_enabled",True)
        d = select_table("maapi_device_list",None,None,None,None)
        maapi_math_id=0
        for i in d:
            if d[i]["device_name"] == 'MathExpr':  # errorrrr
                maapi_math_id= d[i]["id"]
                print maapi_math_id
        device_table=select_table("devices",None,None,None, None)


        update_cron(sys.argv[0])
        def run_math_expressions(math2,force_e,force_v):
            qa('run_math_expressions        -            running')
            print "duP"
            if device_table[int(math_table[math2]["math_update_rom_id"])]["dev_type_id"] == maapi_math_id:
                old_value = device_table[int(math_table[math2]["math_update_rom_id"])] ["dev_value"]

                if math_table[math2]["math_data_from_1_id"] is not None:
                    v1 =  device_table[math_table[math2]["math_data_from_1_id"]]["dev_value"]
                    V1 = v1
                else:
                    v1='none'
                    V1='none'

                if math_table[math2]["math_data_from_2_id"] is not None:
                    v2 =  device_table[math_table[math2]["math_data_from_2_id"]]["dev_value"]
                    V2 = v2
                else:
                    v2='none'
                    V2='none'

                if math_table[math2]["math_data_from_3_id"] is not None:
                    v3 =  device_table[math_table[math2]["math_data_from_3_id"]]["dev_value"]
                    V3 = v3
                else:
                    v3='none'
                    V3='none'

                if math_table[math2]["math_data_from_4_id"] is not None:
                    v4 =  device_table[math_table[math2]["math_data_from_4_id"]]["dev_value"]
                    V4 = v4
                else:
                    v4='none'
                    V4='none'

                if force_e:
                    value=force_v
                else:
                    value=eval(math_table[math2]["math_math"])

                insert_data(math_table[math2]["math_update_rom_id"],value,device_type,True)
                qa ( "inserting data")
        for math in math_table:
            enable=0
            qa('\nmath reg {0}'.format(math))
            if math_table[math]["math_enabled"]:
                if math_table[math]["math_exec_if_cond_e"]:
                    qa('exec if cond enabled {0}'.format(math_table[math]["math_exec_if_cond_e"]))
                    if math_table[math]["math_exec_cond_id"] is not None:
                        qa('sensor exist {0}'.format(math_table[math]["math_exec_cond_id"]))
                        dev_value = device_table[math_table[math]["math_exec_cond_id"]]["dev_value"]

                        qa('sensor value {0}'.format(dev_value))
                        if math_table[math]["math_exec_cond_value_min_e"]:
                            qa('math_exec_cond_value_min_e {0}'.format(math_table[math]["math_exec_cond_value_min_e"]))
                            if dev_value < math_table[math]["math_exec_cond_value_min"]:
                                qa('dev_value={0} < math_exec_cond_value_min={1}  = {2}'.format(dev_value,math_table[math]["math_exec_cond_value_min"], dev_value < math_table[math]["math_exec_cond_value_min"]))
                                enable=1
                            else:
                                run_math_expressions(math,math_table[math]["math_exec_cond_force_value_e"],math_table[math]["math_exec_cond_force_value"])
                                qa('dev_value={0} < math_exec_cond_value_min={1}  = {2} -------------------------------force 0 on min--------------------------------'.format(dev_value,math_table[math]["math_exec_cond_value_min"], dev_value < math_table[math]["math_exec_cond_value_min"]))
                        if math_table[math]["math_exec_cond_value_max_e"]:
                            qa('math_exec_cond_value_max_e {0}'.format(math_table[math]["math_exec_cond_value_max_e"]))
                            if (dev_value > math_table[math]["math_exec_cond_value_max"]):
                                qa('dev_value={0} > math_exec_cond_value_max={1}  = {2}'.format(dev_value,math_table[math]["math_exec_cond_value_max"], (dev_value > math_table[math]["math_exec_cond_value_max"])))
                                enable=1
                                qa('enable =1 ')
                            else:
                                run_math_expressions(math,math_table[math]["math_exec_cond_force_value_e"],math_table[math]["math_exec_cond_force_value"])
                                qa('dev_value={0} > math_exec_cond_value_max={1}  = {2} -------------------------------force 0 on max--------------------------------'.format(dev_value,math_table[math]["math_exec_cond_value_max"], (dev_value > math_table[math]["math_exec_cond_value_max"])))
                    if enable==1:
                        run_math_expressions(math,False,0)
                else:
                    run_math_expressions(math,False,0)
try:
    if sys.argv[1]=="--help":
        print "MaaPi Senosrs module : Cron Managment\n -v       verbose"
    else:
        run()
except:
    run()
