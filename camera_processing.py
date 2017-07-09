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

bytes = bytes()

def get_frame(stream):
	global bytes
	bytes += stream.read(1024)
	a = bytes.find(b'\xff\xd8')
	b = bytes.find(b'\xff\xd9')
	if a != -1 and b != -1:
		jpg = bytes[a:b+2]
		bytes = bytes[b+2:]
		img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
		return img
	return None
	

scanner = zbar.ImageScanner()
scanner.parse_config('enable')

hc_methods = {
	'face': cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml'),
	'upperbody': cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_upperbody.xml'),
	'fullbody': cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_fullbody.xml')
}

def process_video(stream, tb_ip='192.168.4.1', tb_port=8787, detect=True, feature='qrcode'):

	message = None
	rect_center = None
	detection = False
	cmd = {}

	img = get_frame(stream)
	while img == None:
		img = get_frame(stream)

	if not detect:
		ret_enc, jpeg = cv2.imencode('.jpg', img)
		return cmd, jpeg.tobytes()

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	center = (img.shape[1]/2, img.shape[0]/2)
	cv2.circle(img, center, 3, (0, 255, 0), 1)

	if feature != "qrcode":
		hc = hc_methods[feature]
		detections = hc.detectMultiScale(gray, 1.3, 5)
		for (x, y, w, h) in detections:
			detection = True
			cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
			rect_center = (x + w/2, y + h/2)
			cv2.circle(img, rect_center, 3, (255, 0, 0), 1)
			cv2.line(img, center, rect_center, (0, 255, 0))
			break
	else:
		pil = Image.fromarray(gray)
		width, height = pil.size
		raw = pil.tobytes()
		image = zbar.Image(width, height, 'Y800', raw)
		scanner.scan(image)		
		for symbol in image:
			detection = True
			try:
				cv2.rectangle(img, symbol.location[0], symbol.location[2], (255, 0, 0), 2)
			except:
				# cv2.Rectangle tuple error, skipping...
				detection = False
				break
			x = symbol.location[0][0]
			y = symbol.location[0][1]
			w = symbol.location[2][0] - symbol.location[0][0]
			h = symbol.location[2][1] - symbol.location[0][1]
			rect_center = (x + w/2, y + h/2)
			cv2.circle(img, rect_center, 3, (255, 0, 0), 1)
			cv2.line(img, center, rect_center, (0, 255, 0))
			break

	if detection:
		x_distance = center[0] - rect_center[0]
		y_distance = center[1] - rect_center[1]
		message = str(x_distance) + ',' + str(y_distance)
		cmd['delta_x'] = x_distance
		cmd['delta_y'] = y_distance

		# if hw_test:
		# 	# Send UDP package with the cmd message
		# 	if message == None:
		# 		message = '0,0'
		# 	sendUDPpackage(message, tb_ip, tb_port)
		# 	if receiveUDPpackage(tb_port) != "acknowledged":
		# 		print("Error: receiveUDPpackage() != \"acknowledged\"")
		# 		return

	ret_enc, jpeg = cv2.imencode('.jpg', img)
	return cmd, jpeg.tobytes()
