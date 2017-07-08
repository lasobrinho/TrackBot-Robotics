import socket
import sys
import json
import machine

board_led = machine.Pin(2, machine.Pin.OUT)
board_led(1)

def start_server():
	s = socket.socket()

	host, port = '0.0.0.0', 8787
	s.bind((host, port))
	s.listen(5)

	print()
	print('--------------------------------------------------------------------------------')
	print('Starting robot control server, listening on port 8787...')

	c, addr = s.accept()
	print('Connection from', addr)
	print()

	while True:
		m = c.recv(1024)
		if not m:
			break
		try: 
			cmd = json.loads(m)
			board_led(0)
		except:
			continue
		delta_x, delta_y = cmd['delta_x'], cmd['delta_y']
		board_led(1)

	c.close()
	s.close()
	print('Robot control server closed...')
	print('--------------------------------------------------------------------------------')
	print()

