#!/usr/bin/env python

from flask import Flask, render_template, Response, request
import camera_processing
import time

app = Flask(__name__)
webcam_ip = ''

@app.route('/')
def index():
	global webcam_ip
	webcam_ip = str(request.args.get('webcam_ip'))
	return render_template('index.html')

def gen():
	global webcam_ip
	while True:
		frame = camera_processing.process_video(webcam_ip=webcam_ip)
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
	return Response(gen(),
					mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)