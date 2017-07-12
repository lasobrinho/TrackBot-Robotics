#!/usr/bin/env python

from flask import Flask, render_template, Response, request
import camera_processing
import time
import socket, json, sys
import urllib
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkeyqwerty'
socketio = SocketIO(app)

webcam_ip = ''
detectionType = 'qrcode'
detect = 'stop_detection'
detectToggle = {
	'start_detection': True,
	'stop_detection': False
}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host, port = '192.168.4.1', 8787
s.connect((host, port))

commandThreshold = 25
sendCounter = 0
sendFreq = 50
minSendFreq = 10

@app.route('/')
def index():
	global webcam_ip
	webcam_ip = str(request.args.get('webcam_ip'))
	return render_template('index.html')

def adjustSendCounter(absDeltaX):
	global sendFreq
	absDiff = abs(commandThreshold - absDeltaX)
	sendFreq = 50 - absDiff
	if sendFreq < minSendFreq:
		sendFreq = minSendFreq

def sendJSON(cmd, s):
	m = json.dumps(cmd)
	s.sendall(m)

def gen():
	global webcam_ip
	global s
	global sendCounter

	url = 'http://{}:{}/video'.format(webcam_ip, str(8080))
	stream = urllib.urlopen(url)

	while True:
		cmd, frame = camera_processing.process_video(stream, feature=detectionType, detect=detectToggle[detect])
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
		if sendCounter % sendFreq == 0:
			if cmd:
				absDeltaX = abs(cmd['delta_x'])
				if absDeltaX > commandThreshold:
					adjustSendCounter(absDeltaX)
					sendJSON(cmd, s)
					sendCounter = 0
		sendCounter += 1

@app.route('/video_feed')
def video_feed():
	return Response(gen(),
					mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('change_detection_type')
def handle_change_detection_type(json):
	global detectionType
	detectionType = json['detectionType']

@socketio.on('detection_toggle')
def handle_detection_toggle(json):
	global detect
	detect = json['detect']

@socketio.on('move_command')
def handle_move_command(json):
	global s
	cmd = {}
	cmd['command'] = json['command']
	sendJSON(cmd, s)

@socketio.on('disconnect')
def handle_disconnect():
	s.close()

if __name__ == '__main__':
	socketio.run(app)
