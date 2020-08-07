#!/usr/bin/env python
# coding: utf-8


import imutils
import cv2

class Camera:

	img_counter = 0

	def __init__(self,test_flag):
		#placeholder
		self.cam = True
		self.test_flag = test_flag

	def takePicture(self):
		#grab an image from the camera
		image = None
		if self.test_flag:
		# for testing purpose
			img_filename = "image1.jpg" # Read image of clear board
			image = cv2.imread(img_filename)
		else:
			video = cv2.VideoCapture(0)
			while True:
				check, frame = video.read()
				frame = cv2.resize(frame, (500, 500))
				frame = cv2.rotate(frame, cv2.ROTATE_180)
				cv2.imshow("Capturing",frame)

				key = cv2.waitKey(1)
				if key == ord(' '):
					#img_name = "opencvframe{}.jpg".format(Camera.img_counter)
					#cv2.imwrite(f"test_images/{img_name}", frame)
					Camera.img_counter += 1
					frame = cv2.rotate(frame, rotateCode=cv2.ROTATE_90_COUNTERCLOCKWISE)
					image = frame
					break

			video.release()
			cv2.destroyAllWindows
		resized_image = imutils.resize(image, height = 500, width = 500)
		return resized_image

