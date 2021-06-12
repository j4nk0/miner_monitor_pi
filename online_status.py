import requests
from lxml import html, etree

class SomeOnlineStatus:

    ONLINE_STATUS_ELEMENT = 'some_online_status'

    def __init__(self):
        self.worker = '-'
        self.hashrate = '-'
        self.coins = '-'

    def __repr__(self):
        return 'SomeOnlineStatus'

    def __str__(self):
        return repr(self)

    def encode_xml(self):
        return etree.Element(self.ONLINE_STATUS_ELEMENT)

    def decode_xml(self, elem):
        return self

class LitecoinpoolOnlineStatus:

    IN_URL = 'litecoinpool'

    LITE_POOL_ONLINE_STATUS_ELEMENT = 'litecoinpool'
    WORKER_ELEMENT = 'lite_worker'
    HASHRATE_ELEMENT = 'lite_hashtate'
    COINS_ELEMENT = 'lite_coins'
    
    def __init__(self, worker='-', hashrate='-', coins='-'):
        self.worker = worker
        self.hashrate = hashrate
        self.coins = coins

    def __repr__(self):
        return 'LitecoinPoolStatus(' + self.worker + ','    \
            + self.hashrate + ',' + self.coins + ')'

    def __str__(self):
        return 'worker: ' + self.worker + '\n' +    \
            'hashrate: ' + self.hashrate + '\n' +   \
            'total_coins: ' + self.coins

    def encode_xml(self):
        xml = etree.Element(self.LITE_POOL_ONLINE_STATUS_ELEMENT)
        etree.SubElement(xml, self.WORKER_ELEMENT).text = self.worker
        etree.SubElement(xml, self.HASHRATE_ELEMENT).text = self.hashrate
        etree.SubElement(xml, self.COINS_ELEMENT).text = self.coins
        return xml

    def decode_xml(self, xml):
        self.worker = xml.find(self.WORKER_ELEMENT).text
        self.hashrate = xml.find(self.HASHRATE_ELEMENT).text
        self.coins = xml.find(self.COINS_ELEMENT).text
        return self

def get_litecoinpool_online_status(worker, api_key):

    STATUS_URL = 'https://www.litecoinpool.org/api?format=html&api_key='

    page = requests.get(STATUS_URL + api_key)
    tree = html.fromstring(page.content)
    try:
        worker_hashrate = tree.xpath('//td[@id="zosimus.1"]')[0].text.split(' ')[0]
        total_coins = tree.xpath('//td[@id="user_total_rewards"]')[0].text
        return LitecoinpoolOnlineStatus(worker, worker_hashrate, total_coins)
    except IndexError:
        return LitecoinpoolOnlineStatus()

