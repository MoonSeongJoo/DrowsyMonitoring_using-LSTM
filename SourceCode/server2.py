import socket
import threading
import pickle
import http.client
from datetime import datetime

conn = http.client.HTTPConnection("125.131.73.188:8080")
headers={'Content-type': 'text/plain; charset=utf-8'}
xml_head = """
<epcis:EPCISDocument xmlns:epcis="urn:epcglobal:epcis:xsd:1"
	xmlns:example="http://ns.example.com/epcis" xmlns:xsd="http://www.w3.org/2001/XMLSchema"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" creationDate="2005-07-11T11:30:47.0Z"
	schemaVersion="1.2">
	<EPCISBody>
		<EventList>
"""

xml_tail = """
		</EventList>
	</EPCISBody>
</epcis:EPCISDocument>
"""


def make_body(a,b):
    now = datetime.now()
    nowDatetime = now.strftime('%Y-%m-%dT%H:%M:%S') + '.' + str(now.microsecond)[:3] + '-09:00'
    print(nowDatetime)

    body = "<ObjectEvent>" + \
          "<eventTime>" + nowDatetime + "</eventTime>" + \
          "<eventTimeZoneOffset>" + "-09:00" + "</eventTimeZoneOffset>" + \
          "<epcList>" + "<epc>" + a + "</epc>" + "<epc>" + b + "</epc>" + "</epcList>" + \
          "<action>OBSERVE</action>" + "</ObjectEvent>"

    return body


class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        #print(type(client))
        print ("Connected ", address)
        while True:
            try:
                data = client.recv(size)

                if data:
                    # Set the response to echo back the recieved data
                    response = 'ok'
                    client.send(response.encode())
                    
                    obj= pickle.loads(data)
                    #print(obj)
                    test = obj.split(',')
                    print(test)
                    #################################################
                    xml_request = str(xml_head + make_body(test[0], test[1]) + xml_tail)
                    conn.request("POST", "/epcis/Service/EventCapture", headers=headers, body=xml_request.encode('utf-8'))
                    res = conn.getresponse()
                    data = res.read()
                    print(data.decode("utf-8"))
                    #################################################

                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False

if __name__ == "__main__":
    port_num = 50007
    ThreadedServer('',port_num).listen()