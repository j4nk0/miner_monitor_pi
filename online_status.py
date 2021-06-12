import requests
from datetime import datetime as dt
import json

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

if __name__ == '__main__':
    print (get_litecoinpool_online_status())
 
