import json
import requests
from django.db.models import Q
from django.http import HttpResponse
from apps.home.models import *
import xlwt
from xlwt import *
import datetime

# Get token
authToken = ''
import subprocess
import traceback
headers = dict()

subprocess.call('/home/TVadmin/django_code/wanextract/auth.sh', shell=True)
filepath = '/home/TVadmin/django_code/wanextract/tvc-client.cookie'
with open(filepath) as fp:
    line = fp.readline()
    cnt = 1
    while line:
        if len(line.split('\t')) > 1:
            authToken = line.split('\t')[6].split('\n')[0]
            print("authToken: ", authToken)
        line = fp.readline()
        cnt += 1
headers['Cookie'] = 'authToken=' + authToken
headers['User-Agent'] = 'curl/7.29.0'
headers['Accept'] = '*/*'

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


def extract_total_octets_per_site(timestamp_from, timestamp_to):
    response = HttpResponse(content_type='application/ms-excel')
    filename = "TotalOctectperSite.xls"
    response['Content-Disposition'] = 'attachment; ' + 'filename=' + filename

    center_style = xlwt.easyxf("align: vert centre, horiz centre")
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('OctetsPerSite', True)
    columns = ['PROVIDER', 'SITE NAME', 'RxOctets', 'TxOctets', 'TotalOctets',]

    for col_num in range(len(columns)):
        ws.write(0, col_num, columns[col_num], style)
        ws.col(col_num).width = COL_WIDTH

    ws.write_merge(1, 1, 0, 7, 'Extract Total Octets per Site from {} to {}'.format(str(datetime.datetime.fromtimestamp(timestamp_from)), str(datetime.datetime.fromtimestamp(timestamp_to))), style)

    url = 'http://tlspbnflow02/api/v1/perfdata?ViewBy=Site&Metric=RxOctets&Metric=TxOctets&Metric=TotalOctets&OrderBy=TotalOctets&dir=DESC&grid=true&wait=false&MaxRows=30&period=CUSTOM_TIME&autoUpdate=false&startTime={}&endTime={}'.format(timestamp_from, timestamp_to)
    response = requests.get(url, headers=headers, verify=False)
    response = json.loads(response.text)

    row_num = 2
    if "records" in response.keys():
        for site in response['records']:
            ws.write(row_num, 0, str(site), center_style)
            ws.write(row_num, 1, '', center_style)
            ws.write(row_num, 2, '', center_style)
            ws.write(row_num, 4, '', center_style)
            ws.write(row_num, 5, '', center_style)
            row_num += 1

    wb.save(response)
    return response
