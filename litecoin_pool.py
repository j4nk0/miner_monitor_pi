import requests
from lxml import html, etree

class LitecoinPoolStatus:
    
    def __init__(self, worker=None, hashrate=None, coins=None):
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

def get_litecoin_pool_status(worker, api_key):

    STATUS_URL = 'https://www.litecoinpool.org/api?format=html&api_key='

    page = requests.get(STATUS_URL + api_key)
    tree = html.fromstring(page.content)
    worker_hashrate = tree.xpath('//td[@id="zosimus.1"]')[0].text.split(' ')[0]
    total_coins = tree.xpath('//td[@id="user_total_rewards"]')[0].text
    return LitecoinPoolStatus(worker, worker_hashrate, total_coins)

if __name__ == '__main__':
    print(get_litecoin_pool_status('zosimus.1', 'c23d63c025d4b9e901d79e5f955245aa'))
