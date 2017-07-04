import cv2

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        ret_val, img = self.video.read()
        return ret_val, img

        #ret, jpeg = cv2.imencode('.jpg', img)
        #return jpeg.tobytes()
