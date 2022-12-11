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

def pupulate_application(headers):
    url = 'http://tlspbnflow02/api/v1/config/collection/domain/11/Applications?start=0&limit=10000&sort=appName'
    response = requests.get(url, headers=headers, verify=False)
    print(response)
    response = json.loads(response.text)
    for data in response['data']:
        print("############")
        print(data)
        app = Application(truview_app_id=data['appId'], name=data['appName'])
        app.save()

def burst_per_interface_hourly(headers, interfaceId, DeviceIp, DeviceName, start_time=None, end_time=None):
    url = 'http://tlspbnflow02/api/v1/perfdata?ViewBy=Time&Metric=InBurst1&Metric=InBurst2&Metric=InBurst3&Metric=InBurst4&Metric=InOther&Metric=OutBurst1&Metric=OutBurst2&Metric=OutBurst3&Metric=OutBurst4&Metric=OutOther&minGranularity=MIN15&grid=true&period=CUSTOM_TIME&autoUpdate=false&startTime={}&endTime={}&nfinterfaceId={}&PortIfType=2&DeviceIp={}&DeviceName=RTRB1SHADU&CollectorId=0'.format(
        start_time, end_time, interfaceId, DeviceIp, DeviceName)
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


def throughput_per_interface_hourly(headers, interfaceId, DeviceIp, DeviceName, start_time=None, end_time=None):
    url = 'http://tlspbnflow02/api/v1/trafficanalysis?MetricSpace=uptimenpv&ViewBy=Time&ViewBy=Application&Metric=TotalThroughput&Metric=RxThroughput&Metric=TxThroughput&Metric=InCap&Metric=OutCap&grid=true&OrderBy=TotalThroughput&TopN=5&nfinterfaceId={}&PortIfType=2&DeviceIp={}&DeviceName={}&CollectorId=0&period=CUSTOM_TIME&autoUpdate=false&startTime={}&endTime={}'.format(
        interfaceId, DeviceIp, DeviceName, start_time, end_time)
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


def history_function_interfaces_burst(headers, var_timestamp):
    from datetime import datetime
    local_timestamp = var_timestamp
    timestamp = local_timestamp
    # END  = str(local_timestamp).split('.')[0]
    # START = str(local_timestamp - 3600).split('.')[0]
    END = str(local_timestamp - 3600).split('.')[0]
    START = str(local_timestamp - 3600 - 3600).split('.')[0]
    print("START END", START, END)
    try:
        date_en = datetime.fromtimestamp(timestamp).date()
        time_en = datetime.fromtimestamp(timestamp).time()
        print("DATE, TIME", str(date_en), str(time_en))
    except Exception:
        print(traceback.format_exc())
    for interface in Interface.objects.all():
        response = burst_per_interface_hourly(headers, interface.truview_if_id, interface.deviceIp, interface.deviceName,
                                              str(START) + '000', str(END) + '000')
        response = json.loads(response)
        apps_throughput = throughput_per_interface_hourly(headers, interface.truview_if_id, interface.deviceIp,
                                                          interface.deviceName, str(START) + '000', str(END) + '000')
        apps_throughput = json.loads(apps_throughput)
        apps_dict = dict()
        for record in apps_throughput['records']:
            if record['Application'] is None:
                if 'UNKNOWN' in apps_dict.keys():
                    if record['TxThroughput'] is not None: apps_dict['UNKNOWN']['TxThroughput'] = apps_dict['UNKNOWN'][
                                                                                                      'TxThroughput'] + \
                                                                                                  record['TxThroughput']
                    if record['RxThroughput'] is not None: apps_dict['UNKNOWN']['RxThroughput'] = apps_dict['UNKNOWN'][
                                                                                                      'RxThroughput'] + \
                                                                                                  record['RxThroughput']
                    if record['TotalThroughput'] is not None: apps_dict['UNKNOWN']['TotalThroughput'] = \
                    apps_dict['UNKNOWN']['TotalThroughput'] + record['TotalThroughput']
                else:
                    apps_dict['UNKNOWN'] = {'TxThroughput': record['TxThroughput'],
                                            'RxThroughput': record['RxThroughput'],
                                            'TotalThroughput': record['TotalThroughput']}
            else:
                if record['Application']['name'] in apps_dict.keys():
                    if record['TxThroughput'] is not None: apps_dict[record['Application']['name']]['TxThroughput'] = \
                    apps_dict[record['Application']['name']]['TxThroughput'] + record['TxThroughput']
                    if record['RxThroughput'] is not None: apps_dict[record['Application']['name']]['RxThroughput'] = \
                    apps_dict[record['Application']['name']]['RxThroughput'] + record['RxThroughput']
                    if record['TotalThroughput'] is not None: apps_dict[record['Application']['name']][
                        'TotalThroughput'] = apps_dict[record['Application']['name']]['TotalThroughput'] + record[
                        'TotalThroughput']
                else:
                    apps_dict[record['Application']['name']] = dict()
                    apps_dict[record['Application']['name']]['TxThroughput'] = record['TxThroughput']
                    apps_dict[record['Application']['name']]['RxThroughput'] = record['RxThroughput']
                    apps_dict[record['Application']['name']]['TotalThroughput'] = record['TotalThroughput']
        if "records" in response.keys():
            for app in response['records']:
                OutBurst1 = 0.0
                OutBurst2 = 0.0
                OutBurst3 = 0.0
                OutBurst4 = 0.0
                Burst1 = 0
                Burst2 = 0
                Burst3 = 0
                Burst4 = 0
                if app['OutBurst1'] is not None: OutBurst1 = app['OutBurst1']
                if app['OutBurst2'] is not None: OutBurst2 = app['OutBurst2']
                if app['OutBurst3'] is not None: OutBurst3 = app['OutBurst3']
                if app['OutBurst4'] is not None: OutBurst4 = app['OutBurst4']
                if OutBurst3 >= 60: Burst3 = 1
                if OutBurst4 >= 80: Burst4 = 1
                if Burst4 == 1:
                    print(interface.deviceName, interface.name, OutBurst1, OutBurst2, OutBurst3, OutBurst4)
                    o1 = OutInterfaceBurst(date=date_en, time=time_en, interface=interface, OutBurst1=OutBurst1,
                                           OutBurst2=OutBurst2, OutBurst3=OutBurst3, OutBurst4=OutBurst4, Burst3=Burst3,
                                           Burst4=Burst4)
                    o1.applications = str(apps_dict)
                    o1.save()
        if "records" in response.keys():
            for app in response['records']:
                InBurst1 = 0.0
                InBurst2 = 0.0
                InBurst3 = 0.0
                InBurst4 = 0.0
                Burst1 = 0
                Burst2 = 0
                Burst3 = 0
                Burst4 = 0
                if app['InBurst1'] is not None: InBurst1 = app['InBurst1']
                if app['InBurst2'] is not None: InBurst2 = app['InBurst2']
                if app['InBurst3'] is not None: InBurst3 = app['InBurst3']
                if app['InBurst4'] is not None: InBurst4 = app['InBurst4']
                if InBurst3 > 60: Burst3 = 1
                if InBurst4 > 80: Burst4 = 1
                if Burst4 == 1:
                    print(interface.deviceName, interface.name, InBurst1, InBurst2, InBurst3, InBurst4)
                    i1 = InInterfaceBurst(date=date_en, time=time_en, interface=interface, InBurst1=InBurst1,
                                          InBurst2=InBurst2, InBurst3=InBurst3, InBurst4=InBurst4, Burst3=Burst3,
                                          Burst4=Burst4)
                    i1.applications = str(apps_dict)
                    i1.save()


from datetime import datetime
from time import time as timestamp
import traceback

local_timestamp = timestamp()
# local_timestamp = 1670666314
for hour in range(1, 3000):
    try:
        history_function_interfaces_burst(headers, local_timestamp)
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
        history_function_interfaces_burst(headers, local_timestamp)
        print(traceback.format_exc())
    local_timestamp = local_timestamp - 3600

"""
"""
def application_per_interface_hourly(headers, interfaceId, DeviceIp, DeviceName, start_time=None, end_time=None):
    url = 'http://tlspbnflow02/api/v1/trafficanalysis?MetricSpace=uptimenpv&ViewBy=Time&ViewBy=Application&Metric=TotalThroughput&Metric=RxThroughput&Metric=TxThroughput&Metric=InCap&Metric=OutCap&grid=true&OrderBy=TotalThroughput&TopN=5&nfinterfaceId={}&PortIfType=2&DeviceIp={}&DeviceName={}CollectorId=0&period=CUSTOM_TIME&autoUpdate=false&startTime={}&endTime={}'.format(
        interfaceId, DeviceIp, DeviceName, start_time, end_time)
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


def history_function_interfaces_applications(headers, var_timestamp):
    from datetime import datetime
    local_timestamp = var_timestamp
    timestamp = local_timestamp
    END = str(local_timestamp).split('.')[0]
    START = str(local_timestamp - 3600).split('.')[0]
    TEAMS_TX = 0.0
    TEAMS_RX = 0.0
    HTTPS_TX = 0.0
    HTTPS_RX = 0.0
    try:
        date_en = datetime.fromtimestamp(timestamp).date()
        time_en = datetime.fromtimestamp(timestamp).time()
        print(str(date_en), str(time_en))
        print(str(datetime.fromtimestamp(local_timestamp - 3600).time()),
              str(datetime.fromtimestamp(local_timestamp).time()))
    except Exception:
        print(traceback.format_exc())
    for interface in Interface.objects.all():
        response = application_per_interface_hourly(interface.truview_if_id, interface.deviceIp, interface.deviceName,
                                                    str(START) + '000', str(END) + '000')
        response = json.loads(response)
        if "records" in response.keys():
            for app in response['records']:
                RxThroughput = app['RxThroughput']
                TxThroughput = app['TxThroughput']
                if app['RxThroughput'] is None: RxThroughput = 0.0
                if app['TxThroughput'] is None: TxThroughput = 0.0
                app_obj = None
                if app['Application'] is not None:
                    if app['Application']['name'] == 'HTTPS' and interface.deviceName == 'RTRB2SAODD':
                        HTTPS_TX = HTTPS_TX + TxThroughput
                        HTTPS_RX = HTTPS_RX + RxThroughput
                    if app['Application']['name'] == 'O365_Teams' and interface.deviceName == 'RTRB2SAODD':
                        TEAMS_TX = TEAMS_TX + TxThroughput
                        TEAMS_RX = TEAMS_RX + RxThroughput
                    # print("NOT NONE", interface.deviceName, interface.name, app['Application'])
                    # print(app)
                    # app_obj = Application.objects.get(truview_app_id=app['Application']['id'],name=app['Application']['name'])
                    o1 = AppInterfaceOut(date=date_en, time=time_en, interface=interface,
                                         app=app['Application']['name'], tx_throuput=TxThroughput)
                    # o1.save()
                    i1 = AppInterfaceIn(date=date_en, time=time_en, interface=interface, app=app['Application']['name'],
                                        rx_throuput=RxThroughput)
                    # i1.save()
                else:
                    # print("NONE", interface.deviceName, interface.name, app['Application'])
                    # print(app)
                    o1 = AppInterfaceOut(date=date_en, time=time_en, interface=interface, tx_throuput=TxThroughput,
                                         app='Other')
                    # o1.save()
                    i1 = AppInterfaceIn(date=date_en, time=time_en, interface=interface, rx_throuput=RxThroughput,
                                        app='Other')
                    # i1.save()
    print("HTTPS_TX, HTTPS_RX, TEAMS_TX, TEAMS_RX")
    print(HTTPS_TX, HTTPS_RX, TEAMS_TX, TEAMS_RX)


from datetime import datetime
from time import time as timestamp
import traceback

local_timestamp = timestamp()
local_timestamp = 1670440507
for hour in range(1, 2):
    try:
        history_function_interfaces_applications(headers, local_timestamp)
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
            print(traceback.format_exc())
    local_timestamp = local_timestamp - 3600