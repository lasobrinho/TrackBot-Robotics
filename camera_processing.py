import cv2
import numpy as np
import socket

def sendUDPpackage(message):
	UDP_IP = "192.168.0.50"
	UDP_PORT = 5005
	# print "UDP target IP:", UDP_IP
	# print "UDP target port:", UDP_PORT
	# print "message:", message
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.sendto(message, (UDP_IP, UDP_PORT))

def show_webcam(mirror=False):
	face_cascade = cv2.CascadeClassifier('/Users/lucas/opencv/data/haarcascades/haarcascade_frontalface_default.xml')

	cam = cv2.VideoCapture(0)
	while True:
		ret_val, img = cam.read()
		if mirror: 
			img = cv2.flip(img, 1)
		# cv2.imshow('my webcam', img)

		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		
		center = (img.shape[1]/2, img.shape[0]/2)
		cv2.circle(img, center, 3, (0, 255, 0), 1)

		message = None

		for (x, y, w, h) in faces:
			cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
			rect_center = (x + w/2, y + h/2)
			cv2.circle(img, rect_center, 3, (255, 0, 0), 1)
			cv2.line(img, center, rect_center, (0, 255, 0))
			
			x_distance = center[0] - rect_center[0]
			y_distance = center[1] - rect_center[1]
			message = str(x_distance) + ',' + str(y_distance)
			break

		cv2.imshow('img',img)

		# Send UDP package with the message
		if message == None:
			message = '0,0'
		sendUDPpackage(message)

		if cv2.waitKey(1) == 27: 
			break  # esc to quit

	cv2.destroyAllWindows()

def main():
	show_webcam(mirror=True)


if __name__ == '__main__':
	main()





