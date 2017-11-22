# coding: utf-8
from django.contrib import admin
from .models import MaapiFuturesModel,CronModel, BackgroudListModel,PortListenerModel, ScanedOneWireListModel,  Devices, Groups, Units, Locations, Logs, SensorsList, CommandLine, SqlQuery, MathModel, MainScreen, SwitchModel ,BusTypes, MailWachDog, MailingList


@admin.register(Devices)
class DevicesAdmin(admin.ModelAdmin):
    ordering=['dev_user_id']

    fieldsets = [
                ('Main device parameters',              {'fields': ['dev_user_id', 'dev_user_name', 'dev_user_describe', 'dev_rom_id', 'dev_time_stamp','dev_status']}),
                ('Bus and type parameters',             {'fields': ['dev_type','dev_bus_type','dev_unit', 'dev_gpio_pin','dev_hidden','dev_sensor_type']}),
                ('Device - value info ',                {'fields': ['dev_value','dev_adjust','dev_value_old','dev_last_update','dev_read_error','dev_interval','dev_interval_unit_id']}),

                ('Database',                             {'fields': ['dev_collect_values_to_db',
                                                                     'dev_collect_values_if_cond_e',
                                                                     'dev_collect_values_if_cond_from_dev_e',
                                                                     'dev_collect_values_if_cond_from_dev',
                                                                     'dev_collect_values_if_cond_min_e',
                                                                     'dev_collect_values_if_cond_min',
                                                                     'dev_collect_values_if_cond_max_e',
                                                                     'dev_collect_values_if_cond_max',
                                                                     ]}),

                ('Location and Groups',                 {'fields': ['dev_location','dev_main_group','dev_sec_group','dev_third_group',]}),
                ]

    list_display=[
                  'dev_id',
                  'dev_user_id',
                  'dev_user_name',
                  'dev_rom_id',
                  'dev_type',
                  'dev_bus_type',
                  'dev_unit',
                  'dev_location',
                  'dev_main_group',
                  'dev_sec_group',
                  'dev_third_group',
                  'dev_value',
                  'dev_interval',
                  'dev_interval_unit_id',
                  'dev_last_update',
                  'dev_status',
                  'dev_hidden',


                  ]
    list_display_links = list_display
    list_filter = [
        ('dev_main_group', admin.RelatedOnlyFieldListFilter),
        ('dev_location', admin.RelatedOnlyFieldListFilter),
        ('dev_type', admin.RelatedOnlyFieldListFilter),
        ('dev_bus_type', admin.RelatedOnlyFieldListFilter),
        ]

    def get_readonly_fields(self, request, obj=None):
        if obj: # editing an existing object
            return self.readonly_fields + ('dev_rom_id',)
        return self.readonly_fields



@admin.register(MailWachDog)
class MailWachDogAdmin(admin.ModelAdmin):
    list_display=['mail_user_id','mail_name','mail_condition_min_e','mail_condition_max_e','mail_send_to','mail_enabled']
    list_display_links = list_display
    fieldsets = [
                ('WatchMan - Send mail  - info',             {'fields': ['mail_user_id', 'mail_name', ]}),
                ('Get value form device',                    {'fields': ['mail_data_from_sensor','mail_range_acc']}),
                ('Conditions min / max ',                    {'fields': ['mail_condition_min_e','mail_condition_min','mail_condition_max_e','mail_condition_max']}),
                ('Mail Settings',                            {'fields': ['mail_data', 'mail_send_to']}),
                ('Mail subject and content',                 {'fields': ['mail_subject', 'mail_mesge_if_min','mail_mesge_if_max']}),
            #    ('Last sent value ',                         {'fields': ['mail_last_sended_at_value_min', 'mail_last_sended_at_value_max']}),
                ('Status ',                                  {'fields': ['mail_enabled']}),
                ]
    class Media:
        js = ('/static/admin/js/hide_mail_form.js',)


@admin.register(PortListenerModel)
class PortListenerModelAdmin(admin.ModelAdmin):
    list_display=['pl_name','pl_timestamp','pl_running','pl_enabled','pl_location']
    list_display_links = list_display
    readonly_fields=('pl_running', 'pl_timestamp')
    fieldsets = [
                ('info',                                     {'fields': ['pl_id', 'pl_name', 'pl_timestamp','pl_running' ]}),
                ('Enabled?',                                 {'fields': ['pl_enabled']}),
                ('Start / stop commands ',                   {'fields': ['pl_command_start','pl_command_stop']}),
                ('location ',                                {'fields': ['pl_location']}),
                ]




@admin.register(ScanedOneWireListModel)
class ScanedOneWireListModelAdmin(admin.ModelAdmin):
    list_display=['device_id','device_name','device_description']
    list_display_links = list_display

@admin.register(MaapiFuturesModel)
class MaapiFuturesAdmin(admin.ModelAdmin):
    list_display=['f_name','f_descript','f_done','f_added','f_created']
    list_display_links = list_display




@admin.register(BackgroudListModel)
class ScanedOneWireListModelAdmin(admin.ModelAdmin):
    list_display=['bg_id','bg_name']
    list_display_links = list_display


@admin.register(CommandLine)
class CommandLineAdmin(admin.ModelAdmin):
    ordering=['-cmd_id']
    list_display=['cmd_id','cmd_user_id','cmd_name','cmd_command','cmd_describe','cmd_location','cmd_enabled']
    list_display_links = list_display

    fieldsets = [
                ('Exec Linux Command - info',               {'fields': ['cmd_user_id', 'cmd_name', 'cmd_describe' ]}),
                ('Command to execute ',                     {'fields': ['cmd_command',]}),
                ('Select device to update value',           {'fields': ['cmd_update_rom']}),
                ('Where To Execute And Status ',            {'fields': ['cmd_location', 'cmd_enabled']}),
                ]


@admin.register(CronModel)
class CronModelAdmin(admin.ModelAdmin):
    list_display=[  'pk',
                    'cron_last_file_exec',

                    'cron_interpreter',
                    'cron_file_path',
                    'cron_minute_on_every_id',
                    'cron_minute_id',
                    'cron_hour_on_every_id',
                    'cron_hour_id',
                    'cron_day_on_every_id',
                    'cron_day_id',
                    'cron_where_exec',
                    'cron_time_of_exec',
                    'cron_enabled'
                ]
    list_display_links = list_display
    fieldsets = [
                ('Settings - Linux Cron Table - info',      {'fields': ['cron_comment','cron_last_exec_date','cron_last_file_exec']}),
                ('Cron Interval - 1 every: run on each minute./hour/day, 1 on: run only in this min./hour/day',         {'fields': ['cron_minute_id','cron_minute_on_every_id',
                                                                                                                'cron_hour_id','cron_hour_on_every_id',
                                                                                                                'cron_day_id','cron_day_on_every_id',]}),
                ('Execute command',                         {'fields': ['cron_interpreter','cron_file_path']}),
                ('Where To Execute And Status ',            {'fields': ['cron_where_exec', 'cron_enabled']}),
                ]


@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):

    list_display=['pk','group_user_id','group_name','group_enabled']
    list_display_links = list_display
    fieldsets = [
                ('Settings - Sensors Groups - info',             {'fields': ['group_user_id', 'group_name', ]}),
                ('Status ',                                  {'fields': ['group_enabled']}),
                ]


@admin.register(Units)
class UnitAdmin(admin.ModelAdmin):

    list_display=['pk','unit_user_id','unit_name','unit_sign','unit_enabled']
    list_display_links = list_display
    fieldsets = [
                ('Settings - Sensors Units  - info',             {'fields': ['unit_user_id', 'unit_name','unit_sign']}),
                ('Status ',                                  {'fields': ['unit_enabled']}),
                ]


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):

    list_display=['ml_user_id','ml_name','ml_user','ml_smtp','ml_port']
    list_display_links = list_display
    fieldsets = [
                ('Settings - Emails accounts list  - info',      {'fields': ['ml_user_id','ml_name',]}),
                ('Email data ',                                  {'fields': ['ml_user','ml_password','ml_smtp','ml_port']}),
                ]


@admin.register(BusTypes)
class BusTypesAdmin(admin.ModelAdmin):

    list_display=['bus_name','bus_type','bus_description','bus_enabled']
    list_display_links = list_display
    fieldsets = [
                ('Settings - Bus Types - info',             {'fields': ['bus_name', 'bus_description', ]}),
                ('Bus Type ',                               {'fields': ['bus_type',]}),
                ('Status ',                                 {'fields': ['bus_enabled']}),

                ]


@admin.register(SwitchModel)
class SwitchModelAdmin(admin.ModelAdmin):
    ordering=['id']
    list_display=['switch_name','switch_value_min_e','switch_value_max_e','switch_invert','switch_descript','switch_enabled']
    list_display_links = list_display
    fieldsets = [
                ('WatchMan - Switch - info',                 {'fields': ['switch_user_id', 'switch_name','switch_descript' ,'switch_data_from_sens','switch_range_acc']}),
                ('Switch at min value ',                     {'fields': ['switch_value_min_e','switch_reference_sensor_min_e','switch_reference_sensor_min','switch_value_min']}),
                ('Switch at max value ',                     {'fields': ['switch_value_max_e','switch_reference_sensor_max_e','switch_reference_sensor_max','switch_value_max']}),
                ('Gpio state invert',                        {'fields': ['switch_invert',
                                                                         'switch_turn_on_at_sensor_e',
                                                                         'switch_turn_on_at_sensor',
                                                                         'switch_turn_on_at_sensor_value_min_e',
                                                                         'switch_turn_on_at_sensor_value_min',
                                                                         'switch_turn_on_at_sensor_value_max_e',
                                                                         'switch_turn_on_at_sensor_value_max']}),
                ('Select device to update value',            {'fields': ['switch_update_rom']}),
                ('Status ',                                  {'fields': ['switch_enabled']}),
                ]
    class Media:
        js = ('/static/admin/js/hide_switch_form.js',)


@admin.register(Locations)
class LocationsAdmin(admin.ModelAdmin):

    list_display=['location_user_id','location_name','location_enabled']
    list_display_links = list_display
    fieldsets = [
                ('Settings - Sensors Locations - info',      {'fields': ['location_user_id','location_name',]}),
                ('Status ',                                  {'fields': ['location_enabled']}),
                ]


@admin.register(MainScreen)
class MainScreenAdmin(admin.ModelAdmin):

    list_display=[
                    'dev_on_main_id',
                    'dev_on_main_name',
                    'dev_on_main_enabled',
                    ]
    list_display_links = list_display
    fieldsets = [
                ('Settings - Sensors on Main screen - info',        {'fields': ['dev_on_main_id','dev_on_main_name']}),
                ('Choise main backgroud',                           {'fields': ['main_backgroud']}),
                ('Main device on Main screen',                      {'fields': ['dev_on_main_screen_main']}),
                ('devices on Main screen',                          {'fields': ['dev_on_main_screen_1','dev_on_main_screen_2','dev_on_main_screen_3','dev_on_main_screen_4','dev_on_main_screen_5','dev_on_main_screen_6','dev_on_main_screen_7','dev_on_main_screen_8','dev_on_main_screen_9','dev_on_main_screen_10','dev_on_main_screen_11','dev_on_main_screen_12',]}),
                ('Status ',                                         {'fields': ['dev_on_main_enabled']}),
                ]



@admin.register(MathModel)
class MathModelAdmin(admin.ModelAdmin):
    ordering=['-id']
    list_display=[
                    'id',
                    'math_name',
                    'math_math',
                    'math_descript',
                    'math_enabled',
                ]
    list_display_links = list_display
    fieldsets = [
                ('Exec - Mathematical Expresions - info',   {'fields': ['math_user_id', 'math_name', 'math_descript' ]}),
                ('Get data from devices',                   {'fields': ['math_data_from_1','math_data_from_2','math_data_from_3','math_data_from_4',]}),
                ('Mathematical Expresion',                  {'fields': ['math_math']}),

                ('Select device to update value',      {'fields': ['math_update_rom']}),
                ('Exec expression when condition is true',          {'fields': ['math_exec_if_cond_e','math_exec_cond','math_exec_cond_value_min_e','math_exec_cond_value_min','math_exec_cond_value_max_e','math_exec_cond_value_max','math_exec_cond_force_value_e','math_exec_cond_force_value']}),
                ('Status ',                                 {'fields': ['math_enabled']}),
                ]
    class Media:
        js = ('/static/admin/js/hide_from_math.js',)


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    ordering=['-log_time_stamp']
    list_display=['log_id','log_time_stamp','log_name','log_file_name','log_describe','log_additional_data']
    list_display_links = list_display


@admin.register(SensorsList)
class SensorsListAdmin(admin.ModelAdmin):
    ordering=['id']
    list_display=['id','device_name','device_desctiption','device_lib_name','device_location','device_enabled']
    list_display_links = list_display
    fieldsets = [
                ('Settings - Sensors list  - info',          {'fields': ['device_desctiption',]}),
                ('Device type - name ',                      {'fields': ['device_name']}),
                ('Library ',                                 {'fields': ['device_lib_name']}),
                ('Status ',                                  {'fields': ['device_location','device_enabled']}),
                ]
