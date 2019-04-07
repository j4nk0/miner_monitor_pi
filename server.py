import socketserver as socks
from status import FullStatus
from lxml import etree

last_status = []

def complete_table(table):
    table_header = etree.SubElement(table, 'tr')
    etree.SubElement(table_header, 'th').text = 'Label'
    etree.SubElement(table_header, 'th').text = 'Date Time'
    etree.SubElement(table_header, 'th').text = 'Hashrate KH/s'
    etree.SubElement(table_header, 'th').text = 'Elapsed time'
    etree.SubElement(table_header, 'th').text = 'Fan1 RPM'
    etree.SubElement(table_header, 'th').text = 'Fan2 RPM'
    etree.SubElement(table_header, 'th').text = 'Pool url'
    etree.SubElement(table_header, 'th').text = 'Worker'
    etree.SubElement(table_header, 'th').text = 'Accepted'
    etree.SubElement(table_header, 'th').text = 'Rejected'
    etree.SubElement(table_header, 'th').text = 'Stales'
    etree.SubElement(table_header, 'th').text = 'Pool Worker'
    etree.SubElement(table_header, 'th').text = 'Pool Hashrate KH/s'
    etree.SubElement(table_header, 'th').text = 'Coins'
    etree.SubElement(table_header, 'th').text = 'HW errors'
    etree.SubElement(table_header, 'th').text = 'PCB temp C'
    etree.SubElement(table_header, 'th').text = 'Chip temp C'
    etree.SubElement(table_header, 'th').text = 'Chip status'

def get_html_list(status):
    """12 rows per miner"""
    html_list = []
    row1 = etree.Element('tr')          #1
    html_list.append(row1)
    etree.SubElement(row1, 'td', rowspan='12').text = status.label
    # MinerStatus
    etree.SubElement(row1, 'td', rowspan='12').text = status.miner_status.datetime
    etree.SubElement(row1, 'td', rowspan='12').text = status.miner_status.hashrate
    etree.SubElement(row1, 'td', rowspan='12').text = status.miner_status.elapsed_time
    etree.SubElement(row1, 'td', rowspan='12').text = status.miner_status.fan1_rpm
    etree.SubElement(row1, 'td', rowspan='12').text = status.miner_status.fan2_rpm
    # PoolStaus 0
    etree.SubElement(row1, 'td', rowspan='4').text = status.miner_status.pools[0].url
    etree.SubElement(row1, 'td', rowspan='4').text = status.miner_status.pools[0].worker
    etree.SubElement(row1, 'td', rowspan='4').text = status.miner_status.pools[0].accepted
    etree.SubElement(row1, 'td', rowspan='4').text = status.miner_status.pools[0].rejected
    etree.SubElement(row1, 'td', rowspan='4').text = status.miner_status.pools[0].stales
    # PoolOnlineStatus 0
    etree.SubElement(row1, 'td', rowspan='4').text = status.pool_online_statuses[0].worker
    etree.SubElement(row1, 'td', rowspan='4').text = status.pool_online_statuses[0].hashrate
    etree.SubElement(row1, 'td', rowspan='4').text = status.pool_online_statuses[0].coins
    # HashboardStatus 0
    etree.SubElement(row1, 'td', rowspan='3').text = status.miner_status.hashboards[0].hw_errors
    etree.SubElement(row1, 'td', rowspan='3').text = status.miner_status.hashboards[0].temp_pcb
    etree.SubElement(row1, 'td', rowspan='3').text = status.miner_status.hashboards[0].temp_chip
    etree.SubElement(row1, 'td', rowspan='3').text = status.miner_status.hashboards[0].chip_status

    html_list.append(etree.Element('tr'))      # 2
    html_list.append(etree.Element('tr'))        # 3
    row4 = etree.Element('tr') # 4
    html_list.append(row4)
    # HashboardStatus 1
    etree.SubElement(row4, 'td', rowspan='3').text = status.miner_status.hashboards[1].hw_errors
    etree.SubElement(row4, 'td', rowspan='3').text = status.miner_status.hashboards[1].temp_pcb
    etree.SubElement(row4, 'td', rowspan='3').text = status.miner_status.hashboards[1].temp_chip
    etree.SubElement(row4, 'td', rowspan='3').text = status.miner_status.hashboards[1].chip_status

    row5 = etree.Element('tr') # 5
    html_list.append(row5)
    # PoolStaus 1
    etree.SubElement(row5, 'td', rowspan='4').text = status.miner_status.pools[1].url
    etree.SubElement(row5, 'td', rowspan='4').text = status.miner_status.pools[1].worker
    etree.SubElement(row5, 'td', rowspan='4').text = status.miner_status.pools[1].accepted
    etree.SubElement(row5, 'td', rowspan='4').text = status.miner_status.pools[1].rejected
    etree.SubElement(row5, 'td', rowspan='4').text = status.miner_status.pools[1].stales
    # PoolOnlineStatus 1
    etree.SubElement(row5, 'td', rowspan='4').text = status.pool_online_statuses[1].worker
    etree.SubElement(row5, 'td', rowspan='4').text = status.pool_online_statuses[1].hashrate
    etree.SubElement(row5, 'td', rowspan='4').text = status.pool_online_statuses[1].coins

    html_list.append(etree.Element('tr'))        # 6
    row7 = etree.Element('tr') # 7
    html_list.append(row7)
    # HashboardStatus 2
    etree.SubElement(row7, 'td', rowspan='3').text = status.miner_status.hashboards[2].hw_errors
    etree.SubElement(row7, 'td', rowspan='3').text = status.miner_status.hashboards[2].temp_pcb
    etree.SubElement(row7, 'td', rowspan='3').text = status.miner_status.hashboards[2].temp_chip
    etree.SubElement(row7, 'td', rowspan='3').text = status.miner_status.hashboards[2].chip_status

    html_list.append(etree.Element('tr'))        # 8
    row9 = etree.Element('tr') # 9
    html_list.append(row9)
    # PoolStaus 2
    etree.SubElement(row9, 'td', rowspan='4').text = status.miner_status.pools[2].url
    etree.SubElement(row9, 'td', rowspan='4').text = status.miner_status.pools[2].worker
    etree.SubElement(row9, 'td', rowspan='4').text = status.miner_status.pools[2].accepted
    etree.SubElement(row9, 'td', rowspan='4').text = status.miner_status.pools[2].rejected
    etree.SubElement(row9, 'td', rowspan='4').text = status.miner_status.pools[2].stales
    # PoolOnlineStatus 2
    etree.SubElement(row9, 'td', rowspan='4').text = status.pool_online_statuses[2].worker
    etree.SubElement(row9, 'td', rowspan='4').text = status.pool_online_statuses[2].hashrate
    etree.SubElement(row9, 'td', rowspan='4').text = status.pool_online_statuses[2].coins

    row10 = etree.Element('tr') # 10
    html_list.append(row10)
    # HashboardStatus 3
    etree.SubElement(row10, 'td', rowspan='3').text = status.miner_status.hashboards[3].hw_errors
    etree.SubElement(row10, 'td', rowspan='3').text = status.miner_status.hashboards[3].temp_pcb
    etree.SubElement(row10, 'td', rowspan='3').text = status.miner_status.hashboards[3].temp_chip
    etree.SubElement(row10, 'td', rowspan='3').text = status.miner_status.hashboards[3].chip_status
    html_list.append(etree.Element('tr'))        # 11
    html_list.append(etree.Element('tr'))        # 12 
    #html_list.append(etree.Element('tr'))        # 13
    return html_list

def brief_table(table):
    table_header = etree.SubElement(table, 'tr')
    etree.SubElement(table_header, 'th').text = 'Label'
    etree.SubElement(table_header, 'th').text = 'Date Time'
    etree.SubElement(table_header, 'th').text = 'Elapsed time'
    etree.SubElement(table_header, 'th').text = 'Hashrate KH/s'
    etree.SubElement(table_header, 'th').text = 'Pool KH/s'
    etree.SubElement(table_header, 'th').text = 'Coins'
    etree.SubElement(table_header, 'th').text = 'Chip temp C'

def get_brief_html(status):
    """1 row per miner"""
    row1 = etree.Element('tr')          #1
    etree.SubElement(row1, 'td').text = status.label
    etree.SubElement(row1, 'td').text = status.miner_status.datetime
    etree.SubElement(row1, 'td').text = status.miner_status.elapsed_time
    etree.SubElement(row1, 'td').text = status.miner_status.hashrate
    etree.SubElement(row1, 'td').text = status.pool_online_statuses[0].hashrate
    etree.SubElement(row1, 'td').text = status.pool_online_statuses[0].coins
    etree.SubElement(row1, 'td').text = status.miner_status.hashboards[0].temp_chip
    return row1

def run_server(ip, port, queue_list):
    class ThreadedTCPServer(socks.ThreadingMixIn, socks.TCPServer):
        pass

    class RequestHandler(socks.BaseRequestHandler):

        def handle(self):
            global last_status
            for i in range(len(queue_list)):
                if len(last_status) == i: last_status.append(queue_list[i].get())   # blocking
                while not queue_list[i].empty():
                    last_status[i] = queue_list[i].get()
            content = etree.Element('html')
            head = etree.SubElement(content, 'head')
            style = etree.SubElement(head, 'style').text = """
                table, th, td {
                  border: 1px solid black;
                }
                th, td {
                  text-align: center;
                }
                table th {
                  background-color: black;
                  color: white;
                }
                a:link, a:visited {
                  background-color: black;
                  color: white;
                  padding: 15px 25px;
                  text-align: center;
                  text-decoration: none;
                  display: inline-block;
                }
            """
            script = etree.SubElement(head, 'script').text = """
            function reload() {
              location.reload();
            }
            """
            title = etree.SubElement(head, 'title').text = 'Miners'
            data = self.request.recv(256)
            try:
                url = data.decode('UTF-8').split(' ')[1]
            except IndexError:
                url = ''
            body = etree.SubElement(content, 'body')
            button_refresh = etree.SubElement(body, 'button', {'onclick': 'reload()'}).text = 'Refresh'
            if url == '/detailed':
                button_brief = etree.SubElement(body, 'button', {
                    'onclick': 'window.location.href="/"'
                }).text = 'Brief'
                table = etree.SubElement(body, 'table')
                complete_table(table)
                for status in last_status: 
                    for elem in get_html_list(status):
                        table.insert(len(list(table)), elem)
            else:
                button_detailed = etree.SubElement(body, 'button', {
                    'onclick': 'window.location.href="/detailed"'
                }).text = 'Detailed'
                table = etree.SubElement(body, 'table')
                brief_table(table)
                for status in last_status:
                    table.insert(len(list(table)), get_brief_html(status))
            response = b'<!DOCTYPE html>' + etree.tostring(content)
            self.request.sendall(response)

    with ThreadedTCPServer((ip, port), RequestHandler) as server:
        server.serve_forever()

