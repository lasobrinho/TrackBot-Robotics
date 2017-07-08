import socket

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
		<div>
			<ol>
				<li>Install IP Webcam app from Google Play</li>
				<li>Connect your phone to the WiFi network named <b>TrackBot WiFi</b> (password: <u>mytrackbot</u>)</li>
				<li>Open IP Webcam app and start the server</li>
				<li>Get the <b>IP address</b> for you IP Webcam server</li>
				<li>Enter the <b>IP address</b> in the field below and click <b>Start TrackBot</b></li>
				<li>All set! The TrackBot management page will appear automatically.</li>
			</ul>
		</div>
		<br>
		<div>
			Please enter your IP Webcam address: 
			<input type="text" id="webcam_ip" value="192.168.4.3">
			<br>
			<button type="button" id="start_button">Start TrackBot</button>
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

def show():
	s = socket.socket()

	ai = socket.getaddrinfo("0.0.0.0", 80)
	addr = ai[0][-1]

	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(addr)
	s.listen(5)
	print()
	print('--------------------------------------------------------------------------------')
	print("Starting configuration page web server, listening on port 8080...")

	while True:
		res = s.accept()
		client_sock = res[0]
		client_addr = res[1]
		print('Connection from', client_addr)

		client_stream = client_sock

		req = client_stream.readline()
		while True:
			h = client_stream.readline()
			if h == b"" or h == b"\r\n":
				break
		print('Sending configuration page...')
		client_stream.write(CONTENT)

		client_stream.close()
		print('Web server closed...')
		print('--------------------------------------------------------------------------------')
		print()

		break

