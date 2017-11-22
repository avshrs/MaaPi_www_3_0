#!/usr/bin/python2.7
# -*- coding: utf-8 -*-import sys
###############################################################
#
#                          MAAPI 2.0
#                 Send Mail When Condtions are met
#
##############################################################

#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from MaaPi_Settings import *
import psycopg2
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
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
        qa("I am unable to connect to the database")
    else:
        x = conn.cursor()

        x.execute("SELECT COUNT(*) FROM maapi_mail WHERE mail_enabled=True ")
        counter = x.fetchone()
        x.execute("UPDATE maapi_cron SET cron_last_file_exec=now() WHERE cron_file_path ='{0}' and cron_where_exec='{1}'".format(sys.argv[0],Maapi_location))
        conn.commit()

        x.execute("SELECT mail_data_from_sensor_id FROM maapi_mail WHERE mail_enabled=True")
        mail_data_from_sensor_id = x.fetchall()

        x.execute("SELECT id FROM maapi_mail WHERE mail_enabled=True")
        mail_id = x.fetchall()

        x.execute("SELECT mail_data_id FROM maapi_mail WHERE mail_enabled=True")
        mail_data_id = x.fetchall()

        x.execute("SELECT mail_condition_min_e FROM maapi_mail WHERE mail_enabled=True")
        mail_condition_min_e = x.fetchall()

        x.execute("SELECT mail_condition_min FROM maapi_mail WHERE mail_enabled=True")
        mail_condition_min = x.fetchall()

        x.execute("SELECT mail_condition_max_e FROM maapi_mail WHERE mail_enabled=True")
        mail_condition_max_e = x.fetchall()

        x.execute("SELECT mail_condition_max FROM maapi_mail WHERE mail_enabled=True")
        mail_condition_max = x.fetchall()

        x.execute("SELECT mail_send_to FROM maapi_mail WHERE mail_enabled=True")
        mail_send_to = x.fetchall()

        x.execute("SELECT mail_subject FROM maapi_mail WHERE mail_enabled=True")
        mail_subject = x.fetchall()

        x.execute("SELECT mail_mesge_if_min FROM maapi_mail WHERE mail_enabled=True")
        mail_mesge_if_min = x.fetchall()

        x.execute("SELECT mail_mesge_if_max FROM maapi_mail WHERE mail_enabled=True")
        mail_mesge_if_max = x.fetchall()

        x.execute("SELECT mail_last_sended_at_value_min FROM maapi_mail WHERE mail_enabled=True")
        mail_last_sended_at_value_min = x.fetchall()

        x.execute("SELECT mail_last_sended_at_value_max FROM maapi_mail WHERE mail_enabled=True")
        mail_last_sended_at_value_max = x.fetchall()

        for i in xrange(0,counter[0]):
            x.execute("SELECT ml_user FROM maapi_mailing_list WHERE id={0}".format(mail_data_id[i][0]))
            ml_user = x.fetchone()[0]

            x.execute("SELECT ml_password FROM maapi_mailing_list WHERE id={0}".format(mail_data_id[i][0]))
            ml_password  = x.fetchone()[0]

            x.execute("SELECT ml_smtp FROM maapi_mailing_list WHERE id={0}".format(mail_data_id[i][0]))
            ml_smtp = x.fetchone()[0]

            x.execute("SELECT ml_port FROM maapi_mailing_list WHERE id={0}".format(mail_data_id[i][0]))
            ml_port = x.fetchone()[0]


            x.execute("SELECT dev_value FROM devices WHERE dev_id={0}".format(mail_data_from_sensor_id[i][0]))
            value = x.fetchone()[0]
            qa("for")
            if mail_condition_min_e[i][0]:
                qa("mail_condition_min_e {0}".format(mail_condition_min_e[i][0]))
                if value <= mail_condition_min[i][0]:
                    if mail_last_sended_at_value_min[i][0] <= mail_condition_min[i][0]:
                        pass
                    else:
                        qa("value {0} <= mail_condition_min {1}".format(value, mail_condition_min[i][0]))
                        msg = MIMEMultipart()
                        msg['From'] = ml_user
                        msg['To'] = mail_send_to[i][0]
                        msg['Subject'] = mail_subject[i][0]
                        msg.attach(MIMEText('{0} - value {1}'.format(mail_mesge_if_min[i][0],value)))
                        mailServer = smtplib.SMTP(ml_smtp, ml_port)
                        mailServer.ehlo()
                        mailServer.starttls()
                        mailServer.ehlo()
                        mailServer.login(ml_user, ml_password)
                        mailServer.sendmail(ml_password, mail_send_to[i][0], msg.as_string())
                        mailServer.close()
                        x.execute("UPDATE maapi_mail SET mail_last_sended_at_value_min='{0}' WHERE id='{1}'".format(value,mail_id[i][0]))
                        conn.commit()
                else:
                    x.execute("UPDATE maapi_mail SET mail_last_sended_at_value_min='{0}' WHERE id='{1}'".format(value,mail_id[i][0]))
                    conn.commit()

            if mail_condition_max_e[i][0]:
                qa("mail_condition_max_e {0}".format(mail_condition_max_e[i][0]))
                if value >= mail_condition_max[i][0]:
                    qa("value {0} >= mail_condition_max {1}".format(value, mail_condition_max[i][0]))
                    if mail_last_sended_at_value_max[i][0] >= mail_condition_max[i][0]:
                        pass
                        qa("last {0} >= condition max {1} ".format(value, mail_condition_max[i][0]))
                    else:

                        msg = MIMEMultipart()
                        msg['From'] = ml_user
                        msg['To'] = mail_send_to[i][0]
                        msg['Subject'] = mail_subject[i][0]
                        msg.attach(MIMEText('{0} - value {1}'.format(mail_mesge_if_max[i][0],value)))
                        mailServer = smtplib.SMTP(ml_smtp, ml_port)
                        mailServer.ehlo()
                        mailServer.starttls()
                        mailServer.ehlo()
                        mailServer.login(ml_user, ml_password)
                        mailServer.sendmail(ml_password, mail_send_to[i][0], msg.as_string())
                        mailServer.close()
                        x.execute("UPDATE maapi_mail SET mail_last_sended_at_value_max='{0}' WHERE id='{1}'".format(value,mail_id[i][0]))
                        conn.commit()
                else:
                    x.execute("UPDATE maapi_mail SET mail_last_sended_at_value_max='{0}' WHERE id='{1}'".format(value,mail_id[i][0]))
                    conn.commit()


try:
    if sys.argv[1]=="--help":
        print "MaaPi Senosrs module : Cron Managment\n -v       verbose"
    else:
        run()
except:
    run()
