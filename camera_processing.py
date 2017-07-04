import cv2
import zbar
from PIL import Image
import numpy as np
import socket

def sendUDPpackage(message, ip, port):
	UDP_IP = ip
	UDP_PORT = port
	# print "UDP target IP:", UDP_IP
	# print "UDP target port:", UDP_PORT
	# print "message:", message
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

def show_webcam(ip, port=8888, feature='qrcode', mirror=False, hw_test=False):

	scanner = zbar.ImageScanner()
	scanner.parse_config('enable')
	face_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')

	cam = cv2.VideoCapture(0)
	while True:
		message = None
		rect_center = None
		detection = False

		ret_val, img = cam.read()
		if mirror: 
			img = cv2.flip(img, 1)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		center = (img.shape[1]/2, img.shape[0]/2)
		cv2.circle(img, center, 3, (0, 255, 0), 1)

		if feature == 'faces':
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
				# print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
				# print 'location', symbol.location
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

		if detection:
			x_distance = center[0] - rect_center[0]
			y_distance = center[1] - rect_center[1]
			message = str(x_distance) + ',' + str(y_distance)

			if hw_test:
				# Send UDP package with the message
				if message == None:
					message = '0,0'
				sendUDPpackage(message, ip, port)
				if receiveUDPpackage(port) != "acknowledged":
					print("Error: receiveUDPpackage() != \"acknowledged\"")
					return

		cv2.imshow('img',img)

		if cv2.waitKey(1) == ord('q'): 
			break  # esc to quit

	cv2.destroyAllWindows()

def main():
	show_webcam(ip='192.168.1.13')


if __name__ == '__main__':
	main()





