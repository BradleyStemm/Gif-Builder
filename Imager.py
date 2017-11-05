
import sys
import time
import datetime
import numpy as np
import cv2

from sense_hat import SenseHat

class Imager:

	def __init__(self, flashPercentage, rVal, bVal, gVal):
		self.flashPercentage = flashPercentage
		self.rVal = rVal
		self.bVal = bVal
		self.gVal = gVal
		return

	def undistortImage(self):
		criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
		# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
		objp = np.zeros((6*7,3), np.float32)
                objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
		# Arrays to store object points and image points from all the images.
                objpoints = [] # 3d point in real world space
                imgpoints = [] # 2d points in image plane.
		ret, corners = cv2.findChessboardCorners(im, (7,6),None)
		if ret == True:
                	objpoints.append(objp)
                	cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
                        imgpoints.append(corners)

                        # Draw and display the corners
                        cv2.drawChessboardCorners(im, (7,6), corners2,ret)
                        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
                        dist = np.array([-0.13615181, 0.53005398, 0, 0, 0])
                        h,  w = im.shape[:2]
                        newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
                        # undistort
                        dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
                        x,y,w,h = roi
                        dst = dst[y:y+h, x:x+w]
                        cv2.imwrite("U"+ str(self.getTimeStamp()) + ".jpg",dst) # writes image test.bmp to disk
		return

	def ensuredImageCapture(self):
		imageCaptured = False
		while( not imageCaptured):
			cam = cv2.VideoCapture(0)
			if (cam.isOpened()):
				for i in xrange(25):		   	#25 images should be read to allow the camera to adjust to light
					temps, tempim = cam.read() 	# captures image
				s, img = cam.read() 			# captures image
				uniqueTime = str(self.getTimeStamp())
				cv2.imwrite("tempImage.jpg",img)
				im = cv2.imread("tempImage.jpg", 0)
				imageCaptured = True
				#self.undistortImage(im)
			cam.release()
			del(cam)
		return

	def getTimeStamp(self):
		nt = datetime.datetime.now()
    		now = int(datetime.datetime.strptime(str(nt), '%Y-%m-%d %H:%M:%S.%f').strftime("%s"))
    		then = int(datetime.datetime.strptime('09/01/2016', '%d/%m/%Y').strftime("%s"))
    		return (now - then)

	def takePicture(self):
		lights = SenseHat()
		self.lightOn(lights)
		self.ensuredImageCapture()
		self.lightOff(lights)
		return

	def lightOn(self,lights):
		r = int((255 * self.rVal) * self.flashPercentage)
		g = int((255 * self.gVal) * self.flashPercentage)
		b = int((255 * self.bVal) * self.flashPercentage)
		lights.clear((r, g, b))
		return

	def lightOff(self,lights):
		r = 0
		g = 0
		b = 0
		lights.clear((r, g, b))
		return

