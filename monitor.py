from status import get_miner_status, dummy_get_miner_status
from view import *
from threading import Thread as th
from server import run_server
from queue import Queue
from os.path import isfile
from sys import argv
from time import sleep
from lxml import etree
from litecoin_pool import get_litecoin_pool_status
from configparser import ConfigParser

def get_config(filename):
    config = ConfigParser()
    config.read(filename)
    global_settings = { 'miners' : {} }
    if 'MAIN' in config.sections():
        global_settings['server_ip'] = config.get('server_ip', '127.0.0.1')
        global_settings['server_port'] = config.getint('server_port', 80)
    else:
        global_settings['server_ip'] = '127.0.0.1'
        global_settings['server_port'] = 80
    for section in config.sections():
        if section == 'MAIN': continue
        miner = { 'label' : section }
        miner['username'] = config[section].get('username', 'root')
        miner['password'] = config[section].get('password', 'root')
        miner['ip'] = config[section].get('ip', '192.168.0.1')
        miner['gpio'] = config[section].getint('gpio', 5)
        miner['db_file'] = config[section].get('db_file', section + '_db.xml')
        miner['api_key1'] = config[section].get('api_key1', 'no_key')
        miner['api_key2'] = config[section].get('api_key2', 'no_key')
        miner['api_key3'] = config[section].get('api_key3', 'no_key')
        global_settings['miners'][section] = miner
    return global_settings

class StatusDB:

    STATUS_LOG_ELEMENT = 'status_log'
    MAX_RECORDS = 1000

    def __init__(self, other=None):
        if other != None: self.tree = other.tree
        else: self.tree = etree.ElementTree(etree.Element(self.STATUS_LOG_ELEMENT))

    def add(self, status):
        if len(list(self.tree.getroot())) >= self.MAX_RECORDS:
            self.tree.getroot().remove(self.tree.getroot()[0])
        self.tree.getroot().insert(self.count(), status.encode_xml())

    def count(self):
        return len(list(self.tree.getroot()))

    def get(self, index=None):
        if self.count() == 0: return None
        if index == None: index = self.count() - 1
        return Miner_status().decode_xml(self.tree.getroot().getchildren()[index])

    def read(self, filename):
        self.tree = etree.parse(filename)

    def write(self, filename):
        self.tree.write(filename)

def monitor(queue, db, miner_settings):

    SCAN_INTERVAL = 5 #30  # seconds
    PASSES_BEFORE_SAVING = 1 #20   # amounts to cca 10 minutes

    while True:
        for _ in range(PASSES_BEFORE_SAVING):
            miner_status = get_miner_status(miner_settings['ip'], miner_settings['password'])
            #miner_status = dummy_get_miner_status()
            litecoin_pool_status = get_litecoin_pool_status(miner_status.pools[0].worker, miner_settings['api_key1'])
            db.add(miner_status)
            view = MinerView(miner_status)
            if queue.full(): queue.get()
            queue.put(miner_status)
            print(miner_status.datetime, miner_status.hashrate, litecoin_pool_status.hashrate)
            sleep(SCAN_INTERVAL)
        db.write(miner_settings['db_file'])

try:
    config_filename = argv[1]
    if not isfile(config_filename): raise IndexError
except IndexError:
    config_filename = 'miner_monitor.conf'  # Default

global_settings = get_config(config_filename)
queue_list = []

for miner in global_settings['miners']:
    db = StatusDB()
    dbfilename = global_settings['miners'][miner]['db_file']
    if isfile(dbfilename): db.read(dbfilename)
    q = Queue(3)
    queue_list.append(q)
    th(target=monitor, args=(q, db, global_settings['miners'][miner])).start()

run_server(global_settings['server_ip'], global_settings['server_port'], queue_list)

