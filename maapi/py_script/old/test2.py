
    def insert_data(senor_id,value,sensor_type,status):
        try:
            conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(Maapi_dbname,Maapi_user,Maapi_host,Maapi_passwd))
        except:
            print "I am unable to connect to the database"
        else:
            x = conn.cursor()

            """get data from devices where dev_id=senosr_id"""
            x.execute("SELECT dev_value, dev_rom_id, dev_collect_values_to_db FROM devices WHERE dev_id='{0}' and dev_status=True".format(senor_id))
            db_data = x.fetchone()


            x.execute("UPDATE devices SET dev_value_old={0} WHERE dev_id='{1}' and dev_status=True".format(db_data[0],senor_id)
            conn.commit()

            if status:
                """"if stst is true, update actual value, date and stat on devices""""
                x.execute("UPDATE devices SET dev_value={0}, dev_last_update=NOW(),dev_read_error='ok' WHERE dev_id='{1}' and dev_status=True".format(value,senor_id)
                conn.commit()
                """if dev_collect_values_to_db true - enable write to values table"""
                if db_data[2]:
                    x.execute("""INSERT INTO maapi_dev_rom_{0}_values VALUES (default,{1},default,{2})""".format(db_data[1].replace("-", "_"), senor_id,value))
                    conn.commit()
            else:
                x.execute("UPDATE devices SET dev_value={0},dev_read_error='Errorr' WHERE dev_id='{1}' and dev_status=True".format(9999,senor_id)
                conn.commit()
            conn.close()

    def update_cron(file_name):
        try:
            conn = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(Maapi_dbname,Maapi_user,Maapi_host,Maapi_passwd))
        except:
            print "I am unable to connect to the database"
        else:
            x = conn.cursor()""" database - update cron table with date of execution"""
            x.execute("UPDATE maapi_cron SET cron_last_file_exec=NOW() WHERE cron_file_path ='{0}' and cron_where_exec='{1}'".format(file_name,Maapi_location))
            conn.commit()
            conn.close()
