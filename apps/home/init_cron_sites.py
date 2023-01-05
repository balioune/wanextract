from __future__ import unicode_literals
import requests
from datetime import datetime
from datetime import date
import time
import json
from time import time as timestamp
from apps.home.models import Site, Interface, Router
import threading
import subprocess
import traceback

headers = dict()
headers['User-Agent'] = 'curl/7.29.0'
headers['Accept'] = '*/*'

"""
INTERFACE BURST
"""
def burst_per_interface_hourly(interfaceId, DeviceIp, DeviceName, start_time=None, end_time=None):
   url = 'http://tlspbnflow02/api/v1/perfdata?ViewBy=Time&Metric=InBurst1&Metric=InBurst2&Metric=InBurst3&Metric=InBurst4&Metric=InOther&Metric=OutBurst1&Metric=OutBurst2&Metric=OutBurst3&Metric=OutBurst4&Metric=OutOther&minGranularity=MIN15&grid=true&period=CUSTOM_TIME&autoUpdate=false&startTime={}&endTime={}&nfinterfaceId={}&PortIfType=2&DeviceIp={}&DeviceName=RTRB1SHADU&CollectorId=0'.format(start_time, end_time, interfaceId, DeviceIp, DeviceName)
   response = requests.get(url, headers = headers, verify=False)
   return response.text

"""
INTERFACES DETAILS
"""
def get_interfaces_details():
   url = 'http://tlspbnflow02/api/v1/perfdata?_dc=1670175295581&OrderBy=RxUtilization&dir=DESC&ViewBy=Interface&Metric=RxUtilization&Metric=TxUtilization&Metric=RxThroughput&Metric=TxThroughput&Metric=RxPPS&Metric=TxPPS&Metric=Availability&Metric=CurrentStatus&wait=false&rowLimit=100000&searchFields=name%2CInterface.description&GroupSortColumn=&GroupSortDir=ASC&start=0&limit=500&search=&period=LAST_60_MIN&autoUpdate=false'
   response = requests.get(url, headers = headers, verify=False)
   return response.text

def get_intranet_sites():
  subprocess.call('/home/TVadmin/django_code/wanextract/auth.sh', shell=True)
  filepath = '/home/TVadmin/tvc-client.cookie'
  with open(filepath) as fp:
    line = fp.readline()
    cnt = 1
    while line:
      if len(line.split('\t')) > 1:
        authToken = line.split('\t')[6].split('\n')[0]
        headers['Cookie'] = 'authToken=' + authToken
        print("authToken: ", authToken)
      line = fp.readline()
      cnt += 1
    fp.close()
  url_interfaces_by_domain = 'http://127.0.0.1/api/v1/config/collection/json/domain/11/Sites'
  print(url_interfaces_by_domain)
  response = requests.get(url_interfaces_by_domain, headers=headers, verify=False)
  print(response)
  sites = json.loads(response.text)
  for site in sites:
    try:
      check_site = Site.objects.filter(site_name = site['siteName'], truview_site_id = site['siteId'])
      print("check_site", check_site)
      if len(check_site)==0: 
        #site_obj = Site(zonegeo=site['tags']['ZoneGeo'], site_name = site['siteName'], truview_site_id = site['siteId'])
        site_obj = Site(site_name = site['siteName'], truview_site_id = site['siteId'])
        try:
          site_obj.save()
        except Exception:
           print(traceback.format_exc())
        for interface in site['interfaces']:
          print(interface)
          interface_obj = Interface(site=site_obj,deviceIp=interface['deviceIp'], deviceName=interface['deviceName'], truview_if_id=interface['id'], tvfIfId=interface['tvfIfId'],description=interface['description'],name=interface['name'],ifIndex=interface['ifIndex'])
          interface_obj.save()
    except Exception:
      print(traceback.format_exc())
  
  interfaces_details = get_interfaces_details() 
  interfaces_details = json.loads(interfaces_details)
  print(interfaces_details)
  print("### XXX ###")
  for detail in interfaces_details['records']:
    print(detail['Interface'])
    try:
      check_interface = Interface.objects.get(truview_if_id = detail['Interface']['id'])
      print("check_interface ", check_interface)
      check_interface.in_bw = float(detail['Interface']['networkInterfaceInSpeed'])
      check_interface.out_bw = float(detail['Interface']['networkInterfaceOutSpeed'])
      print("check_interface.in_bw check_interface.out_bw ",check_interface.name, check_interface.in_bw, check_interface.out_bw)
      check_interface.save()
      print("saved")
    except Exception:
      print(traceback.format_exc())



def periodic_function_interface_burst():
   filepath = '/home/TVadmin/django_code/wanextract/tvc-client.cookie'
   with open(filepath) as fp:
     line = fp.readline()
     cnt = 1
     while line:
       if len(line.split('\t')) > 1:
         authToken = line.split('\t')[6].split('\n')[0]
         headers['Cookie'] = 'authToken=' + authToken
         print("authToken: ", authToken)
       line = fp.readline()
       cnt += 1
     fp.close()
   from time import time as timestamp
   from datetime import datetime
   local_timestamp = timestamp()
   timestamp=local_timestamp
   END  = str(local_timestamp).split('.')[0]
   START = str(local_timestamp - 3600).split('.')[0]
   print("START END", START, END)
   try:
     date_en = datetime.fromtimestamp(timestamp).date()
     time_en = datetime.fromtimestamp(timestamp).time()
     print(date_en, time_en)
   except Exception:
     print(traceback.format_exc())
   for interface in Interface.objects.all():
      response = burst_per_interface_hourly(interface.truview_if_id, interface.deviceIp, interface.deviceName, str(START) + '000' , str(END)+'000')
      response = json.loads(response)
      print(response)
      if "records" in response.keys():
         for app in response['records']:
            OutBurst1=0.0
            OutBurst2=0.0
            OutBurst3=0.0
            OutBurst4=0.0
            Burst1=0
            Burst2=0
            Burst3=0
            Burst4=0
            if app['OutBurst1'] is not None: OutBurst1= app['OutBurst1']
            if app['OutBurst2'] is not None: OutBurst2= app['OutBurst2']
            if app['OutBurst3'] is not None: OutBurst3= app['OutBurst3']
            if app['OutBurst4'] is not None: OutBurst4= app['OutBurst4']
            if OutBurst3 >= 60: Burst3= 1
            if OutBurst4 >= 80: Burst4= 1
            if Burst3==1 or Burst4==1:
               print(OutBurst1, OutBurst2, OutBurst3, OutBurst4)
               o1 = OutInterfaceBurst(date=date_en, time=time_en, interface = interface, OutBurst1 = OutBurst1, OutBurst2 = OutBurst2, OutBurst3 = OutBurst3, OutBurst4 = OutBurst4, Burst3 = Burst3,  Burst4 = Burst4)
               o1.save()
      if "records" in response.keys():
         for app in response['records']:
            InBurst1=0.0
            InBurst2=0.0
            InBurst3=0.0
            InBurst4=0.0
            Burst1=0
            Burst2=0
            Burst3=0
            Burst4=0
            if app['InBurst1'] is not None: InBurst1 = app['InBurst1']
            if app['InBurst2'] is not None: InBurst2= app['InBurst2']
            if app['InBurst3'] is not None: InBurst3= app['InBurst3']
            if app['InBurst4'] is not None: InBurst4= app['InBurst4']
            if InBurst3 > 60: Burst3= 1
            if InBurst4 > 80: Burst4= 1
            if Burst3==1 or Burst4==1:
               print(InBurst1, InBurst2, InBurst3, InBurst4)
               i1 = InInterfaceBurst(date=date_en, time=time_en, interface = interface, InBurst1 = InBurst1, InBurst2 = InBurst2, InBurst3 = InBurst3, InBurst4 = InBurst4, Burst3 = Burst3,  Burst4 = Burst4)
               i1.save()
