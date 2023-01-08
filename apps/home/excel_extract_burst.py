import json

from django.shortcuts import render
import time
import datetime

from django.db.models import Q
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from apps.home.models import *

import xlwt
import xlrd
from xlwt import *
import requests

# Excel Conf
COL_WIDTH = 150 * 50

front_style = xlwt.XFStyle()
al = xlwt.Alignment()
al.horz = xlwt.Alignment().HORZ_CENTER
al.vert = xlwt.Alignment().VERT_CENTER
front_style.alignment = al
front_style.font.bold = True
pattern = xlwt.Pattern()
pattern.pattern = xlwt.Pattern.SOLID_PATTERN
pattern.pattern_fore_colour = xlwt.Style.colour_map['white']
front_style.pattern = pattern

fnt = Font()
fnt.name = 'Arial'
fnt.bold = True

borders = Borders()
borders.left = 6
borders.right = 6
borders.top = 6
borders.bottom = 6

alignment = Alignment()
alignment.horz = Alignment.HORZ_CENTER
alignment.vert = Alignment.VERT_CENTER

style = XFStyle()
style.font = fnt
style.borders = borders
style.alignment = alignment


def extract_input(datetime_from, datetime_to):
    response = HttpResponse(content_type='application/ms-excel')
    filename = "extract_inburst_congested.xls"
    response['Content-Disposition'] = 'attachment; ' + 'filename=' + filename

    center_style = xlwt.easyxf("align: vert centre, horiz centre")
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('INPUT_BURST_DETAIL', True)
    ws2 = wb.add_sheet('INPUT_BURST', True)
    columns = ['DATE', 'TIME', 'SITE NAME', 'ROUTER', 'INTERFACE', 'Capacity', 'Congested > 80%', 'Apps RxThroughput']
    columns2 = ['SITE NAME', 'ROUTER', 'INTERFACE', 'Nb of intervals (15 min) congested', 'Top Apps']

    for col_num in range(len(columns)):
        ws.write(0, col_num, columns[col_num], style)
        ws.col(col_num).width = COL_WIDTH

    #ws.write(1, 0, 'Extract from {} to {}'.format(str(datetime_from), str(datetime_to)), center_style)
    ws.write_merge(1, 1, 0, 7, 'Ingress Extract from {} to {}'.format(str(datetime_from), str(datetime_to)), style)
    for col_num in range(len(columns2)):
        ws2.write(0, col_num, columns2[col_num], style)
        ws2.col(col_num).width = COL_WIDTH

    ws2.write_merge(1, 1, 0, 7, 'Extract from {} to {}'.format(str(datetime_from), str(datetime_to)), center_style)

    dataset = InInterfaceBurst.objects.filter( Q(timestamp__gte=str(datetime_from)) & Q(timestamp__lte=str(datetime_to))).order_by('timestamp')
    row_num = 2
    for data in dataset:
        apps_data = ''
        apps_json_data = data.applications.replace("'", '"').replace("True", '"True"').replace("False", '"False"').replace("null", '"null"')
        apps_json_data = json.loads(apps_json_data)
        for app in apps_json_data:
            apps_data +=   app + ' : ' +  str(apps_json_data[app]['RxThroughput']/1000000) + ' Mbps  ' + '\n'

        ws.write_merge(row_num, row_num+5, 0, 0, str(data.date), center_style)
        ws.write_merge(row_num, row_num+5, 1, 1, str(data.time), center_style)
        ws.write_merge(row_num, row_num+5, 2, 2, str(data.interface.site.site_name), center_style)
        ws.write_merge(row_num, row_num+5, 3, 3, str(data.interface.deviceName), center_style)
        ws.write_merge(row_num, row_num+5, 4, 4, str(data.interface.name), center_style)
        ws.write_merge(row_num, row_num+5, 5, 5,  str(data.interface.in_bw/1000000) + ' Mbps', center_style)
        ws.write_merge(row_num, row_num+5, 6, 6, data.InBurst4, center_style)
        ws.write_merge(row_num, row_num+5, 7, 7, apps_data, center_style)
        row_num += 6

    # Synthese view
    # Get interfaces
    site_interfaces = list()
    list_interfaces = list()
    site_congestion_dict = dict()
    interface_congestion_dict = dict()
    for obj in dataset:
        if obj.interface not in list_interfaces:
            list_interfaces.append(obj.interface)

    for obj in dataset.values_list('interface__site__site_name').distinct():
        if obj[0] not in site_interfaces:
            site_congestion_dict[obj[0]] = list()

    for interface in list_interfaces:
        interface_congestion_dict[interface] = len(dataset.filter(interface=interface))
        site_congestion_dict[interface.site.site_name].append({0: interface, 1: len(dataset.filter(interface=interface))})

    row_num = 2
    for site in site_congestion_dict:
        ws2.write(row_num, 0, str(site), center_style)
        len_interface = len(site_congestion_dict[site])
        for itf in range(0, len_interface):
            ws2.write(row_num, 1, str(site_congestion_dict[site][itf][0].deviceName), center_style)
            ws2.write(row_num, 2, str(site_congestion_dict[site][itf][0].name), center_style)
            ws2.write(row_num, 3, str(site_congestion_dict[site][itf][0].in_bw / 1000000) + ' Mbps', center_style)
            ws2.write(row_num, 3, str(site_congestion_dict[site][itf][1]), center_style)
            row_num += 1

    total = 0
    for obj in interface_congestion_dict:
        total += interface_congestion_dict[obj]

    # wb.save('extract_inburst_congested' + '.xls')
    wb.save(response)
    return response

