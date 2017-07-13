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
	<style>
		body {
			font-family: verdana;
			margin: auto;
			width: 42%;
			color: #444;
			font-size: 15px;
		}
		h1 {
			color: #777;
			text-align: center;
			font-weight: 400;
		}
		ol {
			line-height: 24px;
		}
		.form {
			text-align: center;
		}
		#webcam_ip {
			width: 120px;
			height: 15px;
			font-size: 15px;
			text-align: center;
			border: 1px solid #FFF;
			border-bottom-color: #BBB;
			color: #444;
		}
		#start_button {
			margin-top: 15px;
			width: 150px;
			height: 32px;
			border: 1px solid;
			border-color: #4cae4c;
			font-size: 14px;
			line-height: 1.42857143;
			color: #FFF;
			border-radius: 4px;
			background-color: #5cb85c;
		}
		.divider {
			background-color: #DDD;
			height: 1px;
		}
	</style>
	<body>

		<h1>TrackBot v1.0</h1>
		<div class="divider"></div>
		<div>
			<ol>
				<li>Execute the <b>TrackBot Server</b> in your computer</li>
				<li>Connect your phone to the WiFi network named <b>TrackBot WiFi</b> (password: <u>mytrackbot</u>)</li>
				<li>Install and open IP Webcam app and start the server</li>
				<li>Get the <b>IP address</b> from your IP Webcam app</li>
				<li>Enter the <b>IP address</b> from IP Webcam app in the field below</li>
				<li>Click <b>Start TrackBot</b></li>
				<li>All set! The TrackBot management page will appear automatically!</li>
			</ul>
		</div>
		<br>
		<div class="divider"></div>
		<br>
		<div class="form">
			Please enter your IP Webcam address: 
			<input type="text" id="webcam_ip" value="192.168.1.22">
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
		s.close()
		print('Web server closed...')
		print('--------------------------------------------------------------------------------')
		print()

		break

