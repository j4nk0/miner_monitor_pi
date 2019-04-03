from lxml import html, etree
import requests
from requests.auth import HTTPDigestAuth # = antminer authentification
from datetime import datetime

class PoolStatus:
    """DTO represents 1 pool"""

    POOL_STATUS_ELEMENT = 'pool_status'
    URL_ELEMENT = 'url'
    WORKER_ELEMENT = 'worker'
    ACCEPTED_ELEMENT = 'accepted'
    REJECTED_ELEMENT = 'rejected' 
    STALES_ELEMENT = 'stales'

    def __init__(self, url=None, worker=None, accepted=None, rejected=None, stales=None):
        self.url = url
        self.worker = worker
        self.accepted = accepted
        self.rejected = rejected
        self.stales = stales

    def __repr__(self):
        return 'Pool_status(' + str(self.url) + ', '    \
            + str(self.worker)   + ', '                 \
            + str(self.accepted) + ', '                 \
            + str(self.rejected) + ', '                 \
            + str(self.stales) + ')'

    def __str__(self):
        string  = 'url: '      + str(self.url)      + '\n'
        string += 'worker: '   + str(self.worker)   + '\n'
        string += 'accepted: ' + str(self.accepted) + '\n'
        string += 'rejected: ' + str(self.rejected) + '\n'
        string += 'stales: '   + str(self.stales)
        return string
 
    def encode_xml(self):
        """returns XML element object"""
        xml = etree.Element(self.POOL_STATUS_ELEMENT)
        etree.SubElement(xml, self.URL_ELEMENT).text = str(self.url)
        etree.SubElement(xml, self.WORKER_ELEMENT).text = str(self.worker)
        etree.SubElement(xml, self.ACCEPTED_ELEMENT).text = str(self.accepted)
        etree.SubElement(xml, self.REJECTED_ELEMENT).text = str(self.rejected)
        etree.SubElement(xml, self.STALES_ELEMENT).text = str(self.stales)
        return xml 

    def decode_xml(self, xml):
        """takes XML element object"""
        self.url = xml.find(self.URL_ELEMENT).text
        self.worker = xml.find(self.WORKER_ELEMENT).text
        self.accepted = xml.find(self.ACCEPTED_ELEMENT).text
        self.rejected = xml.find(self.REJECTED_ELEMENT).text
        self.stales = xml.find(self.STALES_ELEMENT).text
        return self

class HashboardStatus:
    """DTO represents 1 hashboard"""

    HASHBOARD_STATUS_ELEMENT = 'hashboard_status'
    HW_ERRORS_ELEMENT = 'hw_errors'
    TEMP_PCB_ELEMENT = 'temp_pcb'
    TEMP_CHIP_ELEMENT = 'temp_chip'
    CHIP_STATUS_ELEMENT = 'chip_status'

    def __init__(self, hw_errors=None, temp_pcb=None, temp_chip=None, chip_status=None):
        self.hw_errors = hw_errors
        self.temp_pcb = temp_pcb
        self.temp_chip = temp_chip
        self.chip_status = chip_status

    def __repr__(self):
        return 'Hashboard_status(' + str(self.hw_errors) + ', '    \
            + str(self.temp_pcb) + ', '                            \
            + str(self.temp_chip) + ', '                           \
            + str(self.chip_status) + ')'

    def __str__(self):
        string  = 'hw_errors: '   + str(self.hw_errors) + '\n'
        string += 'temp_pcb: '    + str(self.temp_pcb)  + '\n'
        string += 'temp_chip: '   + str(self.temp_chip) + '\n'
        string += 'chip_status: ' + str(self.chip_status)
        return string

    def encode_xml(self):
        """returns XML element object"""
        xml = etree.Element(self.HASHBOARD_STATUS_ELEMENT)
        etree.SubElement(xml, self.HW_ERRORS_ELEMENT).text = str(self.hw_errors)
        etree.SubElement(xml, self.TEMP_PCB_ELEMENT).text = str(self.temp_pcb)
        etree.SubElement(xml, self.TEMP_CHIP_ELEMENT).text = str(self.temp_chip)
        etree.SubElement(xml, self.CHIP_STATUS_ELEMENT).text = str(self.chip_status)
        return xml

    def decode_xml(self, xml):
        """takes XML element object"""
        self.hw_errors = xml.find(self.HW_ERRORS_ELEMENT).text
        self.temp_pcb = xml.find(self.TEMP_PCB_ELEMENT).text
        self.temp_chip = xml.find(self.TEMP_CHIP_ELEMENT).text
        self.chip_status = xml.find(self.CHIP_STATUS_ELEMENT).text
        return self

class MinerStatus:
    """DTO, describes whole miner at certain time"""

    MINER_STATUS_ELEMENT = 'miner_status'
    DATETIME_ELEMENT = 'datetime'
    HASHRATE_ELEMENT = 'hashrate'
    ELAPSED_TIME_ELEMENT = 'elapsed_time'
    FAN1_RPM_ELEMENT = 'fan1_rpm'
    FAN2_RPM_ELEMENT = 'fan2_rpm'

    def __init__(self, datetime=None, hashrate=None, elapsed_time=None, fan1_rpm=None,  \
        fan2_rpm=None, pools=None, hashboards=None):
        self.datetime = datetime
        self.hashrate = hashrate
        self.elapsed_time = elapsed_time
        self.fan1_rpm = fan1_rpm
        self.fan2_rpm = fan2_rpm
        self.pools = pools
        self.hashboards = hashboards
        if self.pools == None: self.pools = [ PoolStatus() for _ in range(3) ]
        if self.hashboards == None: self.hashboards = [ HashboardStatus() for _ in range(4) ]

    def __repr__(self):
        return 'Miner_status(' + str(self.datetime) + ', '     \
            + str(self.hashrate) + ', '                        \
            + str(self.elapsed_time) + ', '                    \
            + str(self.fan1_rpm) + ', '                        \
            + str(self.fan2_rpm) + ', '                        \
            + repr(self.pools) + ', '                          \
            + repr(self.hashboards) + ')'                      \

    def __str__(self):
        string = 'Miner_status from ' + str(self.datetime) + ':\n'
        string += 'hashrate: ' + str(self.hashrate) + '\n'
        string += 'elapsed_time: ' + str(self.elapsed_time) + '\n'
        string += 'fan1_rpm: ' + str(self.fan1_rpm) + '\n'
        string += 'fan2_rpm: ' + str(self.fan2_rpm) + '\n'
        for i in range(3): 
            string += ('\t' + 'pool ' + str(i) + ':\n'
                + str(self.pools[i]) + '\n'
            )
        for i in range(4): 
            string += ('\t' + 'hashboard ' + str(i) + ':\n'
                + str(self.hashboards[i]) + '\n'
            )
        return string[:-1]

    def encode_html(self, label):
        """a single table row"""
        html = etree.Element('tr')
        etree.SubElement(html, 'td').text = label
        etree.SubElement(html, 'td').text = self.datetime
        etree.SubElement(html, 'td').text = self.hashrate
        etree.SubElement(html, 'td').text = self.elapsed_time
        etree.SubElement(html, 'td').text = self.fan1_rpm
        etree.SubElement(html, 'td').text = self.fan2_rpm
        return html

    def encode_xml(self):
        """returns XML element object"""
        xml = etree.Element(self.MINER_STATUS_ELEMENT)
        etree.SubElement(xml, self.DATETIME_ELEMENT).text = str(self.datetime)
        etree.SubElement(xml, self.HASHRATE_ELEMENT).text = str(self.hashrate)
        etree.SubElement(xml, self.ELAPSED_TIME_ELEMENT).text = str(self.elapsed_time)
        etree.SubElement(xml, self.FAN1_RPM_ELEMENT).text = str(self.fan1_rpm)
        etree.SubElement(xml, self.FAN2_RPM_ELEMENT).text = str(self.fan2_rpm)
        for pool in self.pools:
            xml.insert(-1, pool.encode_xml())
        for hashboard in self.hashboards:
            xml.insert(-1, hashboard.encode_xml())
        return xml

    def decode_xml(self, xml):
        """takes XML element object"""
        self.datetime = xml.find(self.DATETIME_ELEMENT).text
        self.hashrate = xml.find(self.HASHRATE_ELEMENT).text
        self.elapsed_time = xml.find(self.ELAPSED_TIME_ELEMENT).text
        self.fan1_rpm = xml.find(self.FAN1_RPM_ELEMENT).text
        self.fan2_rpm = xml.find(self.FAN2_RPM_ELEMENT).text
        self.pools = [ PoolStatus().decode_xml(i) for i in xml.iterfind(PoolStatus.POOL_STATUS_ELEMENT) ]
        self.hashboards = [ HashboardStatus().decode_xml(i) for i in xml.iterfind(HashboardStatus.HASHBOARD_STATUS_ELEMENT) ]
        return self

class FullStatus:
    
    def __init__(self, label=None, miner_status=None, pool_online_statuses=None):
        self.label = label
        self.miner_status = miner_status
        self.pool_online_statues = pool_online_statuses if pool_online_statuses != None else []

    def encode_xml(self):
        pass

    def decode_xml(self, element):
        pass

    def encode_html(self):
        pass

def get_miner_status(ip, password):
    """Connects to miner using given ip_address and password.
    Scrapes needed data and returns Miner_status object.
    Always sets recovered values as strings.

    Also builds needed Hashboard_status and Pool_status objects.
    """
    # given by antminer design
    STATUS_URL = '/cgi-bin/minerStatus.cgi'
    MINER_USER = 'root'
    PROTOCOL = 'http://'

    url = PROTOCOL  + ip + STATUS_URL
    authenification = HTTPDigestAuth(MINER_USER, password)
    page = requests.get(url, auth=authenification, timeout=10)
    tree = html.fromstring(page.content)

    miner_status = MinerStatus()
    miner_status.datetime = str(datetime.now())
    miner_status.hashrate = str(1000 * float(tree.xpath('//div[@id="ant_ghs5s"]/text()')[0]))
    miner_status.elapsed_time = tree.xpath('//div[@id="ant_elapsed"]/text()')[0] # 37m44s
    miner_status.fan1_rpm = ''.join(tree.xpath('//td[@id="ant_fan1"]/text()')[0].split(','))
    miner_status.fan2_rpm = ''.join(tree.xpath('//td[@id="ant_fan2"]/text()')[0].split(','))

    # order is important!
    # last value represents number of hardware errors -> is useless
    pools_urls = self.tree.xpath('//div[@id="cbi-table-1-url"]/text()')
    pool_workers = self.tree.xpath('//div[@id="cbi-table-1-user"]/text()')
    pool_accepted = self.tree.xpath('//div[@id="cbi-table-1-accepted"]/text()')
    # fourth value being total 
    pool_rejected = self.tree.xpath('//div[@id="cbi-table-1-rejected"]/text()')
    # fourth value being total 
    pool_stales = self.tree.xpath('//div[@id="cbi-table-1-stale"]/text()')
    for i in range(len(self.status.pools)):
       miner_status.pools[i].url = pools_urls[i]
       miner_status.pools[i].worker = pool_workers[i]
       miner_status.pools[i].accepted = pool_accepted[i]
       miner_status.pools[i].rejected = pool_rejected[i]
       miner_status.pools[i].stales = pool_stales[i]

    HW_errors = self.tree.xpath('//div[@id="cbi-table-1-hw"]/text()')
    # data: ['I:0 O:64', 'I:0 O:60', 'I:0 O:61', 'I:0 O:58']
    temp_pcb = self.tree.xpath('//div[@id="cbi-table-1-temp"]/text()') 
    # ['I:0 O:69', 'I:0 O:66', 'I:0 O:67', 'I:0 O:65']
    temp_chip = self.tree.xpath('//div[@id="cbi-table-1-temp2"]/text()') 
    # status: ' oooooooo oooooooo oooooooo oooooooo oooooooo oooooooo oooooooo oooooooo oooooooo', 
    # first 3 values being pool statuses (for some odd reason)
    board_chip_status = self.tree.xpath('//div[@id="cbi-table-1-status"]/text()')
    for i in range(len(self.status.hashboards)):
        miner_status.hashboards[i].hw_errors = HW_errors[i]
        miner_status.hashboards[i].temp_pcb = temp_pcb[i].split(':')[2]  # in deg C
        miner_status.hashboards[i].temp_chip = temp_chip[i].split(':')[2]    # in deg C
        miner_status.hashboards[i].chip_status = board_chip_status[i + 3]
    return miner_status

def dummy_get_miner_status():
    ps = PoolStatus('url', 'worker', 12, 3, 5)
    hb = HashboardStatus('5', 40, 45, ' oooooooo oooooooo ')
    ms = MinerStatus(str(datetime.now()), '501', '2h35m13s', '1500', '1300', [ps, ps, ps],
        [hb, hb, hb, hb])
    return ms
   
if __name__ == '__main__':
    ps = PoolStatus('url', 'worker', 12, 3, 5)
    hb = HashboardStatus('5', 40, 45, ' oooooooo oooooooo ')
    ms = MinerStatus(datetime.now(), '501', '2h35m13s', '1500', '1300', [ps, ps, ps], [hb, hb, hb, hb])
    print(ms)
    ms2 = MinerStatus().decode_xml(ms.encode_xml())
    assert str(ms) == str(ms2)
    try:
        status = get_miner_status()
        print(status)
    except:
        print('Failed to establish connectio to server!')
