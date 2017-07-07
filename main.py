#!/usr/bin/env python

from flask import Flask, render_template, Response
import camera_processing
import subprocess
import atexit

app = Flask(__name__)
webcam_ip = ''

@app.route('/')
def index():
	webcam_ip = request.arg.get('webcam_ip')
	webcam_process = subprocess.Popen(['./prepare-videochat.sh', webcam_ip], shell=True)
	return render_template('index.html')

def gen():
	while True:
		frame = camera_processing.process_video(ip=webcam_ip)
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
	return Response(gen(),
					mimetype='multipart/x-mixed-replace; boundary=frame')

def finish_webcam_process():
	print('finishing page')
	webcam_process.communicate(input='\n')
	webcam_process.terminate()

atexit.register(finish_webcam_process)

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)