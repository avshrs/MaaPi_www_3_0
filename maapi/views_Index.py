from maapi.models import Groups, Devices, MainScreen
from datetime import datetime, date, timedelta
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView


class MainIndexView(ListView):
    model = Devices
    template_name = '1/_Main.html'

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(MainIndexView, self).get_context_data(**kwargs)
        main_dev = []
        main_list = MainScreen.objects.values('dev_on_main_screen_1',
                                              'dev_on_main_screen_2',
                                              'dev_on_main_screen_2',
                                              'dev_on_main_screen_3',
                                              'dev_on_main_screen_4',
                                              'dev_on_main_screen_5',
                                              'dev_on_main_screen_6',
                                              'dev_on_main_screen_7',
                                              'dev_on_main_screen_8',
                                              'dev_on_main_screen_9',
                                              'dev_on_main_screen_10',
                                              'dev_on_main_screen_11',
                                              'dev_on_main_screen_12',
                                              'dev_on_main_enabled',
                                              'dev_on_main_screen_main',
                                              'main_backgroud',
                                              )[0]
        print(main_list)
        print(main_list['dev_on_main_screen_main'])
        
        devices = Devices.objects.values('dev_id',
                                         'dev_user_name',
                                         'dev_value',
                                         'dev_unit',
                                         'dev_adjust',
                                         'dev_unit_id',
                                         'dev_location'
                                         ).filter(
                                             dev_status=True
                                             ).filter(
                                                 dev_hidden=False
                                                 ).order_by('dev_user_id')
        print(devices)
        for i in range(1, 13):
            try:
                if main_list[f'dev_on_main_screen_{i}'] is not None:
                    main_dev.append(main_list[f'dev_on_main_screen_{i}'])
            except Exception:
                pass
        dev_main = []
        for dev in devices:
            print(dev)
            if dev['dev_id'] == main_list['dev_on_main_screen_main']:
                print("indev", dev)
                dev_main.append(dev)
                print(dev_main)
        context['temp'] = dev_main
        context['dev_on_main_screen'] = main_dev
        context['date_time'] = datetime.now()
        context['data'] = devices
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        else:
            return HttpResponseRedirect('/login')
        return super(MainIndexView, self).dispatch(request, *args, **kwargs)

    class Media:
        css = {'all': ('/static/assets/css/main.css', )}
        js = ('/static/admin/js/hide_mail_form.js', )


class SensorListView(ListView):
    model = Devices
    template_name = '1/_SensorListDetail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context

        context = super(SensorListView, self).get_context_data(**kwargs)
        context['date_time'] = datetime.now()
        context['devices'] = Devices.objects.order_by('dev_user_id').filter(
            dev_status=True).filter(dev_hidden=False)
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        else:
            return HttpResponseRedirect('/login')
        return super(SensorListView, self).dispatch(request, *args, **kwargs)


class SensorsDetailListView(ListView):
    model = Devices
    template_name = '1/_SensorsSettings.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SensorsDetailListView, self).get_context_data(**kwargs)
        context['date_time'] = datetime.now()
        context['devices'] = Devices.objects.order_by('dev_user_id').filter(dev_hidden=False)
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        else:
            return HttpResponseRedirect('/login')
        return super(SensorsDetailListView, self).dispatch(
            request, *args, **kwargs)


class twenty(TemplateView):
    template_name = 'twenty/index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            pass
        else:
            return HttpResponseRedirect('/login')
        return super(twenty, self).dispatch(request, *args, **kwargs)
