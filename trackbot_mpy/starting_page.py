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
		<div class="form-group">
			<label for="webcam_ip">Please type your IP Webcam address: </label>
			<input type="text" class="form-control" id="webcam_ip" value="192.168.4.">
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

def show():
	s = socket.socket()

	ai = socket.getaddrinfo("0.0.0.0", 80)
	print("Bind address info:", ai)
	addr = ai[0][-1]

	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(addr)
	s.listen(5)
	print("Listening, connect your browser to http://{<this_host>}:8080/")

	while True:
		res = s.accept()
		client_sock = res[0]
		client_addr = res[1]
		print("Client address:", client_addr)
		print("Client socket:", client_sock)

		client_stream = client_sock

		print("Request:")
		req = client_stream.readline()
		print(req)
		while True:
			h = client_stream.readline()
			if h == b"" or h == b"\r\n":
				break
			print(h)
		client_stream.write(CONTENT)

		client_stream.close()
		print()

		break

