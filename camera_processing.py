import cv2
import zbar
from PIL import Image
import numpy as np
import socket
import urllib

def sendUDPpackage(message, ip, port):
	UDP_IP = ip
	UDP_PORT = port
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.sendto(message, (UDP_IP, UDP_PORT))

def receiveUDPpackage(port):
	UDP_PORT = port
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(("", UDP_PORT))
	while 1:
		data, addr = s.recvfrom(1024)
		print data
		return data

def get_frame(webcam_ip, webcam_port):
	url = 'http://{}:{}/shot.jpg'.format(webcam_ip, str(webcam_port))
	req = urllib.urlopen(url)
	arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
	img = cv2.imdecode(arr, -1)
	return img

scanner = zbar.ImageScanner()
scanner.parse_config('enable')
face_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')

def process_video(webcam_ip, webcam_port=8080, tb_ip='192.168.4.1', tb_port=8787, feature='qrcode', hw_test=False):

	message = None
	rect_center = None
	detection = False

	img = get_frame(webcam_ip, webcam_port)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	center = (img.shape[1]/2, img.shape[0]/2)
	cv2.circle(img, center, 3, (0, 255, 0), 1)

	if feature == 'face':
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)

		for (x, y, w, h) in faces:
			detection = True
			cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
			rect_center = (x + w/2, y + h/2)
			cv2.circle(img, rect_center, 3, (255, 0, 0), 1)
			cv2.line(img, center, rect_center, (0, 255, 0))
			break

	if feature == 'qrcode':
		pil = Image.fromarray(gray)
		width, height = pil.size
		raw = pil.tobytes()
		image = zbar.Image(width, height, 'Y800', raw)
		scanner.scan(image)
		
		for symbol in image:
			detection = True
			cv2.rectangle(img, symbol.location[0], symbol.location[2], (255, 0, 0), 2)
			x = symbol.location[0][0]
			y = symbol.location[0][1]
			w = symbol.location[2][0] - symbol.location[0][0]
			h = symbol.location[2][1] - symbol.location[0][1]
			rect_center = (x + w/2, y + h/2)
			cv2.circle(img, rect_center, 3, (255, 0, 0), 1)
			cv2.line(img, center, rect_center, (0, 255, 0))
			break

	cmd = {}
	if detection:
		x_distance = center[0] - rect_center[0]
		y_distance = center[1] - rect_center[1]
		message = str(x_distance) + ',' + str(y_distance)
		cmd['delta_x'] = x_distance
		cmd['delta_y'] = y_distance

		if hw_test:
			# Send UDP package with the cmd message
			if message == None:
				message = '0,0'
			sendUDPpackage(message, tb_ip, tb_port)
			if receiveUDPpackage(tb_port) != "acknowledged":
				print("Error: receiveUDPpackage() != \"acknowledged\"")
				return

	ret_enc, jpeg = cv2.imencode('.jpg', img)
	return cmd, jpeg.tobytes()
