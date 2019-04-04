import socketserver as socks
from lxml import etree

last_status = []

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
            style = etree.SubElement(head, 'style').text = """table {
                  width:100%;
                }
                table, th, td {
                  border: 1px solid black;
                  border-collapse: collapse;
                }
                th, td {
                  text-align: center;
                }
                table#t01 tr:nth-child(even) {
                  background-color: #eee;
                }
                table#t01 tr:nth-child(odd) {
                  background-color: #fff;
                }
                table th {
                  background-color: black;
                  color: white;
                }
            """
            body = etree.SubElement(content, 'body')
            table = etree.SubElement(body, 'table')
            table_header = etree.SubElement(table, 'tr')
            etree.SubElement(table_header, 'th').text = 'Label'
            etree.SubElement(table_header, 'th').text = 'Date Time'
            etree.SubElement(table_header, 'th').text = 'Hashrate'
            etree.SubElement(table_header, 'th').text = 'Elapsed time'
            etree.SubElement(table_header, 'th').text = 'Fan1'
            etree.SubElement(table_header, 'th').text = 'Fan2'
            etree.SubElement(table_header, 'th').text = 'Pool url'
            etree.SubElement(table_header, 'th').text = 'Worker'
            etree.SubElement(table_header, 'th').text = 'Accepted'
            etree.SubElement(table_header, 'th').text = 'Rejected'
            etree.SubElement(table_header, 'th').text = 'Stales'
            etree.SubElement(table_header, 'th').text = 'Worker'
            etree.SubElement(table_header, 'th').text = 'Hashrate'
            etree.SubElement(table_header, 'th').text = 'Coins'
            etree.SubElement(table_header, 'th').text = 'HW errors'
            etree.SubElement(table_header, 'th').text = 'PCB temp'
            etree.SubElement(table_header, 'th').text = 'Chip temp'
            etree.SubElement(table_header, 'th').text = 'Chip status'
            #etree.SubElement(table_header, 'th').text = 'Pool hashrate'
            table_datarow = etree.SubElement(table, 'tr')
            for status in last_status:
                table_datarow.insert(-1, status.get_html())

            response = b'<!DOCTYPE html>' + etree.tostring(content)
            self.request.sendall(response)

    with ThreadedTCPServer((ip, port), RequestHandler) as server:
        server.serve_forever()
