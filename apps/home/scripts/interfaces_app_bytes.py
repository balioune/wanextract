from extract.models import *
from __future__ import unicode_literals
import requests
from datetime import datetime
from datetime import date
import time
import json
from time import time as timestamp
from extract.models import *
import threading

# Get token
authToken = ''
import subprocess

subprocess.call('/home/TVadmin/django_code/analytics_dashboard/dashboard/auth.sh', shell=True)
filepath = 'tvc-client.cookie'
with open(filepath) as fp:
    line = fp.readline()
    cnt = 1
    while line:
        if len(line.split('\t')) > 1:
            authToken = line.split('\t')[6].split('\n')[0]
            print("authToken: ", authToken)
        line = fp.readline()
        cnt += 1

headers = dict()
headers['Cookie'] = 'authToken=' + authToken
headers['User-Agent'] = 'curl/7.29.0'
headers['Accept'] = '*/*'

"""
"""


def application_byte_per_interface_hourly(headers, AppId, start_time=None, end_time=None):
    # url = 'http://tlspbnflow02/api/v1/trafficanalysis?MetricSpace=uptimenpv&ViewBy=Time&ViewBy=Application&Metric=TotalThroughput&Metric=RxThroughput&Metric=TxThroughput&Metric=InCap&Metric=OutCap&grid=true&OrderBy=TotalThroughput&TopN=5&nfinterfaceId={}&PortIfType=2&DeviceIp={}&DeviceName={}CollectorId=0&period=CUSTOM_TIME&autoUpdate=false&startTime={}&endTime={}'.format(interfaceId, DeviceIp, DeviceName, start_time, end_time)
    url = 'http://tlspbnflow02/api/v1/perfdata?OrderBy=TotalOctets&dir=DESC&grid=true&wait=false&period=CUSTOM_TIME&autoUpdate=false&startTime={}&endTime={}&appId={}&ViewBy=Interface&Metric=TotalOctets&Metric=TxOctets&Metric=RxOctets'.format(
        start_time, end_time, AppId)
    try:
        response = requests.get(url, headers=headers, verify=False)
    except Exception:
        subprocess.call('/home/TVadmin/django_code/analytics_dashboard/dashboard/auth.sh', shell=True)
        filepath = 'tvc-client.cookie'
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
            response = requests.get(url, headers=headers, verify=False)
    return response.text


def applications_bytes_per_interfaces(headers, var_timestamp):
    from datetime import datetime
    local_timestamp = var_timestamp
    timestamp = local_timestamp
    END = str(local_timestamp).split('.')[0]
    START = str(local_timestamp - 3600).split('.')[0]
    try:
        date_en = datetime.fromtimestamp(timestamp).date()
        time_en = datetime.fromtimestamp(timestamp).time()
        print(str(date_en), str(time_en))
        print(str(datetime.fromtimestamp(local_timestamp - 3600).time()),
              str(datetime.fromtimestamp(local_timestamp).time()))
    except Exception:
        print(traceback.format_exc())
    RxOctets = 0.0
    TxOctets = 0.0
    for application in Application.objects.all():
        response = application_byte_per_interface_hourly(headers, application.truview_app_id, str(START) + '000',
                                                         str(END) + '000')
        response = json.loads(response)
        if "records" in response.keys():
            for record in response['records']:
                if application.name == 'O365_Teams':
                    RxOctets += record['RxOctets']
                    TxOctets += record['TxOctets']
                    print(application.name, record['Device']['name'], record['Interface']['name'], record['TxOctets'],
                          record['RxOctets'], record['TotalOctets'])
    print(application.name, record['Device']['name'], record['Interface']['name'], TxOctets, RxOctets)


from datetime import datetime
from time import time as timestamp
import traceback

local_timestamp = timestamp()
local_timestamp = 1670440507
local_timestamp = 1670436900
for hour in range(1, 2):
    try:
        applications_bytes_per_interfaces(headers, local_timestamp)
    except Exception:
        print(traceback.format_exc())
        subprocess.call('/home/TVadmin/django_code/analytics_dashboard/dashboard/auth.sh', shell=True)
        filepath = 'tvc-client.cookie'
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
            applications_bytes_per_interfaces(headers, local_timestamp)
    local_timestamp = local_timestamp - 3600