"""
import datetime
#from dashboard.models import *
from extract.models import *
for burst in InInterfaceBurst.objects.all():
   burst.delete()
"""

from __future__ import unicode_literals

import requests
from datetime import datetime
from datetime import date
import time
import json
from time import time as timestamp
# from dashboard.models import *
from extract.models import *
import threading

"""
WAIT_SECONDS = 60
DOMAINS_DICT = dict()
SITES_DOMAIN_DICT = dict()

local_timestamp = timestamp()
START_TIME = str(local_timestamp).split('.')[0] + '000'
END_TIME = str(local_timestamp + 3600).split('.')[0] + '000'
"""

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
            # authToken = line.split('\t')[6]
            authToken = line.split('\t')[6].split('\n')[0]
            print("authToken: ", authToken)
        line = fp.readline()
        cnt +=  # Authentication
# Variables
jsondata = list()

headers = dict()
headers['Cookie'] = 'authToken=' + authToken
headers['User-Agent'] = 'curl/7.29.0'
headers['Accept'] = '*/*'

# URL: Domains
url_domains = 'http://tlspbnflow02/api/v1/config/collection/json/system/Domains?'


def app_usage_per_interface(interfaceId, DeviceIp, DeviceName):
    url = 'http://tlspbnflow02/api/v1/trafficanalysis?ViewBy=Application&ViewBy=ApplicationClass&Metric=TotalUtilization&Metric=TotalThroughput&Metric=TotalPPS&Metric=TotalFPS&Metric=InCap&Metric=OutCap&grid=true&CalcOthers=false&rowLimit=10000&pageAtSource=true&passSort=true&raw=true&start=0&limit=10&OrderBy=TotalUtilization&period=LAST_60_MIN&autoUpdate=false&nfinterfaceId={}&PortIfType=2&DeviceIp={}&DeviceName={}&CollectorId=0&SortColumn=TotalUtilization&SortDirection=DESC'.format(
        interfaceId, DeviceIp, DeviceName)
    response = requests.get(url, headers=headers, verify=False)
    return response.text


def app_usage_per_interface_start_end(interfaceId, DeviceIp, DeviceName, start, end):
    url = 'http://tlspbnflow02/api/v1/trafficanalysis?ViewBy=Application&ViewBy=ApplicationClass&Metric=TotalUtilization&Metric=TotalThroughput&Metric=TotalPPS&Metric=TotalFPS&Metric=InCap&Metric=OutCap&grid=true&CalcOthers=false&rowLimit=10000&pageAtSource=true&passSort=true&raw=true&start=0&limit=10&OrderBy=TotalUtilization&period=CUSTOM_TIME&startTime={}&endTime={}&autoUpdate=false&nfinterfaceId={}&PortIfType=2&DeviceIp={}&DeviceName={}&CollectorId=0&SortColumn=TotalUtilization&SortDirection=DESC'.format(
        start, end, interfaceId, DeviceIp, DeviceName)
    response = requests.get(url, headers=headers, verify=False)
    return response.text


def burst_per_interface(interfaceId, DeviceIp, DeviceName):
    # url = 'http://tlspbnflow02/api/v1/trafficanalysis?ViewBy=Application&ViewBy=ApplicationClass&Metric=TotalUtilization&Metric=TotalThroughput&Metric=TotalPPS&Metric=TotalFPS&Metric=InCap&Metric=OutCap&grid=true&CalcOthers=false&rowLimit=10000&pageAtSource=true&passSort=true&raw=true&start=0&limit=10&OrderBy=TotalUtilization&period=LAST_60_MIN&autoUpdate=false&nfinterfaceId={}&PortIfType=2&DeviceIp={}&DeviceName={}&CollectorId=0&SortColumn=TotalUtilization&SortDirection=DESC'.format(interfaceId, DeviceIp, DeviceName)
    # url = 'http://tlspbnflow02/api/v1/perfdata?ViewBy=Time&Metric=InBurst1&Metric=InBurst2&Metric=InBurst3&Metric=InBurst4&Metric=InOther&Metric=OutBurst1&Metric=OutBurst2&Metric=OutBurst3&Metric=OutBurst4&Metric=OutOther&minGranularity=MIN15&grid=true&period=LAST_60_MIN&autoUpdate=false&nfinterfaceId={}&PortIfType=2&DeviceIp={}&DeviceName={}&CollectorId=0'.format(interfaceId, DeviceIp, DeviceName)
    url = 'http://tlspbnflow02/api/v1/perfdata?ViewBy=Time&Metric=InBurst1&Metric=InBurst2&Metric=InBurst3&Metric=InBurst4&Metric=InOther&Metric=OutBurst1&Metric=OutBurst2&Metric=OutBurst3&Metric=OutBurst4&Metric=OutOther&minGranularity=MIN15&grid=true&period=CUSTOM_TIME&autoUpdate=false&startTime=1663000920000&endTime=1663263720000&nfinterfaceId={}&PortIfType=2&DeviceIp={}&DeviceName=RTRB1SHADU&CollectorId=0'.format(
        interfaceId, DeviceIp, DeviceName)
    response = requests.get(url, headers=headers, verify=False)
    return response.text


def burst_per_interface_hourly(interfaceId, DeviceIp, DeviceName, start_time=None, end_time=None):
    url = 'http://tlspbnflow02/api/v1/perfdata?ViewBy=Time&Metric=InBurst1&Metric=InBurst2&Metric=InBurst3&Metric=InBurst4&Metric=InOther&Metric=OutBurst1&Metric=OutBurst2&Metric=OutBurst3&Metric=OutBurst4&Metric=OutOther&minGranularity=MIN15&grid=true&period=CUSTOM_TIME&autoUpdate=false&startTime={}&endTime={}&nfinterfaceId={}&PortIfType=2&DeviceIp={}&DeviceName=RTRB1SHADU&CollectorId=0'.format(
        start_time, end_time, interfaceId, DeviceIp, DeviceName)
    response = requests.get(url, headers=headers, verify=False)
    return response.text


def burst_per_interface_september(interfaceId, DeviceIp, DeviceName, start_time=None, end_time=None):
    # url = 'http://tlspbnflow02/api/v1/perfdata?ViewBy=Time&Metric=InBurst1&Metric=InBurst2&Metric=InBurst3&Metric=InBurst4&Metric=InOther&Metric=OutBurst1&Metric=OutBurst2&Metric=OutBurst3&Metric=OutBurst4&Metric=OutOther&minGranularity=MIN15&grid=true&period=CUSTOM_TIME&autoUpdate=false&startTime={}&endTime={}&nfinterfaceId={}&PortIfType=2&DeviceIp={}&DeviceName=RTRB1SHADU&CollectorId=0'.format(start_time, end_time, interfaceId, DeviceIp, DeviceName)
    url = 'http://tlspbnflow02/api/v1/perfdata?ViewBy=Time&Metric=InBurst1&Metric=InBurst2&Metric=InBurst3&Metric=InBurst4&Metric=InOther&Metric=OutBurst1&Metric=OutBurst2&Metric=OutBurst3&Metric=OutBurst4&Metric=OutOther&minGranularity=MIN15&grid=true&period=CUSTOM_TIME&autoUpdate=false&startTime=1662039720000&endTime=1664635320000&nfinterfaceId={}&PortIfType=2&DeviceIp={}&DeviceName={}&CollectorId=0'.format(
        interfaceId, DeviceIp, DeviceName)
    response = requests.get(url, headers=headers, verify=False)
    return response.text


def periodic_function_app_usage():
    response = requests.get(url_domains, headers=headers, verify=False)
    url_interfaces_by_domain = 'http://tlspbnflow02/api/v1/perfdata?OrderBy=TxUtilization&dir=DESC&ViewBy=Interface&Metric=RxUtilization&Metric=TxUtilization&Metric=RxThroughput&Metric=TxThroughput&Metric=RxPPS&Metric=TxPPS&Metric=Availability&Metric=CurrentStatus&wait=false&rowLimit=100000&searchFields=name,Interface.description&GroupSortColumn=&GroupSortDir=ASC&start=0&limit=10000&search=&period=LAST_60_MIN&autoUpdate=false'
    response = requests.get(url_interfaces_by_domain, headers=headers, verify=False)
    interfaces = json.loads(response.text)
    for interface in interfaces['records']:
        response = app_usage_per_interface(interface['Interface']['id'], interface['Interface']['deviceIp'],
                                           interface['Interface']['deviceName'])
        response = json.loads(response)
        if "chart" in response.keys():
            print(response)
            for app in response['records']:
                o1 = Interface(in_bandwidth=0.0, date=date.today().strftime("%d/%m/%Y"),
                               time=datetime.now().strftime("%H:%M:%S"), site_name=interface['Site'][0]['name'],
                               router=interface['Device']['name'], interface=interface['Interface']['name'],
                               description=interface['Interface']['description'],
                               application=app['Application']['name'],
                               app_description=app['Application']['description'], out_bandwidth=app['TotalUtilization'],
                               throughput=app['TotalThroughput'])
                o1.save()
                print(o1)


def periodic_function_interface_burst_out_september(interfaces):
    # url_interfaces_by_domain = 'http://tlspbnflow02/api/v1/perfdata?OrderBy=TxUtilization&dir=DESC&ViewBy=Interface&Metric=RxUtilization&Metric=TxUtilization&Metric=RxThroughput&Metric=TxThroughput&Metric=RxPPS&Metric=TxPPS&Metric=Availability&Metric=CurrentStatus&wait=false&rowLimit=100000&searchFields=name,Interface.description&GroupSortColumn=&GroupSortDir=ASC&start=0&limit=10000&search=&period=LAST_60_MIN&autoUpdate=false'
    # response = requests.get(url_interfaces_by_domain, headers=headers, verify=False)
    # interfaces = json.loads(response.text)
    # print(interfaces['records'])
    date_en = str(datetime.fromtimestamp(timestamp)).split(' ')[0].split('-')
    date_fr = date_en[2] + '/' + date_en[1] + '/' + date_en[0]
    time_fr = str(datetime.fromtimestamp(timestamp)).split(' ')[1]
    print(date_fr, time_fr)
    for interface in interfaces['records']:
        # response = burst_per_interface(interface['Interface']['id'], interface['Interface']['deviceIp'], interface['Interface']['deviceName'])
        response = burst_per_interface_hourly(interface['Interface']['id'], interface['Interface']['deviceIp'],
                                              interface['Interface']['deviceName'], str(START) + '000',
                                              str(END) + '000')
        response = json.loads(response)
        # print(response)
        if "records" in response.keys():
            # print(response)
            # time.sleep(5)
            for app in response['records']:
                # print(app['OutBurst1'],app['OutBurst2'],app['OutBurst3'],app['OutBurst4'])
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
                if OutBurst1 > 20: Burst1 = 1
                if OutBurst2 > 20: Burst2 = 1
                if OutBurst3 > 20: Burst3 = 1
                if OutBurst4 > 20: Burst4 = 1
                if Burst3 == 1 or Burst4 == 1:
                    print(OutBurst1, OutBurst2, OutBurst3, OutBurst4)
                    o1 = OutInterfaceBurst(date=date_fr, time=time_fr, site_name=interface['Site'][0]['name'],
                                           router=interface['Device']['name'], interface=interface['Interface']['name'],
                                           OutBurst1=OutBurst1, OutBurst2=OutBurst2, OutBurst3=OutBurst3,
                                           OutBurst4=OutBurst4, Burst1=Burst1, Burst2=Burst2, Burst3=Burst3,
                                           Burst4=Burst4)
                    o1.save()


def periodic_function_interface_burst_out_start_end(interfaces, START, END, timestamp):
    # url_interfaces_by_domain = 'http://tlspbnflow02/api/v1/perfdata?OrderBy=TxUtilization&dir=DESC&ViewBy=Interface&Metric=RxUtilization&Metric=TxUtilization&Metric=RxThroughput&Metric=TxThroughput&Metric=RxPPS&Metric=TxPPS&Metric=Availability&Metric=CurrentStatus&wait=false&rowLimit=100000&searchFields=name,Interface.description&GroupSortColumn=&GroupSortDir=ASC&start=0&limit=10000&search=&period=LAST_60_MIN&autoUpdate=false'
    # response = requests.get(url_interfaces_by_domain, headers=headers, verify=False)
    # interfaces = json.loads(response.text)
    # print(interfaces['records'])
    date_en = str(datetime.fromtimestamp(timestamp)).split(' ')[0].split('-')
    date_fr = date_en[2] + '/' + date_en[1] + '/' + date_en[0]
    time_fr = str(datetime.fromtimestamp(timestamp)).split(' ')[1]
    print(date_fr, time_fr)
    for interface in interfaces['records']:
        # response = burst_per_interface(interface['Interface']['id'], interface['Interface']['deviceIp'], interface['Interface']['deviceName'])
        response = burst_per_interface_hourly(interface['Interface']['id'], interface['Interface']['deviceIp'],
                                              interface['Interface']['deviceName'], str(START) + '000',
                                              str(END) + '000')
        response = json.loads(response)
        # print(response)
        if "records" in response.keys():
            # print(response)
            # time.sleep(5)
            for app in response['records']:
                # print(app['OutBurst1'],app['OutBurst2'],app['OutBurst3'],app['OutBurst4'])
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
                if OutBurst1 > 20: Burst1 = 1
                if OutBurst2 > 20: Burst2 = 1
                if OutBurst3 > 20: Burst3 = 1
                if OutBurst4 > 20: Burst4 = 1
                if Burst3 == 1 or Burst4 == 1:
                    print(OutBurst1, OutBurst2, OutBurst3, OutBurst4)
                    o1 = OutInterfaceBurst(date=date_fr, time=time_fr, site_name=interface['Site'][0]['name'],
                                           router=interface['Device']['name'], interface=interface['Interface']['name'],
                                           OutBurst1=OutBurst1, OutBurst2=OutBurst2, OutBurst3=OutBurst3,
                                           OutBurst4=OutBurst4, Burst1=Burst1, Burst2=Burst2, Burst3=Burst3,
                                           Burst4=Burst4)
                    o1.save()


def periodic_function_interface_burst_in_start_end(interfaces, START, END, timestamp):
    # url_interfaces_by_domain = 'http://tlspbnflow02/api/v1/perfdata?OrderBy=TxUtilization&dir=DESC&ViewBy=Interface&Metric=RxUtilization&Metric=TxUtilization&Metric=RxThroughput&Metric=TxThroughput&Metric=RxPPS&Metric=TxPPS&Metric=Availability&Metric=CurrentStatus&wait=false&rowLimit=100000&searchFields=name,Interface.description&GroupSortColumn=&GroupSortDir=ASC&start=0&limit=10000&search=&period=LAST_60_MIN&autoUpdate=false'
    # response = requests.get(url_interfaces_by_domain, headers=headers, verify=False)
    # interfaces = json.loads(response.text)
    # print(interfaces['records'])
    date_en = str(datetime.fromtimestamp(timestamp)).split(' ')[0].split('-')
    date_fr = date_en[2] + '/' + date_en[1] + '/' + date_en[0]
    time_fr = str(datetime.fromtimestamp(timestamp)).split(' ')[1]
    print(date_fr, time_fr)
    for interface in interfaces['records']:
        # response = burst_per_interface(interface['Interface']['id'], interface['Interface']['deviceIp'], interface['Interface']['deviceName'])
        response = burst_per_interface_hourly(interface['Interface']['id'], interface['Interface']['deviceIp'],
                                              interface['Interface']['deviceName'], str(START) + '000',
                                              str(END) + '000')
        response = json.loads(response)
        # print(response)
        if "records" in response.keys():
            # print(response)
            # time.sleep(5)
            for app in response['records']:
                # print(app['OutBurst1'],app['OutBurst2'],app['OutBurst3'],app['OutBurst4'])
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
                if InBurst1 > 20: Burst1 = 1
                if InBurst2 > 20: Burst2 = 1
                if InBurst3 > 20: Burst3 = 1
                if InBurst4 > 20: Burst4 = 1
                if Burst3 == 1 or Burst4 == 1:
                    print(InBurst1, InBurst2, InBurst3, InBurst4)
                    o1 = InInterfaceBurst(date=date_fr, time=time_fr, site_name=interface['Site'][0]['name'],
                                          router=interface['Device']['name'], interface=interface['Interface']['name'],
                                          InBurst1=InBurst1, InBurst2=InBurst2, InBurst3=InBurst3, InBurst4=InBurst4,
                                          Burst1=Burst1, Burst2=Burst2, Burst3=Burst3, Burst4=Burst4)
                    o1.save()


def periodic_function_app_usage_start_end(START, END, timestamp):
    date_en = str(datetime.fromtimestamp(timestamp)).split(' ')[0].split('-')
    date_fr = date_en[2] + '/' + date_en[1] + '/' + date_en[0]
    time_fr = str(datetime.fromtimestamp(timestamp)).split(' ')[1]
    print(date_fr, time_fr)
    url_interfaces_by_domain = 'http://tlspbnflow02/api/v1/perfdata?OrderBy=TxUtilization&dir=DESC&ViewBy=Interface&Metric=RxUtilization&Metric=TxUtilization&Metric=RxThroughput&Metric=TxThroughput&Metric=RxPPS&Metric=TxPPS&Metric=Availability&Metric=CurrentStatus&wait=false&rowLimit=100000&searchFields=name,Interface.description&GroupSortColumn=&GroupSortDir=ASC&start=0&limit=10000&search=&period=LAST_60_MIN&autoUpdate=false'
    response = requests.get(url_interfaces_by_domain, headers=headers, verify=False)
    interfaces = json.loads(response.text)
    for interface in interfaces['records']:
        # print(interface)
        # response = app_usage_per_interface(interface['Interface']['id'], interface['Interface']['deviceIp'], interface['Interface']['deviceName'])
        response = app_usage_per_interface_start_end(START, END, interface['Interface']['id'],
                                                     interface['Interface']['deviceIp'],
                                                     interface['Interface']['deviceName'])
        response = json.loads(response)
        if "chart" in response.keys():
            # print(response)
            for app in response['records']:
                dictdata = dict()
                dictdata['SITE_NAME'] = interface['Site'][0]['name']
                dictdata['ROUTER'] = interface['Device']['name']
                dictdata['INTERFACE'] = interface['Interface']['name']
                dictdata['DESCRIPTION'] = interface['Interface']['description']
                dictdata['APPLICATION'] = app['Application']['name']
                dictdata['APP_NAME'] = app['Application']['description']
                dictdata['USAGE'] = app['TotalUtilization']
                dictdata['TotalThroughput'] = app['TotalThroughput']
                jsondata.append(dictdata)


"""
EXPORT OUTINTERFACE
"""
from datetime import datetime
from time import time as timestamp

local_timestamp = timestamp()
# 01012022
# local_timestamp = 1664618586
# local_timestamp = 1669381030
local_timestamp = 1667548630
url_interfaces_by_domain = 'http://tlspbnflow02/api/v1/perfdata?OrderBy=TxUtilization&dir=DESC&ViewBy=Interface&Metric=RxUtilization&Metric=TxUtilization&Metric=RxThroughput&Metric=TxThroughput&Metric=RxPPS&Metric=TxPPS&Metric=Availability&Metric=CurrentStatus&wait=false&rowLimit=100000&searchFields=name,Interface.description&GroupSortColumn=&GroupSortDir=ASC&start=0&limit=10000&search=&period=LAST_60_MIN&autoUpdate=false'
response = requests.get(url_interfaces_by_domain, headers=headers, verify=False)
interfaces = json.loads(response.text)
print(interfaces)
for hour in range(1, 3000):
    # END_TIME  = str(local_timestamp).split('.')[0] + '000'
    # START_TIME = str(local_timestamp - 262800).split('.')[0] + '000'
    END_TIME = str(local_timestamp).split('.')[0]
    START_TIME = str(local_timestamp - 3600).split('.')[0]
    local_timestamp = local_timestamp - 3600
    try:
        periodic_function_interface_burst_out_start_end(interfaces, START_TIME, END_TIME, local_timestamp)
    except Exception:
        pass
    try:
        periodic_function_interface_burst_in_start_end(interfaces, START_TIME, END_TIME, local_timestamp)
    except Exception:
        pass

"""
"""
from datetime import datetime
from time import time as timestamp

local_timestamp = timestamp()
# 01012022
# local_timestamp = 1664618586
url_interfaces_by_domain = 'http://tlspbnflow02/api/v1/perfdata?OrderBy=TxUtilization&dir=DESC&ViewBy=Interface&Metric=RxUtilization&Metric=TxUtilization&Metric=RxThroughput&Metric=TxThroughput&Metric=RxPPS&Metric=TxPPS&Metric=Availability&Metric=CurrentStatus&wait=false&rowLimit=100000&searchFields=name,Interface.description&GroupSortColumn=&GroupSortDir=ASC&start=0&limit=10000&search=&period=LAST_60_MIN&autoUpdate=false'
response = requests.get(url_interfaces_by_domain, headers=headers, verify=False)
interfaces = json.loads(response.text)
print(interfaces)
for hour in range(1, 2300):
    # END_TIME  = str(local_timestamp).split('.')[0] + '000'
    # START_TIME = str(local_timestamp - 262800).split('.')[0] + '000'
    END_TIME = str(local_timestamp).split('.')[0]
    START_TIME = str(local_timestamp - 3600).split('.')[0]
    local_timestamp = local_timestamp - 3600
    periodic_function_interface_burst_out_start_end(interfaces, START_TIME, END_TIME, local_timestamp)
    periodic_function_interface_burst_in_start_end(interfaces, START_TIME, END_TIME, local_timestamp)
    # periodic_function_app_usage_start_end(START_TIME, END_TIME, local_timestamp)

print(jsondata)

with open('new_application_usage' + str('10102022') + '.json', 'w') as f:
    json.dump(jsondata, f, indent=2, cls=DecimalEncoder)

"""
GET SITES
url_interfaces_by_domain = 'http://127.0.0.1/api/v1/config/collection/json/domain/11/Sites'
response = requests.get(url_interfaces_by_domain, headers=headers, verify=False)
interfaces = json.loads(response.text)
print(json.dumps(interfaces, indent=2))
"""
url_interfaces_by_domain = 'http://127.0.0.1/api/v1/config/collection/json/domain/11/Sites'
response = requests.get(url_interfaces_by_domain, headers=headers, verify=False)
sites = json.loads(response.text)
SITES_DICT = dict()
for site in sites:
    # print(site['tags']['ZoneGeo'])
    # SITES_DICT[site['siteName']] = site['tags']['ZoneGeo']
    SITES_DICT[str(site['siteName'])] = str(site['tags']['ZoneGeo'])

for burst in OutInterfaceBurst.objects.all():
    burst.zonegeo = str(SITES_DICT[burst.site_name])
    # print(ZoneGeo)
    burst.save()
    print(burst.zonegeo, burst.site_name)

for burst in OutInterfaceBurst.objects.all():
    print(burst.site_name, burst.zonegeo)

# periodic_function_app_usage()

# periodic_function_interface_burst()

Burst1 = Burst1, Burst2 = Burst2, Burst3 = Burst3, Burst4 = Burst4

"""
EXPORT OUTINTERFACE DATA
"""
from decimal import *
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


import datetime
# from dashboard.models import *
from extract.models import *
import json

jsondata = list()
for burst in OutInterfaceBurst.objects.all():
    dictdata = dict()
    dictdata['ZoneGeo'] = burst.zonegeo
    dictdata['DATE'] = burst.date
    dictdata['HEURE'] = burst.time
    dictdata['SITE_NAME'] = burst.site_name
    dictdata['ROUTER'] = burst.router
    dictdata['INTERFACE'] = burst.interface
    dictdata['OutBurst1'] = burst.OutBurst1
    dictdata['OutBurst2'] = burst.OutBurst2
    dictdata['OutBurst3'] = burst.OutBurst3
    dictdata['OutBurst4'] = burst.OutBurst4
    dictdata['Burst1'] = burst.Burst1
    dictdata['Burst2'] = burst.Burst2
    dictdata['Burst3'] = burst.Burst3
    dictdata['Burst4'] = burst.Burst4
    jsondata.append(dictdata)

with open('interfaces_out_burst' + str('10102022') + '.json', 'w') as f:
    json.dump(jsondata, f, indent=2)

with open('interfaces_out_burst' + str('11102022') + '.json', 'w') as f:
    json.dump(jsondata, f, indent=2, cls=DecimalEncoder)
"""
END EXPORT OUTINTERFACE DATA
"""
