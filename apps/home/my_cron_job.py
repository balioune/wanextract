from django_cron import CronJobBase, Schedule
from apps.home.models import *

import logging

headers = dict()
logging.basicConfig(filename="/var/log/wanextract/extract_monthly_data.log", format='%(asctime)s %(message)s', filemode='w')
class MyCronJob(CronJobBase):
    #RUN_EVERY_MINS = 120 # every 2 hours
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'apps.home.my_cron_job'    # a unique code

    def do(self):
        logger=logging.getLogger() 
        logger.info(Interface.objects.all())
        pass    # do your thing here
