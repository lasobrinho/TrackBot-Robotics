import socket
import sys
import json
import machine
from stepper import Stepper

boardLed = machine.Pin(2, machine.Pin.OUT)
boardLed(1)

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

	stepper = Stepper(64, [14, 12, 13, 15])
	stepper.setSpeed(50)

	while True:
		m = c.recv(1024)
		if not m:
			break
		try: 
			cmd = json.loads(m)
			boardLed(0)
		except:
			continue
		if 'command' in cmd:
			manualCommand = cmd['command']
			if manualCommand == 'move_left':
				stepper.step(-1)
			if manualCommand == 'move_right':
				stepper.step(1)
		else:
			deltaX, deltaY = cmd['delta_x'], cmd['delta_y']
			if deltaX > 0:
				stepper.step(1)
			else:
				stepper.step(-1)
		boardLed(1)

	c.close()
	s.close()
	print('Robot control server closed...')
	print('--------------------------------------------------------------------------------')
	print()

