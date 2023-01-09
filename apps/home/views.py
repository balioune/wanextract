# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.home.tables import *
from apps.home.filters import *
from apps.home.forms import TimestampForm, AppReportForm
from apps.home.excel_extract_burst import extract_input, extract_output
from apps.home.excel_extract_applications import extract_total_octets_per_site

from django.utils.timezone import datetime as django_datetime
import time
import datetime
@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))
@login_required(login_url="/login/")
def reports(request):

    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = TimestampForm(request.POST)
        if form.is_valid():
            # "%d/%m/%Y %H:%M:%S"
            timestamp1 = time.mktime(datetime.datetime.strptime(str(request.POST['date_from']), "%Y/%m/%d %H:%M").timetuple())
            timestamp2 = time.mktime(datetime.datetime.strptime(str(request.POST['date_to']), "%Y/%m/%d %H:%M").timetuple())
            if form.cleaned_data['report_type'] == 'inburst':
                return extract_input(datetime.datetime.fromtimestamp(timestamp1), datetime.datetime.fromtimestamp(timestamp2))
            elif form.cleaned_data['report_type'] == 'outburst':
                return extract_output(datetime.datetime.fromtimestamp(timestamp1), datetime.datetime.fromtimestamp(timestamp2))
            elif form.cleaned_data['report_type'] == 'applications':
                pass

    context = {'segment': 'reports'}
    table = SiteTable(Site.objects.all())
    context['table'] = table
    context['form'] = TimestampForm(request.POST)
    html_template = loader.get_template('home/reports.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def sites(request):
    context = {'segment': 'sites'}
    table = SiteTable(Site.objects.all())
    # RequestConfig(request, paginate={"per_page": PAGINATION_SIZE}).configure(table)
    context['table'] = table
    html_template = loader.get_template('home/sites.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def interfaces(request):
    context = {'segment': 'interfaces'}
    table = InterfaceTable(Interface.objects.all())
    # RequestConfig(request, paginate={"per_page": PAGINATION_SIZE}).configure(table)
    context['table'] = table
    html_template = loader.get_template('home/interfaces.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def applications(request):
    print(request.GET, type(request.GET))
    today = django_datetime.now().date()
    context = {'segment': 'applications'}

    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = AppReportForm(request.POST)
        if form.is_valid():
            # "%d/%m/%Y %H:%M:%S"
            timestamp1 = time.mktime(datetime.datetime.strptime(str(request.POST['date_from']), "%Y/%m/%d %H:%M").timetuple())
            timestamp2 = time.mktime(datetime.datetime.strptime(str(request.POST['date_to']), "%Y/%m/%d %H:%M").timetuple())
            if form.cleaned_data['report_type'] == 'octets':
                return extract_input(timestamp1, timestamp2)


    context['filter'] = filter
    context['form'] = AppReportForm(request.POST)
    context['table'] = ApplicationPerInterfaceTable(filter.qs)
    html_template = loader.get_template('home/applications.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def outburst(request):
    context = {'segment': 'outburst'}
    html_template = loader.get_template('home/outburst.html')
    filter = OutInterfaceBurstFilter(request.GET,
                                    queryset=OutInterfaceBurst.objects.filter(
                                        date=django_datetime.today() - datetime.timedelta(days=2)))
    filter = OutInterfaceBurstFilter(request.GET,
                                     queryset=OutInterfaceBurst.objects.all())
    context['filter'] = filter
    print(filter.qs)
    context['table'] = OutInterfaceBurstTable(filter.qs)
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def inburst(request):
    from apps.home.forms import TimestampForm
    print(request.POST)
    context = {'segment': 'inburst'}
    html_template = loader.get_template('home/inburst.html')
    filter = InInterfaceBurstFilter(request.GET,
                                    queryset=InInterfaceBurst.objects.filter(date=django_datetime.today() - datetime.timedelta(days=2)))
    context['filter'] = filter
    context['form'] = TimestampForm(request.POST)
    print(filter.qs)
    context['table'] = InInterfaceBurstTable(filter.qs)

    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def monthly_extract(request):
    from apps.home.forms import TimestampForm
    print(request.POST)
    context = {'segment': 'inburst'}
    html_template = loader.get_template('home/inburst.html')
    filter = InInterfaceBurstFilter(request.GET,
                                    queryset=InInterfaceBurst.objects.filter(date=django_datetime.today() - datetime.timedelta(days=2)))
    context['filter'] = filter
    context['form'] = TimestampForm(request.POST)
    print(filter.qs)
    context['table'] = InInterfaceBurstTable(filter.qs)

    return HttpResponse(html_template.render(context, request))
@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
