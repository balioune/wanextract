from __future__ import unicode_literals
import requests
from datetime import datetime
from datetime import date
import time
import json
from time import time as timestamp
from apps.home.models import *
import threading
# Get token
authToken = ''
import subprocess
import traceback
import logging

headers = dict()
logging.basicConfig(filename="/home/TVadmin/django_code/wanextract/log/extract_monthly_data.log", format='%(asctime)s %(message)s', filemode='w')

def extract_monthly_data():
    #import logging
    global authToken
    global headers

    def authenticate_api():
        print("Authentication")
        global authToken
        global headers
        #subprocess.Popen(['/home/TVadmin/auth.sh'],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        #subprocess.call('/home/TVadmin/auth.sh')
        filepath = '/home/TVadmin/tvc-client.cookie'
        with open(filepath) as fp:
            line = fp.readline()
            cnt = 1
            while line:
                if len(line.split('\t')) > 1:
                    authToken = line.split('\t')[6].split('\n')[0]
                    print("authToken: ", authToken)
                line = fp.readline()
                cnt += 1

        #headers = dict()
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
    
    def burst_per_interface_hourly(global_headers, interfaceId, DeviceIp, DeviceName, start_time=None, end_time=None):
        logger=logging.getLogger()
        logger.info("XXXXXXXX we are in burst_per_interface_hourly")
        global authToken
        global headers
        logger.info(headers)
        url = 'http://tlspbnflow02/api/v1/perfdata?ViewBy=Time&Metric=InBurst1&Metric=InBurst2&Metric=InBurst3&Metric=InBurst4&Metric=InOther&Metric=OutBurst1&Metric=OutBurst2&Metric=OutBurst3&Metric=OutBurst4&Metric=OutOther&minGranularity=MIN15&grid=true&period=CUSTOM_TIME&autoUpdate=false&startTime={}&endTime={}&nfinterfaceId={}&PortIfType=2&DeviceIp={}&DeviceName=RTRB1SHADU&CollectorId=0'.format(
        start_time, end_time, interfaceId, DeviceIp, DeviceName)
        try:
            response = requests.get(url, headers=global_headers, verify=False)
        except Exception:
            #subprocess.call('/home/TVadmin/django_code/wanextract/auth.sh', shell=True)
            filepath = '/home/TVadmin/tvc-client.cookie'
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
        logger.info(response.text)
        return response.text


    def throughput_per_interface_hourly(global_headers, interfaceId, DeviceIp, DeviceName, start_time=None, end_time=None):
        global authToken
        global headers
        url = 'http://tlspbnflow02/api/v1/trafficanalysis?MetricSpace=uptimenpv&ViewBy=Time&ViewBy=Application&Metric=TotalThroughput&Metric=RxThroughput&Metric=TxThroughput&Metric=InCap&Metric=OutCap&grid=true&OrderBy=TotalThroughput&TopN=5&nfinterfaceId={}&PortIfType=2&DeviceIp={}&DeviceName={}&CollectorId=0&period=CUSTOM_TIME&autoUpdate=false&startTime={}&endTime={}'.format(
        interfaceId, DeviceIp, DeviceName, start_time, end_time)
        try:
            response = requests.get(url, headers=global_headers, verify=False)
        except Exception:
            #subprocess.call('/home/TVadmin/django_code/wanextract/auth.sh', shell=True)
            filepath = '/home/TVadmin/tvc-client.cookie'
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


    def history_function_interfaces_burst(global_headers, var_timestamp):
        logger=logging.getLogger()
        logger.info("Interface.objects.all(): history_function_interfaces_burst")
        logger.info(Interface.objects.all())
        logger.info("XXXXXXXXXXXXXXXXXX We are in function history_function_interfaces_burst") 
        logger.info(global_headers)
        from datetime import datetime
        from apps.home.models import Interface, OutInterfaceBurst, InInterfaceBurst
        local_timestamp = var_timestamp
        timestamp = local_timestamp
        END = str(local_timestamp - 3600).split('.')[0]
        START = str(local_timestamp - 3600 - 3600).split('.')[0]
        logger.info(START)
        logger.info(END)
        try:
            date_en = datetime.fromtimestamp(timestamp).date()
            time_en = datetime.fromtimestamp(timestamp).time()
            logger.info(str(date_en))
            logger.info(str(time_en))
        except Exception:
            logger.info(traceback.format_exc())
        try:
            logger.info(" Filtering all Interface")
            logger.info(Interface.objects.all())
            logger.info(" 5555 Filtering all Interface")
            #logger.info(apps.home.models.Interface.objects.all())
            from apps.home import models
            logger.info(models.Interface.objects.all())
        except Exception:
            logger.info(traceback.format_exc())
            from apps.home import models
            logger.info(models.Interface.objects.all())

        logger.info("XXXX Before Calling burst_per_interface_hourly")
        logger.info(apps.home.models.Interface.objects.all())
        for interface in Interface.objects.all():
            logger.info("Before Calling burst_per_interface_hourly")
            response = burst_per_interface_hourly(global_headers, interface.truview_if_id, interface.deviceIp, interface.deviceName,
                                              str(START) + '000', str(END) + '000')
            logger.info(response)
            response = json.loads(response)
            logger.info(response)
            apps_throughput = throughput_per_interface_hourly(global_headers, interface.truview_if_id, interface.deviceIp,
                                                          interface.deviceName, str(START) + '000', str(END) + '000')
            apps_throughput = json.loads(apps_throughput)
            apps_dict = dict()
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
                    o1=None
                    if Burst4 == 1:
                        print(interface.deviceName, interface.name, OutBurst1, OutBurst2, OutBurst3, OutBurst4)
                        o1 = OutInterfaceBurst(timestamp=timestamp,date=date_en, time=time_en, interface=interface, OutBurst1=OutBurst1,
                                           OutBurst2=OutBurst2, OutBurst3=OutBurst3, OutBurst4=OutBurst4, Burst3=Burst3,
                                           Burst4=Burst4)
                        o1.applications = json.loads(str(apps_dict))
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
                    i1=None
                    if Burst4 == 1:
                        print(interface.deviceName, interface.name, InBurst1, InBurst2, InBurst3, InBurst4)
                        i1 = InInterfaceBurst(timestamp=timestamp,date=date_en, time=time_en, interface=interface, InBurst1=InBurst1,
                                          InBurst2=InBurst2, InBurst3=InBurst3, InBurst4=InBurst4, Burst3=Burst3,
                                          Burst4=Burst4)
                        i1.applications = json.loads(str(apps_dict))
                        i1.save()
            for record in apps_throughput['records']:
                RxThroughput = record['RxThroughput']
                TxThroughput = record['TxThroughput']
                TotalThroughput = record['TotalThroughput']
                if record['RxThroughput'] is None: RxThroughput = 0.0
                if record['TxThroughput'] is None: TxThroughput = 0.0
                if record['TxThroughput'] is None: TxThroughput = 0.0
                if record['Application'] is None:
                    if 'UNKNOWN' in apps_dict.keys():
                        if record['TxThroughput'] is not None: apps_dict['UNKNOWN']['TxThroughput'] = apps_dict['UNKNOWN'][
                                                                                                      'TxThroughput'] + \
                                                                                                  record['TxThroughput']
                        if record['RxThroughput'] is not None: apps_dict['UNKNOWN']['RxThroughput'] = apps_dict['UNKNOWN'][
                                                                                                      'RxThroughput'] + \
                                                                                                  RxThroughput
                        if record['TotalThroughput'] is not None: apps_dict['UNKNOWN']['TotalThroughput'] = \
                    apps_dict['UNKNOWN']['TotalThroughput'] + record['TotalThroughput']
                    else:
                        apps_dict['UNKNOWN'] = {'TxThroughput': TxThroughput,
                                            'RxThroughput': RxThroughput,
                                            'TotalThroughput': TotalThroughput}
                else:
                    if record['Application']['name'] in apps_dict.keys():
                        if record['TxThroughput'] is not None: apps_dict[record['Application']['name']]['TxThroughput'] = \
                        apps_dict[record['Application']['name']]['TxThroughput'] + TxThroughput
                        if record['RxThroughput'] is not None: apps_dict[record['Application']['name']]['RxThroughput'] = \
                    apps_dict[record['Application']['name']]['RxThroughput'] + RxThroughput
                        if record['TotalThroughput'] is not None: apps_dict[record['Application']['name']]['TotalThroughput'] = apps_dict[record['Application']['name']]['TotalThroughput'] + TotalThroughput
                    else:
                        apps_dict[record['Application']['name']] = dict()
                        apps_dict[record['Application']['name']]['TxThroughput'] = TxThroughput
                        apps_dict[record['Application']['name']]['RxThroughput'] = RxThroughput
                        apps_dict[record['Application']['name']]['TotalThroughput'] = TotalThroughput
            for key in apps_dict.keys():
                if (i1 is not None) or (o1 is not None):
                    AppInterfaceThrouput(timestamp=timestamp, date=date_en, time=time_en, interface=interface, inburst=i1, outburst=o1, if_name=interface.truview_if_id,router_name=interface.deviceName, app=key,tx_throuput=apps_dict[key]['TxThroughput'], rx_throuput=apps_dict[key]['RxThroughput'], total_throuput=apps_dict[key]['TotalThroughput'])

    print("CRON: cron.py Extraction Monthly Data")
    #logging.basicConfig(filename="/home/TVadmin/django_code/wanextract/log/extract_monthly_data.log", format='%(asctime)s %(message)s', filemode='w')
    #Let us Create an object
    logger=logging.getLogger()
    #Now we are going to Set the threshold of logger to DEBUG
    logger.setLevel(logging.DEBUG)
    #some messages to test
    logger.debug("This is just a harmless debug message")
    logger.info("This is just an information for you")
    logger.warning("OOPS!!!Its a Warning")
    logger.error("Have you try to divide a number by zero")
    logger.critical("The Internet is not working....")
    logger.info("TEST GETTING Interface")
    logger.info("NEWWWWWWWWW Interface.objects.all(): history_function_interfaces_burst")
    try:
        logger.info(Site.objects.all())
        logger.info(Interface.objects.all())
    except Exception:
        print(traceback.format_exc())
    #subprocess.Popen(['/home/TVadmin/auth.sh'],shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #subprocess.call('/home/TVadmin/auth.sh', shell=True)
    filepath = '/home/TVadmin/tvc-client.cookie'
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
    logger.debug(authToken)
    logger.debug(headers)
    #headers = dict()
    headers['Cookie'] = 'authToken=' + authToken
    headers['User-Agent'] = 'curl/7.29.0'
    headers['Accept'] = '*/*'
    local_timestamp = 1672527600
    logger.debug(local_timestamp)
    for hour in range(1, 5):
        try:
            logger.debug("BEFORE : history_function_interfaces_burst")
            history_function_interfaces_burst(headers, local_timestamp)
        except Exception:
            print(traceback.format_exc())
            #subprocess.call('/home/TVadmin/django_code/wanextract/auth.sh', shell=True)
            filepath = '/home/TVadmin/tvc-client.cookie'
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

