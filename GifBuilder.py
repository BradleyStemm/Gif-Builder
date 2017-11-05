import os
import sys
import glob
import time
import datetime
import cv2
import Imager
import subprocess
import numpy as np

stateFile = '/home/bradl/webCam/.gifBuilderState'

class GifBuilder:

	tempFile = "tempImage.jpg"
	fileName = "image_"
	fileExt =  ".jpg"
	imageArray = np.empty((30,640,480))

	def __init__(self):
		self.arrayFull = False
		self.arrayMaxSize = 0
		self.size = 0
		self.lastAccessed = "SOME TIME"
		if not os.path.exists(stateFile):
    			os.mknod(stateFile)
			self.arrayFull = False
                        self.arrayMaxSize = 30
                        self.size = 0
                        self.lastAccessed = "Never"
                        file = open(stateFile, 'w')
                        file.close()
                        self.saveState()
		else:
			self.loadState()
		return

	def addImage(self):
		self.shiftImages()
		self.addNames()
		self.saveImages()
		imageAgent = Imager.Imager(1.0, 1.0, 1.0, 1.0)
		imageAgent.takePicture()
		imageToAdd = cv2.imread(self.tempFile, 0)
		self.imageArray.append(imageToAdd)
		if self.size < 30:
			self.size = self.size + 1
		nt = datetime.datetime.now()
                self.lastAccessed = datetime.datetime.strptime(str(nt), '%Y-%m-%d %H:%M:%S.%f').strftime("%s")
		if self.size == self.arrayMaxSize:
			self.arrayFull = True
		self.buildGif()
		self.saveState()
		return

	def shiftImages(self):
		for index in range(self.arrayMaxSize - 1,1):
			temp = imageArray[index-1]
			imageArray[index] = temp
		return

	def addNames(self):
		#bashCommand = "sudo rm * .jpg"
		#process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
		process = subprocess.Popen(["sudo", "rm"] + glob.glob("*" + ".jpg"),stdout=subprocess.PIPE)
		output, error = process.communicate()
		for index in range(self.arrayMaxSize,1):
			cv2.imwrite(self.filename + str(index + 1) + self.fileExt ,img)
		return

	def buildGif(self):
		return

	def saveImages(self):
		for index in range(0,self.size-1):
                        cv2.imwrite(self.fileName + str(index + 1) + self.fileExt ,self.imageArray[index])
		return

	def loadImages(self):
		for index in range(0,self.arrayMaxSize-1):
			np.append(self.imageArray, cv2.imread(self.fileName + str(index) + self.fileExt, 0))
		return

	def saveState(self):
		file=open(stateFile,'w+')
		file.write("ArrayFull: " + str(self.arrayFull) + "\n")
		file.write("ArrayMaxSize: " + str(self.arrayMaxSize) + "\n")
		self.saveImages()
                file.write("Size: " + str(self.size) + "\n")
                file.write("LastAccessed: " + str(self.lastAccessed) + "\n")
                file.close()
		return

	def loadState(self):
		file=open(stateFile, 'r')

		if str(self.retrieveStateVar(file,"ArrayFull:")) == "False":
			self.arrayFull = False
		else:
			self.arrayFull = True
                self.arrayMaxSize = int(self.retrieveStateVar(file, "ArrayMaxSize:"))
                self.imageArray = self.loadImages()
                self.size = int(self.retrieveStateVar(file,"Size:"))
                self.lastAccessed = str(self.retrieveStateVar(file,"LastAccessed:"))
		self.loadImages()
		file.close()
		return

	def retrieveStateVar(self, afile, attributeName):
		input = afile.readline()
		brokenUp = input.split(' ')
		while brokenUp[0] != attributeName:
			input = afile.readline()
	                brokenUp = input.split(' ')
                secondItem = brokenUp[1]
	        a = secondItem.replace("\n","")
		return a

def main():
	gifBuilderInstance = GifBuilder()
	gifBuilderInstance.addImage()
	return

main()
