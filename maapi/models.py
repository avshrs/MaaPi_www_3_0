# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.db import models
import commands
import sys
import os
from django.db import connection, transaction


class ScanedOneWireListModel(models.Model):
    device_id                   = models.CharField          (blank=False, null=False,max_length=255, verbose_name="Device Id")
    device_name                 = models.CharField          (blank=False, null=False,max_length=255, verbose_name="Devicename")
    device_description          = models.CharField          (blank=False, null=False,max_length=255, verbose_name="Device Description")
    def __unicode__(self):
        return u'%s' % self.device_name
    class Meta:
        managed = True
        db_table = 'maapi_scaned_one_wire_list'
        verbose_name_plural = "Settings - List - Scaned OneWire bus sensors"


class MaapiFuturesModel(models.Model):
    f_name                  = models.CharField          (blank=False, null=False,max_length=255, verbose_name="Short Descript")
    f_descript              = models.CharField          (blank=False, null=False,max_length=255, verbose_name="Description")
    f_done                  = models.NullBooleanField   (blank=False, null=False, default=False, verbose_name="Done")
    f_added                 = models.DateTimeField      (blank=True, null=True, verbose_name="Topic Added")
    f_created               = models.DateTimeField      (blank=True, null=True, verbose_name="Futures done")
    def __unicode__(self):
        return u'%s' % self.f_name
    class Meta:
        managed = True
        db_table = 'maapi_futures'
        verbose_name_plural = "MaaPi projects futures proposal list"


class CronModel(models.Model):
    CRON_MIN = [ (i, i) for i in xrange(1,60) ]
    CRON_HOUR = [ (i, i) for i in xrange(1,24) ]
    CRON_DAYM = [ (i, i) for i in xrange(1,31) ]
    CRON_DAYW = [ (1, "Monday"),(2, "Tuesday"),(3, "Wednesday"),(4, "Thursday"),(5, "Friday"),(6, "Saturday"),(7, "Sunday")]
    CRON_CHOISE = [(1,"On"), (2, "Every")]
    cron_minute_id          = models.IntegerField     (blank=False, null=False, choices=CRON_MIN,       default=1,  verbose_name="Minute")
    cron_minute_on_every_id = models.IntegerField     (blank=False, null=False, choices=CRON_CHOISE,    default=2,  verbose_name="On or Every Minute")
    cron_hour_id            = models.IntegerField     (blank=False, null=False, choices=CRON_HOUR,      default=1,  verbose_name="Hour")
    cron_hour_on_every_id   = models.IntegerField     (blank=False, null=False, choices=CRON_CHOISE,    default=2,  verbose_name="On or Every Hour")
    cron_day_id             = models.IntegerField     (blank=False, null=False, choices=CRON_DAYM,      default=1,  verbose_name="day")
    cron_day_on_every_id    = models.IntegerField     (blank=False, null=False, choices=CRON_CHOISE,    default=2,  verbose_name="On or Every day")

    cron_last_exec_date     = models.DateTimeField      (blank=True, null=True, verbose_name="Date of last update in crontab")
    cron_last_file_exec     = models.DateTimeField      (blank=True, null=True, verbose_name="Date of last file exec")
    cron_interpreter        = models.CharField          (blank=False, null=False,max_length=255, default="e.g. python2.7", verbose_name="Interpreter")
    cron_file_path          = models.CharField          (blank=False, null=False,max_length=255, default="e.g. /home/user/bin/script.py", verbose_name="Path")
    cron_comment            = models.CharField          (blank=False, null=False,max_length=255, verbose_name="Full file name")
    cron_where_exec         = models.CharField          (blank=False, null=False,max_length=255, verbose_name="Location", help_text="On Which machine i have to run this command?")
    cron_enabled            = models.NullBooleanField   (blank=False, null=False, default=False, verbose_name="Enabled")
    cron_time_of_exec       = models.FloatField         (blank=False, null=False, verbose_name="Time Of Execute")
    class Meta:
        managed = True
        db_table = 'maapi_cron'
        verbose_name_plural = "Settings - Linux Cron Table"


class PortListenerModel(models.Model):
    pl_id                   = models.IntegerField       (blank=False, null=False, verbose_name="ID")
    pl_name                 = models.CharField          (blank=False, null=False, max_length=160, verbose_name="Name")
    pl_timestamp            = models.DateTimeField      (blank=True, null=True, verbose_name="Last modified")
    pl_command_start        = models.CharField          (blank=False, null=False, max_length=255, verbose_name="Start Com.")
    pl_command_stop         = models.CharField          (blank=False, null=False, max_length=255, verbose_name="Stop Com.")
    pl_running              = models.NullBooleanField   (blank=False, null=False, default=False, verbose_name="Is Running?")
    pl_enabled              = models.NullBooleanField   (blank=False, null=False, default=False, verbose_name="Enabled")
    pl_location             = models.CharField          (blank=False, null=False, max_length=160)
#    pl_pid              = models.IntegerField       (blank=False, null=False, verbose_name="running")
    def __unicode__(self):
        return u'%s' % self.pl_name
    class Meta:
        managed = False
        db_table = 'maapi_port_listener'
        verbose_name_plural = "Exec - Rest listener"

class MachineLocation(models.Model):
    id                              = models.AutoField        (primary_key=True)
    ml_name                         = models.CharField        (unique=True, max_length=100,null=False,blank=False, verbose_name="Name")
    ml_description                  = models.CharField        (unique=True, max_length=255,null=False,blank=False, verbose_name="Description")
    ml_location                     = models.CharField        (unique=True, max_length=100,null=False,blank=False, verbose_name="Board location")
    ml_enabled                      = models.NullBooleanField (blank=False, null=False, default=False, verbose_name="Enabled")

    def __unicode__(self):
        return u'%s' % self.ml_location
    class Meta:
        managed = False
        db_table = 'maapi_machine_locations'
        verbose_name_plural = "Settings - List - Board location"

class SensorsList(models.Model):

    device_name                 = models.CharField          (unique=True, max_length=60)
    device_desctiption          = models.CharField          (max_length=255)
    device_lib_name             = models.CharField          (max_length=255)
    device_location             = models.ForeignKey         (MachineLocation, on_delete=models.DO_NOTHING, blank=False, null=False, related_name="Machine_Location", verbose_name="Board Location")
    device_enabled              = models.NullBooleanField   (blank=False, null=False, default=False)

    def __unicode__(self):
        return u'%s' % self.device_name
    class Meta:
        managed = False
        db_table = 'maapi_device_list'
        verbose_name_plural = "Settings - Device Library"


class DevValues(models.Model):
    dev_id                  = models.IntegerField       (blank=False, null=False, verbose_name="ID")
    dev_timestamp           = models.DateTimeField      (blank=True, null=True)
    dev_value               = models.FloatField()
    class Meta:
        managed = False
        db_table = 'maapi_devices_values'
        verbose_name_plural = "Table with all sensors values"


class Groups(models.Model):
    group_id                = models.AutoField          (primary_key=True)
    group_user_id           = models.IntegerField       (unique=True,blank=False, null=False, verbose_name="id")
    group_name              = models.CharField          (unique=True, max_length=30, verbose_name="Name")
    group_enabled           = models.NullBooleanField   (blank=False, null=False, default=False, verbose_name="Enabled")
    def __unicode__(self):
        return u'%s' % self.group_name
    class Meta:
        managed = False
        db_table = 'maapi_groups'
        verbose_name_plural = "Settings - List - Sensors Groups"


class Units(models.Model):
    unit_id                 = models.AutoField          (primary_key=True)
    unit_user_id            = models.IntegerField       (unique=True, verbose_name="id")
    unit_name               = models.CharField          (unique=True, max_length=30, verbose_name="Full Name")
    unit_sign               = models.CharField          (unique=False, max_length=30, verbose_name="Sign")
    unit_enabled            = models.NullBooleanField   (blank=False, null=False, default=False, verbose_name="Enabled")
    def __unicode__(self):
        return u'%s' % self.unit_name
    class Meta:
        managed = False
        db_table = 'maapi_units'
        verbose_name_plural = "Settings - List - Sensors Units"


class Locations(models.Model):
    location_id             = models.AutoField          (primary_key=True)
    location_user_id        = models.IntegerField       (unique=True, verbose_name="id")
    location_name           = models.CharField          (unique=True, max_length=30, verbose_name="Name")
    location_enabled        = models.NullBooleanField   (blank=False, null=False, default=False, verbose_name="Enabled")
    def __unicode__(self):
        return u'%s' % self.location_name
    class Meta:
        managed = False
        db_table = 'maapi_locations'
        verbose_name_plural = "Settings - List - Sensors Locations"


class BusTypes(models.Model):
    id                      = models.AutoField        (primary_key=True)
    bus_name                = models.CharField        (unique=True, max_length=30,null=False,blank=False, verbose_name="Name")
    bus_type                = models.CharField        (unique=True, max_length=30,null=False,blank=False, verbose_name="Bus Type")
    bus_description         = models.CharField        (unique=True, max_length=30,null=False,blank=False, verbose_name="Description")
    bus_lib_name            = models.CharField        (unique=True, max_length=30,null=False,blank=False, verbose_name="Lib file name")
    bus_lib_name_class_name = models.CharField        (unique=True, max_length=30,null=False,blank=False, verbose_name="Class name")
    bus_enabled             = models.NullBooleanField (blank=False, null=False, default=False, verbose_name="Enabled")
    def __unicode__(self):
        return u'%s' % self.bus_type
    class Meta:
        managed = False
        db_table = 'maapi_bustypes'
        verbose_name_plural = "Settings - List - Bus Types"

class Tags(models.Model):
    id                      = models.AutoField        (primary_key=True)
    tag_short               = models.CharField        ( max_length=5,null=False,blank=False, verbose_name="Tag 5 leters")
    tag_long                = models.CharField        ( max_length=30,null=False,blank=False, verbose_name="tag long")
    tag_description          = models.CharField        ( max_length=60, verbose_name="Description")
    def __unicode__(self):
        return u'%s' % self.tag_short
    class Meta:
        managed = False
        db_table = 'maapi_tags'
        verbose_name_plural = "Settings - List - Tags Names"


class Devices(models.Model):
    TYPE_CHOISE = [('1',"Real"), ('2', "Virtual")]
    INTERVAL_UNIT_CHOISE = [(1,"Seconds"), (2, "Minutes"), (3, "Hours")]
    dev_id                              = models.AutoField        (primary_key=True,  null=False,blank=False , verbose_name="DB id")
    dev_rom_id                          = models.CharField        (unique=True, max_length=30,null=False ,blank=False , verbose_name="ROM id")
    dev_time_stamp                      = models.DateTimeField    (null=False, blank=False , verbose_name="Create date")
    dev_user_id                         = models.IntegerField     (default=9999, name="dev_user_id",null=False,blank=False , verbose_name="Id")
    dev_tag_name                        = models.ForeignKey       (Tags, max_length=30, verbose_name="User TAG")
    dev_user_name                       = models.CharField        (max_length=30, default="Name",null=False,blank=False, verbose_name="User Name")
    dev_user_describe                   = models.CharField        (blank=False, null=False,max_length=60 ,verbose_name="Description")
    dev_location                        = models.ForeignKey       (Locations, on_delete=models.DO_NOTHING, related_name="dev_location", blank=False, null=False, verbose_name="Location")
    dev_bus_type                        = models.ForeignKey       (BusTypes, on_delete=models.DO_NOTHING,  blank=False, null=False, verbose_name="Bus Type")
    dev_type                            = models.ForeignKey       (SensorsList, on_delete=models.DO_NOTHING, blank=False, null=False, verbose_name="Sensor Type")
    dev_unit                            = models.ForeignKey       (Units, on_delete=models.DO_NOTHING, related_name="dev_unit", verbose_name="Unit")
    dev_gpio_pin                        = models.IntegerField     (blank=False, null=False, default=0, verbose_name="Gpio Pin")
    dev_interval                        = models.IntegerField     (blank=False, null=False, default=1,  verbose_name="Read Interval")
    dev_interval_unit_id                = models.IntegerField   (max_length=30,  choices=INTERVAL_UNIT_CHOISE, null=False, blank=False, verbose_name="Unit chose")
    dev_value                           = models.FloatField       (blank=True, null=True, default=0, verbose_name="Value")
    dev_adjust                          = models.IntegerField     (blank=False, null=False, default=0, verbose_name="Value - Adjust")
    dev_value_old                       = models.FloatField       (blank=True, null=True,verbose_name="Value - Old")
    dev_last_update                     = models.DateTimeField    (blank=True, null=True,verbose_name="Last Update")
    dev_read_error                      = models.CharField        (blank=True, null=True,max_length=30, default="n/a", verbose_name="Sensor Status")
    dev_main_group                      = models.ForeignKey       (Groups, on_delete=models.DO_NOTHING, related_name="dev_main_group",blank=False, null=False,  verbose_name="Group Main")
    dev_sec_group                       = models.ForeignKey       (Groups, on_delete=models.DO_NOTHING, related_name="dev_sec_group", blank=False, null=False, verbose_name="Group Second")
    dev_third_group                     = models.ForeignKey       (Groups, on_delete=models.DO_NOTHING, related_name="dev_third_group", blank=False, null=False, verbose_name="Group Third")
    dev_status                          = models.NullBooleanField (blank=False, null=False ,default=False, verbose_name="Enabled")
    dev_hidden                          = models.NullBooleanField (blank=False, null=False ,default=False , verbose_name="Hide")
    dev_machine_location                = models.ForeignKey       (MachineLocation, on_delete=models.DO_NOTHING, blank=False, null=False, related_name="Machine_Location", verbose_name="Board Location")
    dev_sensor_type                     = models.CharField        (max_length=30, choices=TYPE_CHOISE, null=False, blank=False, verbose_name="Sensor type")
    dev_collect_values_to_db            = models.NullBooleanField (blank=False, null=False ,default=True, verbose_name="Collect to database")
    dev_collect_values_if_cond_e        = models.NullBooleanField (blank=False, null=False ,default=False, verbose_name="Collect condition")
    dev_collect_values_if_cond_min_e    = models.NullBooleanField (blank=False, null=False ,default=False, verbose_name="Enabled min")
    dev_collect_values_if_cond_max_e    = models.NullBooleanField (blank=False, null=False ,default=False, verbose_name="Enabled max")
    dev_collect_values_if_cond_max      = models.FloatField       (blank=True, null=True,default=0,verbose_name="value > X")
    dev_collect_values_if_cond_min      = models.FloatField       (blank=True, null=True,default=0,verbose_name="value < X")
    dev_collect_values_if_cond_from_dev_e = models.NullBooleanField (blank=False, null=False ,default=False, verbose_name="Enable refered sensor")
    dev_collect_values_if_cond_from_dev   = models.ForeignKey       ('self',null=True, blank=True,on_delete=models.DO_NOTHING,  )
    dev_collect_values_if_cond_force_value_e = models.NullBooleanField (blank=False, null=False ,default=False, verbose_name="if cond False")
    dev_collect_values_if_cond_force_value = models.FloatField       (blank=True, null=True,verbose_name="Force value")
    def save(self, *args, **kwargs):
        if not self.pk:
            cursor = connection.cursor()
            sql = """CREATE TABLE maapi_dev_rom_{0}_values (id SERIAL PRIMARY KEY,  dev_id integer,  dev_timestamp  TIMESTAMP DEFAULT CURRENT_TIMESTAMP, dev_value real)""".format(self.dev_rom_id.replace("-", "_"))
            cursor.execute(sql)
            cursor.close()
        super(Devices, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        cursor = connection.cursor()
        sql = "DROP TABLE maapi_dev_rom_{0}_values".format(self.dev_rom_id.replace("-", "_"))
        cursor.execute(sql)
        cursor.close()
        super(Devices, self).delete(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.dev_user_name
    class Meta:
        managed = True
        db_table = 'devices'
        verbose_name_plural = "Settings - All Sensors "


class MailingList(models.Model):
    ml_user_id              = models.IntegerField     (default=9999, null=False,blank=False , verbose_name="id")
    ml_name                 = models.CharField        (max_length=60, default="Name",null=False,blank=False, verbose_name="Name")
    ml_user                 = models.CharField        (max_length=30, default="someone @ server",null=False,blank=False, verbose_name="Mail addres")
    ml_password             = models.CharField        (max_length=255, null=False, verbose_name="Password")
    ml_smtp                 = models.CharField        (max_length=255, null=False, default='smtp.gmail.com', verbose_name="Smtp")
    ml_port                 = models.IntegerField     (default=587, null=False, blank=False , verbose_name="smtp port")
    def __unicode__(self):
        return u'%s' % self.ml_name
    class Meta:
        managed = True
        db_table = 'maapi_mailing_list'
        verbose_name_plural = "Settings - List - Source Emails Accounts"


class MailWachDog(models.Model):
    mail_user_id             = models.IntegerField     (default=9999, null=False,blank=False , verbose_name="Id")
    mail_name                = models.CharField        (max_length=30, default="Name",null=False,blank=False, verbose_name="Name")
    mail_data_from_sensor    = models.ForeignKey       (Devices, on_delete=models.DO_NOTHING, related_name="devices_msail", blank=False, null=False, verbose_name="Source Sensor")
    mail_condition_min_e     = models.NullBooleanField (blank=False, null=False, default=False , verbose_name="Enable Value <= X")
    mail_condition_min       = models.FloatField       (blank=False, null=False , default=0, verbose_name="Sensor Value Value<= X")
    mail_condition_max_e     = models.NullBooleanField (blank=False, null=False, default=False , verbose_name="Enable Value >= X")
    mail_condition_max       = models.FloatField       (blank=False, null=False , default=0, verbose_name="Sensor Value >= X")
    mail_data                = models.ForeignKey       (MailingList, on_delete=models.DO_NOTHING, related_name="MailingList", blank=False, null=False, verbose_name="Mail - settings")
    mail_send_to             = models.CharField        (max_length=255, null=False, verbose_name="Send to")
    mail_subject             = models.CharField        (max_length=255, null=False, verbose_name="subject")
    mail_mesge_if_min        = models.CharField        (max_length=255, null=False, verbose_name="message if <= min")
    mail_mesge_if_max        = models.CharField        (max_length=255, null=False, verbose_name="message if >= max")
    mail_last_sended_at_value_min= models.FloatField   (blank=False, null=False , default=999999, verbose_name="Last Sended at Value_min")
    mail_last_sended_at_value_max= models.FloatField   (blank=False, null=False , default=-999999, verbose_name="Last Sended at Value_max")
    mail_enabled             = models.NullBooleanField (blank=True, null=True ,default=False)
    mail_range_acc           = models.IntegerField     (blank=False, null=False, default=1, verbose_name="Accuracy Range")
    class Meta:
        managed = False
        db_table = 'maapi_mail'
        verbose_name_plural = "WatchMan - Send mail"


class BackgroudListModel(models.Model):
    bg_id               = models.IntegerField       (blank=False, null=False, default=0, verbose_name="id")
    bg_name             = models.CharField          (max_length=30, null=False, verbose_name="Backgroud file name")
    def __unicode__(self):
        return u'%s' % self.bg_name
    class Meta:
        managed = False
        db_table = 'maapi_backgroud_list'
        verbose_name_plural = "Settings - List - Backgroud"


class MainScreen(models.Model):
    """table where user can chose elements on main screen"""
    dev_on_main_id              = models.IntegerField       (blank=False, null=False, default=0, verbose_name="User id")
    dev_on_main_name            = models.CharField          (max_length=30, null=False, verbose_name="Set name")
    main_backgroud              = models.ForeignKey         (BackgroudListModel, on_delete=models.DO_NOTHING, related_name="main_backgroud_p",blank=True, null=True, verbose_name="Choise backgroud")
    dev_on_main_screen_main     = models.ForeignKey         (Devices, on_delete=models.DO_NOTHING, related_name="dev_11",blank=True, null=True, verbose_name="Main sensor", help_text="Big value on main screen")
    dev_on_main_screen_1        = models.ForeignKey         (Devices, on_delete=models.DO_NOTHING, related_name="dev_12",blank=True, null=True, verbose_name="1 Sensor", help_text="1 sernsor in list on main screen")
    dev_on_main_screen_2        = models.ForeignKey         (Devices, on_delete=models.DO_NOTHING, related_name="dev_13",blank=True, null=True, verbose_name="2 Sensor", help_text="2 sernsor in list on main screen ")
    dev_on_main_screen_3        = models.ForeignKey         (Devices, on_delete=models.DO_NOTHING, related_name="dev_14",blank=True, null=True, verbose_name="3 Sensor", help_text="3 sernsor in list on main screen ")
    dev_on_main_screen_4        = models.ForeignKey         (Devices, on_delete=models.DO_NOTHING, related_name="dev_15",blank=True, null=True, verbose_name="4 Sensor", help_text="4 sernsor in list on main screen ")
    dev_on_main_screen_5        = models.ForeignKey         (Devices, on_delete=models.DO_NOTHING, related_name="dev_16",blank=True, null=True, verbose_name="5 Sensor", help_text="5 sernsor in list on main screen ")
    dev_on_main_screen_6        = models.ForeignKey         (Devices, on_delete=models.DO_NOTHING, related_name="dev_17",blank=True, null=True, verbose_name="6 Sensor", help_text="6 sernsor in list on main screen ")
    dev_on_main_screen_7        = models.ForeignKey         (Devices, on_delete=models.DO_NOTHING, related_name="dev_18",blank=True, null=True, verbose_name="7 Sensor", help_text="7 sernsor in list on main screen ")
    dev_on_main_screen_8        = models.ForeignKey         (Devices, on_delete=models.DO_NOTHING, related_name="dev_19",blank=True, null=True, verbose_name="8 Sensor", help_text="8 sernsor in list on main screen ")
    dev_on_main_screen_9        = models.ForeignKey         (Devices, on_delete=models.DO_NOTHING, related_name="dev_110",blank=True, null=True, verbose_name="9 Sensor", help_text="9 sernsor in list on main screen ")
    dev_on_main_screen_10       = models.ForeignKey         (Devices, on_delete=models.DO_NOTHING, related_name="dev_111",blank=True, null=True, verbose_name="10 Sensor", help_text="10 sernsor in list on main screen ")
    dev_on_main_screen_11       = models.ForeignKey         (Devices, on_delete=models.DO_NOTHING, related_name="dev_112",blank=True, null=True, verbose_name="11 Sensor", help_text="11 sernsor in list on main screen ")
    dev_on_main_screen_12       = models.ForeignKey         (Devices, on_delete=models.DO_NOTHING, related_name="dev_113",blank=True, null=True, verbose_name="12 Sensor", help_text="12 sernsor in list on main screen ")
    dev_on_main_enabled         = models.NullBooleanField   (blank=False, null=False, default=False, verbose_name="Enabled")
    class Meta:
        managed = False
        db_table = 'maapi_main_screen'
        verbose_name_plural = "Settings - Site Main Screen "


class SqlQuery(models.Model):
    sql_user_id                 = models.IntegerField       (blank=False, null=False, default=0)
    sql_name                    = models.CharField          (blank=False, null=False,max_length=60)
    sql_query                   = models.TextField          (blank=False, null=False)
    sql_descript                = models.CharField          (blank=True, null=True,max_length=255)
    sql_enabled                 = models.NullBooleanField   (blank=False, null=False, default=False )
    class Meta:
        managed = False
        db_table = 'maapi_sqlquery'
        verbose_name_plural = "Exec - Sql Query"


class MathModel(models.Model):
    """table with math expresions, you can chose 4 difrent sensors, calculate value and update chosen sensor"""
    math_user_id                = models.IntegerField       (blank=False, null=False, default=0, verbose_name="User Id")
    math_name                   = models.CharField          (blank=False, null=False,max_length=60, verbose_name="Name")
    math_data_from_1            = models.ForeignKey         (Devices, on_delete=models.DO_NOTHING, related_name="dev_1",blank=True, null=True, verbose_name="v1 - Value From Sensor")
    math_data_from_2            = models.ForeignKey         (Devices, on_delete=models.DO_NOTHING, related_name="dev_2",blank=True, null=True, verbose_name="v2 - Value From Sensor")
    math_data_from_3            = models.ForeignKey         (Devices, on_delete=models.DO_NOTHING, related_name="dev_3",blank=True, null=True, verbose_name="v3 - Value From Sensor")
    math_data_from_4            = models.ForeignKey         (Devices, on_delete=models.DO_NOTHING, related_name="dev_4",blank=True, null=True, verbose_name="v4 - Value From Sensor")
    math_math                   = models.CharField          (blank=False, null=False,max_length=255, verbose_name="Math Expression", help_text="E.g. v1 * (v2 + v3) / v4 + 100")
    math_descript               = models.CharField          (blank=False, null=False,max_length=255, verbose_name="Description")
    math_update_rom             = models.ForeignKey         (Devices, on_delete=models.DO_NOTHING, related_name="dev_5", verbose_name="Output Sensor")
    math_enabled                = models.NullBooleanField   (blank=False, null=False, default=False , verbose_name="Enabled")
    #math_exec_if_cond_e         = models.NullBooleanField   (blank=False, null=False, default=False , verbose_name="Enabled")
    #math_exec_cond              = models.ForeignKey         (Devices, on_delete=models.DO_NOTHING,related_name="dev_10010",blank=True, null=True, verbose_name="Reference Sensor")
    #math_exec_cond_value_min    = models.FloatField         (blank=False, null=False , default=0, verbose_name="Referens < X" )
    #math_exec_cond_value_max    = models.FloatField         (blank=False, null=False , default=0, verbose_name="Referens > X" )
    #math_exec_cond_value_min_e  = models.NullBooleanField   (blank=False, null=False, default=False , verbose_name="Enable value < X")
    #math_exec_cond_value_max_e  = models.NullBooleanField   (blank=False, null=False, default=False , verbose_name="Enable value > X")
    #math_exec_cond_force_value_e  = models.NullBooleanField   (blank=False, null=False, default=False , verbose_name="If Ref. != cond. put value")
    #math_exec_cond_force_value   = models.FloatField         (blank=False, null=False , default=0, verbose_name="value" )

    class Meta:
        managed = False
        db_table = 'maapi_math'
        verbose_name_plural = "Exec - Mathematical Expresions"


class SwitchModel(models.Model):
    """table with conditions - if condition is tre or false do on or off gpio"""
    switch_user_id                          = models.IntegerField           (blank=False, null=False, default=0, verbose_name="Id")
    switch_name                             = models.CharField              (blank=False, null=False,max_length=60, verbose_name="Name")
    switch_data_from_sens                   = models.ForeignKey             (Devices, on_delete=models.DO_NOTHING, related_name="dev_33",blank=False, null=False, verbose_name="Source Sensor")
    switch_range_acc                        = models.IntegerField           (blank=False, null=False, default=1, verbose_name="Accuracy Range")

    switch_value_min_e                      = models.NullBooleanField       (blank=False, null=False, default=False , verbose_name="Enable Source Sensor < X")
    switch_reference_sensor_min_e           = models.NullBooleanField       (blank=False, null=False, default=False , verbose_name="Enable Reference Sensor")
    switch_reference_sensor_min             = models.ForeignKey             (Devices, on_delete=models.DO_NOTHING,related_name="dev_34",blank=True, null=True, verbose_name="Reference Sensor")
    switch_value_min                        = models.FloatField             (blank=False, null=False , default=0, verbose_name="Source < X or S. < (R. - X)" , help_text="Source Sens < X , or if Enabled RefSens Source Sens < Reference Sens - X")
    #switch_state_at_min                    = models.NullBooleanField       (blank=False, null=False, default=True, verbose_name="State At condition true")

    switch_value_max_e                      = models.NullBooleanField       (blank=False, null=False, default=False , verbose_name="Enable Source Sensor > X")
    switch_reference_sensor_max_e           = models.NullBooleanField       (blank=False, null=False, default=False , verbose_name="Enable Reference Sensor")
    switch_reference_sensor_max             = models.ForeignKey             (Devices, on_delete=models.DO_NOTHING,related_name="dev_35",blank=True, null=True, verbose_name="Reference Sensor")
    switch_value_max                        = models.FloatField             (blank=False, null=False, default=0, verbose_name="Source > X or S. > (R. + X)", help_text="Source Sens > X , or if Enabled RefSens Source Sens > Reference Sens - X")
    #switch_state_at_max                    = models.NullBooleanField       (blank=False, null=False, default=True, verbose_name="State At condition true")

    switch_invert                           = models.NullBooleanField       (blank=False, null=False, default=False , verbose_name="Invert gpio State")
    switch_descript                         = models.CharField              (blank=False, null=False,max_length=60 , verbose_name="Description")
    switch_update_rom                       = models.ForeignKey             (Devices, on_delete=models.DO_NOTHING, related_name="dev_31",blank=False, null=False , verbose_name="Output Sensor", help_text="Which sensor i have to update? - value")
    switch_enabled                          = models.NullBooleanField       (blank=False, null=False, default=False, verbose_name="Enabled")

    #switch_turn_on_at_sensor_e              = models.NullBooleanField       (blank=False, null=False, default=False, verbose_name="switch on - if sensor")
    #switch_turn_on_at_sensor                = models.ForeignKey             (Devices, on_delete=models.DO_NOTHING,related_name="dev_222",blank=True, null=True, verbose_name="Reference Sensor")
    #switch_turn_on_at_sensor_value_min_e    = models.NullBooleanField       (blank=False, null=False, default=False, verbose_name="Enable min")
    #switch_turn_on_at_sensor_value_min      = models.FloatField             (blank=True, null=True, default=0, verbose_name="Source < X")
    #switch_turn_on_at_sensor_value_max_e     = models.NullBooleanField      (blank=False, null=False, default=False, verbose_name="Enable max")
    #switch_turn_on_at_sensor_value_max      = models.FloatField             (blank=True, null=True, default=0, verbose_name="Source > X")
    #switch_turn_on_at_cond_not_e            = models.NullBooleanField      (blank=False, null=False, default=False, verbose_name="if Sensor != cond. put state")
    #switch_turn_on_at_cond_not_val          = models.NullBooleanField      (blank=False, null=False, default=False, verbose_name="State 1=True 0=False")
    class Meta:
        managed = False
        db_table = 'maapi_switch'
        verbose_name_plural = "WatchMan - Switch"


class Logs(models.Model):
    log_id              = models.AutoField      (primary_key=True)
    log_time_stamp      = models.DateTimeField  (blank=True, null=True)
    log_name            = models.TextField()
    log_file_name       = models.TextField()
    log_describe        = models.TextField()
    log_additional_data = models.TextField      (blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'logs'
        verbose_name_plural = "MaaPi Log's"


class CommandLine(models.Model):
    cmd_id              = models.AutoField          (primary_key=True, verbose_name="Id")
    cmd_user_id         = models.IntegerField       (blank=False, null=False, default=0, verbose_name="User Id")
    cmd_name            = models.CharField          (blank=False, null=False,max_length=60,verbose_name="Name")
    cmd_command         = models.CharField          (blank=False, null=False,max_length=255,verbose_name="Command")
    cmd_describe        = models.CharField          (blank=False, null=False,max_length=60,verbose_name="Description")
    cmd_update_rom      = models.ForeignKey         (Devices, on_delete=models.DO_NOTHING, related_name="dev_100",blank=False, null=False, verbose_name="Sensor - Output" )
    cmd_location        = models.CharField          (blank=False, null=False,max_length=60, verbose_name="Location",  help_text="On Which machine i have to run this command?")
    cmd_enabled         = models.NullBooleanField   (blank=False, null=False, default=False,verbose_name="Enabled")
    class Meta:
        managed = True
        db_table = 'maapi_commandline'
        verbose_name_plural = "Exec - Linux commands"
