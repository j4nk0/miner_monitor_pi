from status import *
from lxml import etree
from queue import Queue
from online_status import *
from server import run_server
from restart_pi import restart
from threading import Thread as th

# ++++++++++++++++++++++++ OLD ^^^ +++++++++++++++++++++++++++
from os.path import isfile
from time import sleep
from sys import argv
from configparser import ConfigParser
from online_status import get_litecoinpool_online_status

import requests
from datetime import datetime as dt
import json

def get_config(filename):
    config = ConfigParser()
    config.read(filename)
    global_settings = { 'miners' : {} }
    for section in config.sections():
        miner = { 'label' : section }
        miner['gpio'] = config[section].getint('gpio', 5)
        miner['worker'] = config[section].get('worker', 'zosimus2.1')
        global_settings['miners'][section] = miner
    return global_settings


def get_litecoinpool_online_status():

    API_URL = 'https://www.litecoinpool.org/api'
    API_KEY = 'e404ff1f0125c2e8dea9c16cdda4e6e7'
    STATUS_URL = API_URL + '?api_key=' + API_KEY

    page = requests.get(STATUS_URL).json()

    ONLINE_STATUS = {}
    for worker in page['workers']:
        hashrate = page['workers'][worker]['hash_rate']
        ONLINE_STATUS[worker] = hashrate
    ONLINE_STATUS['datetime'] = dt.now()
    return ONLINE_STATUS


    
SCAN_INTERVAL = 30  # seconds

try:
    config_filename = argv[1]
    if not isfile(config_filename): raise IndexError
except IndexError:
    config_filename = 'miner_monitor.conf'  # Default


global_settings = get_config(config_filename)

while True:
    online_status = get_litecoinpool_online_status()
    for miner in global_settings['miners']:
        hashrate = online_status[miner['worker']]
        if hashrate < 450:
            
    sleep(SCAN_INTERVAL)


