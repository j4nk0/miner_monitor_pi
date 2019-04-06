from sys import argv
from status import *
from time import sleep
from lxml import etree
from queue import Queue
from os.path import isfile
from online_status import *
from server import run_server
from restart_pi import restart
from threading import Thread as th
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
        self.tree.getroot().insert(-1, status.encode_xml())

    def count(self):
        return len(list(self.tree.getroot()))

    def get(self, index=None):
        if self.count() == 0: return None
        if index == None: index = self.count() - 1
        return FullStatus().decode_xml(self.tree.getroot().getchildren()[index])

    def read(self, filename):
        self.tree = etree.parse(filename)

    def write(self, filename):
        self.tree.write(filename)

    
def monitor(queue, db, miner_settings):

    SCAN_INTERVAL = 5 #30  # seconds
    PASSES_BEFORE_SAVING = 1 #20   # amounts to cca 10 minutes

    while True:
        for _ in range(PASSES_BEFORE_SAVING):
            # get status from miner
            try:
                miner_status = get_miner_status(miner_settings['ip'], miner_settings['password'])
            except:
                miner_status = MinerStatus()
            # check if miner is ok:
            if not miner_status.boards_ok(): restart(miner_settings['gpio']
            # get online statuses from pools:
            online_list = [ SomeOnlineStatus() for _ in range(3) ]
            for i in range(3):
                if LitecoinpoolOnlineStatus.IN_URL in miner_status.pools[i].url: 
                    online_list[i] = get_litecoinpool_online_status(
                        miner_status.pools[i].worker,
                        miner_settings['api_key' + str(i + 1)]
                    )
            status = FullStatus(miner_settings['label'], miner_status, online_list)
            # Record statuses
            db.add(status)
            # Send last status to server:
            if queue.full(): queue.get()
            queue.put(status)
            sleep(SCAN_INTERVAL)
        # Record statuses
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

