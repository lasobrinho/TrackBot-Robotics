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
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host, port = '192.168.4.1', 8787

@app.route('/')
def index():
	global webcam_ip
	webcam_ip = str(request.args.get('webcam_ip'))
	return render_template('index.html')

def sendJSON(cmd, s):
	m = json.dumps(cmd)
	s.sendall(m)

def gen():
	global webcam_ip
	s.connect((host, port))

	url = 'http://{}:{}/video'.format(webcam_ip, str(8080))
	stream = urllib.urlopen(url)

	while True:
		cmd, frame = camera_processing.process_video(stream, feature=detectionType)
		if cmd:
			sendJSON(cmd, s)
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
	s.close()

@app.route('/video_feed')
def video_feed():
	return Response(gen(),
					mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('change_detection_type')
def handle_change_detection_type(json):
	global detectionType
	detectionType = json['detectionType']

if __name__ == '__main__':
	socketio.run(app)
