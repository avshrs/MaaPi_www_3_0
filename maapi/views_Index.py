
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
        dev_on_main_screen=[]
        for i in xrange(1,13):
            if MainScreen.objects.values_list('dev_on_main_screen_{0}'.format(i), flat=True)[0] is not None:
                dev_on_main_screen.append( MainScreen.objects.values_list('dev_on_main_screen_{0}'.format(i), flat=True)[0])
        context['temp'] =  Devices.objects.values('dev_id','dev_user_name','dev_value','dev_unit').filter(dev_hidden = False).filter(dev_id = (MainScreen.objects.values_list('dev_on_main_screen_main', flat=True)[0]))
        context['devices'] = Devices.objects.order_by('dev_user_id').filter(dev_hidden = False)
        context['dev_on_main_screen'] = dev_on_main_screen
        context['date_time'] = datetime.now()
        date_from = datetime.now().replace(microsecond=0) - timedelta(hours=1)
        context['data2'] = {'pk':1,'acc':24,'date_from':date_from,'date_to':'now'}
        context['data'] = Devices.objects.all().filter(dev_status = True).filter(dev_hidden = False).order_by('dev_user_id')
        return context
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            pass
        else:
            return HttpResponseRedirect('/login')
        return super(MainIndexView, self).dispatch(request, *args, **kwargs)
    class Media:
        css = {'all':('/static/assets/css/main.css',)}
        js = ('/static/admin/js/hide_mail_form.js',)

class SensorListView(ListView):
    model = Devices
    template_name = '1/_SensorListDetail.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context

        context = super(SensorListView, self).get_context_data(**kwargs)
   	context['date_time'] = datetime.now()
	context['devices'] = Devices.objects.order_by('dev_user_id').filter(dev_status = True).filter(dev_hidden = False)
        return context
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
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
        context['devices'] = Devices.objects.order_by('dev_user_id').all()
        return context
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            pass
        else:
            return HttpResponseRedirect('/login')
        return super(SensorsDetailListView, self).dispatch(request, *args, **kwargs)

class twenty(TemplateView):
    template_name = 'twenty/index.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            pass
        else:
            return HttpResponseRedirect('/login')
        return super(twenty, self).dispatch(request, *args, **kwargs)
