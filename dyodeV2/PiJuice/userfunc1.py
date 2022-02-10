#!/usr/bin/python3

import sys
import logging
import time
from pijuice import PiJuice
import subprocess

logger = logging.getLogger('user_func1')
hdlr = logging.FileHandler('/home/pi/user_func1.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

pj=PiJuice(1,0x14)
logger.info(str(sys.argv))

time.sleep(10)
logger.info('Timeout expired')

status=pj.status.GetStatus()
if status['error'] == 'NO_ERROR':
   data = status['data']
   if (data['powerInput']=='NOT_PRESENT') and (data['powerInput5vIo']=='NOT_PRESENT'):
      logger.info('Still no power, shutting down')
      pj.power.SetWakeUpOnCharge(0.0,non_volatile=True)
      subprocess.call(['sudo', 'halt'])
   else:
      logger.info('power is back')
else:
  logger.info("Status : ERROR")
  pj.power.SetWakeUpOnCharge(0.0,non_volatile=True)
  subprocess.call(['sudo', 'halt'])
