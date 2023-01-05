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
      site_obj = Site(site_name = site['siteName'], truview_site_id = site['siteId'])
      site_obj.save()
      #check_site = Site.objects.filter(site_name = site['siteName'], truview_site_id = site['siteId'])
      check_site=1
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
  """
  interfaces_details = get_interfaces_details() 
  interfaces_details = json.loads(interfaces_details)
  #print(interfaces_details)
  print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
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
  """
