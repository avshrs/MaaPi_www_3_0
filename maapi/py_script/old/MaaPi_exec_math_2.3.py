#!/usr/bin/python2.7
# -*- coding: utf-8 -*-import sys
###############################################################
#
#                          MAAPI 2.1
#                   Calculate Math Sentens
#
##############################################################


import sys
import psycopg2
import commands
from MaaPi_Settings import *

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
        """ database connection established"""

        """ database - get id of PythonMath bus type"""
        x.execute("SELECT id from maapi_bustypes where bus_enabled=True AND bus_type='PythonMath'")
        bus_id= x.fetchone()[0]

        """ database - get Count of all eneblaed match expressions """
        x.execute("SELECT COUNT(*) FROM maapi_math WHERE math_enabled=True")
        counter = x.fetchone()

        """ database - update cron table with date of execution"""
        x.execute("UPDATE maapi_cron SET cron_last_file_exec=NOW() WHERE cron_file_path ='{0}' and cron_where_exec='{1}'".format(sys.argv[0],Maapi_location))
        conn.commit()

        """ database - get id of 1 sensor"""
        x.execute("SELECT math_data_from_1_id FROM maapi_math WHERE math_enabled=True")
        math_data_from_1_id = x.fetchall()
        """ database - get id of 2 sensor"""
        x.execute("SELECT math_data_from_2_id FROM maapi_math WHERE math_enabled=True")
        math_data_from_2_id = x.fetchall()
        """ database - get id of 3 sensor"""
        x.execute("SELECT math_data_from_3_id FROM maapi_math WHERE math_enabled=True")
        math_data_from_3_id = x.fetchall()
        """ database - get id of 4 sensor"""
        x.execute("SELECT math_data_from_4_id FROM maapi_math WHERE math_enabled=True")
        math_data_from_4_id = x.fetchall()

        """ database - get id updete sensor"""
        x.execute("SELECT math_update_rom_id FROM maapi_math WHERE math_enabled=True")
        update_rom = x.fetchall()

        """ database - get math sentece"""
        x.execute("SELECT math_math FROM maapi_math WHERE math_enabled=True")
        math = x.fetchall()

        """ database - get math sentece"""
        x.execute("SELECT math_exec_if_cond_e FROM maapi_math WHERE math_enabled=True")
        math_exec_if_cond_e = x.fetchall()

        x.execute("SELECT math_exec_cond_id FROM maapi_math WHERE math_enabled=True")
        math_exec_cond_id = x.fetchall()

        x.execute("SELECT math_exec_cond_value_min FROM maapi_math WHERE math_enabled=True")
        math_exec_cond_value_min = x.fetchall()

        x.execute("SELECT math_exec_cond_value_max FROM maapi_math WHERE math_enabled=True")
        math_exec_cond_value_max = x.fetchall()

        x.execute("SELECT math_exec_cond_value_max_e FROM maapi_math WHERE math_enabled=True")
        math_exec_cond_value_max_e = x.fetchall()

        x.execute("SELECT math_exec_cond_value_min_e FROM maapi_math WHERE math_enabled=True")
        math_exec_cond_value_min_e = x.fetchall()

        x.execute("SELECT math_exec_cond_force_value_e FROM maapi_math WHERE math_enabled=True")
        math_exec_cond_force_value_e = x.fetchall()

        x.execute("SELECT math_exec_cond_force_value FROM maapi_math WHERE math_enabled=True")
        math_exec_cond_force_value = x.fetchall()

        def run_math_expressions(ii,force_e,force_v):
            qa('run_math_expressions        -            running')
            x.execute("SELECT dev_bus_type_id FROM devices WHERE dev_id='{0}' and dev_status=True".format(update_rom[ii][0]))
            dev_bus_type_id = x.fetchone()[0]

            """ loop - if dev is PythonMath"""
            if dev_bus_type_id == bus_id:

                """ loop - get actula value form device table for updating sensor"""
                x.execute("SELECT dev_value FROM devices WHERE dev_id='{0}' ".format(update_rom[ii][0]))
                old_value = x.fetchone()[0]

                """ loop - get value of 1 sensor"""
                if math_data_from_1_id[ii][0] is not None:
                    x.execute("SELECT dev_value FROM devices WHERE dev_id='{0}' ".format(math_data_from_1_id[ii][0]))
                    v1 = x.fetchone()[0]
                    V1 = v1
                else:
                    v1='none'
                    V1='none'
                """ loop - get value of 2 sensor"""
                if math_data_from_2_id[ii][0] is not None:
                    x.execute("SELECT dev_value FROM devices WHERE dev_id='{0}' ".format(math_data_from_2_id[ii][0]))
                    v2=x.fetchone()[0]
                    V2=v2
                else:
                    v2='none'
                    V2='none'
                """ loop - get value of 3 sensor"""
                if math_data_from_3_id[ii][0] is not None:
                    x.execute("SELECT dev_value FROM devices WHERE dev_id='{0}' ".format(math_data_from_3_id[ii][0]))
                    v3 = x.fetchone()[0]
                    V3=v3
                else:
                    v3='none'
                    V3='none'
                """ loop - get value of 4 sensor"""
                if math_data_from_4_id[ii][0] is not None:
                    x.execute("SELECT dev_value FROM devices WHERE dev_id='{0}' ".format(math_data_from_4_id[ii][0]))
                    v4=x.fetchone()[0]
                    V4 = v4
                else:
                     v4='none'
                     V4='none'
                """ exec math sentens in eval """
                try:
                    if force_e:
                        qa('run_math_expressions        - forcing value ={0}'.format(force_v))
                        value=force_v
                    else:
                        value=eval(math[ii][0])
                        """ exec - update old value """
                        qa('run_math_expressions        - calc math value ={0}'.format(value))
                    try:
                        x.execute("UPDATE devices SET dev_value_old='{0}' WHERE dev_id='{1}'".format(float(old_value),update_rom[ii][0]))

                    except psycopg2.IntegrityError:
                        conn.rollback()
                        qa("rollback - sql error - writeing old value to devices")
                        x.execute("INSERT INTO logs VALUES (default,default,'ERROR' , 'serv Maapi_read_sys_param.py' , 'Math error - writeing old value to devices' , 'IntegrityError')")
                        conn.commit()
                    else:
                        conn.commit()

                    """ exec - update value """
                    try:
                        x.execute("SELECT dev_rom_id FROM devices WHERE dev_id='{0}' ".format(update_rom[ii][0]))
                        dev_rom_id = x.fetchone()[0]
                        x.execute("""INSERT INTO maapi_dev_rom_{0}_values VALUES (default,{1},default,{2})""".format(dev_rom_id.replace("-", "_"), update_rom[ii][0],float(value)))

                    except psycopg2.IntegrityError:
                        conn.rollback()
                        qa("rollback - sql error - writeing value to dev_value")
                        x.execute("INSERT INTO logs VALUES (default,default,'ERROR' , 'serv Maapi_read_sys_param.py' , 'Math error  - writeing value to dev_value' , 'IntegrityError')")
                        conn.commit()
                    else:
                        conn.commit()

                    """ exec - update date of exec """
                    try:
                        x.execute("UPDATE devices SET dev_value='{0}', dev_last_update=NOW(), dev_read_error='{1}' WHERE dev_id='{2}'".format(float(value),'ok',update_rom[ii][0]))

                    except psycopg2.IntegrityError:
                        conn.rollback()
                        qa("rollback - sql error - sql error - writeing new value to devices")
                        x.execute("INSERT INTO logs VALUES (default,default,'ERROR' , 'serv Maapi_read_sys_param.py' , 'Math error - writeing new value devices' , 'IntegrityError')")
                        conn.commit()
                    else:
                        conn.commit()


                except:

                    x.execute("INSERT INTO logs VALUES (default,default,'ERROR' , 'serv MaaPi_exec_math.py' , 'Math error: {0} |  v1={1}, v2={2}, v4={3}, v4={4}' , 'IntegrityError')".format(math[ii][0],v1,v2,v3,v4))
                    conn.commit()
                else:
                    pass



        for i in xrange(0,counter[0]):
            enable=0
            qa('\ndupa {0}'.format(i))
            if math_exec_if_cond_e[i][0]:
                qa('exec if cond enabled {0}'.format(math_exec_if_cond_e[i][0]))
                if math_exec_cond_id[i][0] is not None:
                    qa('sensor exist {0}'.format(math_exec_cond_id[i][0]))
                    x.execute("SELECT dev_value FROM devices WHERE dev_id='{0}' and dev_status=True".format(math_exec_cond_id[i][0]))
                    dev_value = x.fetchone()[0]
                    qa('sensor value {0}'.format(dev_value))
                    if math_exec_cond_value_min_e[i][0]:
                        qa('math_exec_cond_value_min_e {0}'.format(math_exec_cond_value_min_e[i][0]))
                        if dev_value < math_exec_cond_value_min[i][0]:
                            qa('dev_value={0} < math_exec_cond_value_min={1}  = {2}'.format(dev_value,math_exec_cond_value_min[i][0], dev_value < math_exec_cond_value_min[i][0]))
                            enable=1
                        else:
                            run_math_expressions(i,math_exec_cond_force_value_e[i][0],math_exec_cond_force_value[i][0])
                            qa('dev_value={0} < math_exec_cond_value_min={1}  = {2} -------------------------------force 0 on min--------------------------------'.format(dev_value,math_exec_cond_value_min[i][0], dev_value < math_exec_cond_value_min[i][0]))
                    if math_exec_cond_value_max_e[i][0]:
                        qa('math_exec_cond_value_max_e {0}'.format(math_exec_cond_value_max_e[i][0]))
                        if (dev_value > math_exec_cond_value_max[i][0]):
                            qa('dev_value={0} > math_exec_cond_value_max={1}  = {2}'.format(dev_value,math_exec_cond_value_max[i][0], (dev_value > math_exec_cond_value_max[i][0])))
                            enable=1
                            qa('enable =1 ')
                        else:
                            run_math_expressions(i,math_exec_cond_force_value_e[i][0],math_exec_cond_force_value[i][0])
                            qa('dev_value={0} > math_exec_cond_value_max={1}  = {2} -------------------------------force 0 on max--------------------------------'.format(dev_value,math_exec_cond_value_max[i][0], (dev_value > math_exec_cond_value_max[i][0])))
                if enable==1:
                    run_math_expressions(i,False,0)
            else:
                run_math_expressions(i,False,0)


        conn.close()
try:
    if sys.argv[1]=="--help":
        print "MaaPi Senosrs module : Cron Managment\n -v       verbose"
    else:
        run()
except:
    run()
