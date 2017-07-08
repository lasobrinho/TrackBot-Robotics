import socket
import network
import time
import machine

ap = network.WLAN(network.AP_IF)

CONTENT = b"""\
HTTP/1.0 200 OK

<!doctype html>
<html>
    <head>
        <title>TrackBot Helper</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta charset="utf8">
    </head>
    <body>

        <h1>TrackBot v1.0</h1>
        <div class="form-group">
            <label for="webcam_ip">Please type your IP Webcam address: </label>
            <input type="text" class="form-control" id="webcam_ip">
            <button type="button" class="btn btn-success" id="start_button">Start TrackBot</button>
        </div>

        <script>
            var start_button = document.getElementById('start_button');
            start_button.addEventListener('click', function(event) {
                var webcam_ip = document.getElementById('webcam_ip').value;
                window.location.href = "http://localhost:5000/?webcam_ip=" + webcam_ip;
            });
        </script>

    </body>
</html>
"""

class DNSQuery:
  def __init__(self, data):
    self.data = data
    self.domain = ''

    # print("Reading datagram data...")
    m = data[2]
    tipo = (m >> 3) & 15
    if tipo == 0:
      ini = 12
      lon=data[ini]
      while lon != 0:
        self.domain += data[ini + 1:ini + lon + 1].decode("utf-8") + '.'
        ini += lon + 1
        lon = data[ini]

  def resp(self, ip):
    packet = b''
    # print("Resposta {} == {}".format(self.domain, ip))
    if self.domain:
      packet += self.data[:2] + b"\x81\x80"
      packet += self.data[4:6] + self.data[4:6] + b'\x00\x00\x00\x00'
      packet += self.data[12:]
      packet += b'\xc0\x0c'
      packet += b'\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'
      packet += bytes(map(int,ip.split('.')))
    return packet

def start():

    # DNS Server
    ip=ap.ifconfig()[0]
    # print('DNS Server: dom.query. 60 IN A {:s}'.format(ip))

    udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udps.setblocking(False)
    udps.bind(('',53))

    # Web Server
    s = socket.socket()
    ai = socket.getaddrinfo(ip, 80)
    # print("Web Server: Bind address info:", ai)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    s.settimeout(1)
    # print("Web Server: Listening http://{}:80/".format(ip))

    counter = 0
    host = '' 

    while 1:
       

        # DNS Loop
        # print("Before DNS...")
        try:
            data, addr = udps.recvfrom(1024)
            # print("incomming datagram...")
            p=DNSQuery(data)
            udps.sendto(p.resp(ip), addr)
            host = p.domain[:-1]
            # print('Replying: {:s} -> {:s}'.format(p.domain, ip))
        except:
            pass
            # print("No dgram")

        # Web loop
        # print("before accept...")
        # print(host)
        if host != 'mytrackbot.io':
        	# print('Skipping: datagram is not for mytrackbot.io')
        	time.sleep_ms(500)
        	continue
        else:
            print('Accepting datagram for mytrackbot.io')

        try:
            res = s.accept()
            client_sock = res[0]
            client_addr = res[1]
            # print("Client address:", client_addr)
            # print("Client socket:", client_sock)

            client_stream = client_sock

            # print("Request:")
            req = client_stream.readline()
            print(req)
            while True:
                h = client_stream.readline()
                if h == b"" or h == b"\r\n" or h == None:
                    break
                print(h)

            # client_stream.write(CONTENT.format(ai[:-1] + '3'))
            client_stream.write(CONTENT)

            client_stream.close()
            counter += 1

        except:
        	pass
            # print("timeout for web... moving on...")
        # print("loop")
        time.sleep_ms(200)

    udps.close()