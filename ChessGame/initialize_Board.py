import math
import cv2
import numpy as np
import imutils
from matplotlib import pyplot as plt
from Line import Line
from Square import Square

from Board import Board

class initialize_Board:
	'''
	This class handles the initialization of the board. It analyzes
	the empty board finding its border, lines, corners, squares...
    
	'''

	def __init__(self, camera, test_flag):
		self.cam = camera  
		self.test_flag = test_flag
        
	def create_board(self):
        
		corners = []

		# retake picture until board is initialized properly
        
		while len(corners) < 81:
		# Call the camera to take picture
			image = self.cam.takePicture()
			if self.test_flag:
				img = cv2.imread("./test_image/empty_board.bmp")
				image = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

			image = imutils.resize(image, width=500, height = 500)
			## Find corners
			corners = self.findCorners(image)
            
		# Find squares
		squares = self.findSquares(corners, image)
        
		# create Board
		board = Board(squares,self.test_flag)

		return board
        
        
	def findCorners(self, image):    

		## Clean the Image

		# convert to grayscale
		gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

		# setting all pixels above the threshold value to white and those below to black
		adaptiveThresh = cv2.adaptiveThreshold(gray, 255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 125, 1)
		# Initialize Mask

		# find contours
		contours, hierarchy = cv2.findContours(adaptiveThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		# Create copy of original image
		imgContours = image.copy()

		for c in range(len(contours)):
			# Area
			area = cv2.contourArea(contours[c])
			# Perimenter
			perimeter = cv2.arcLength(contours[c], True)
			#the largest square is always the largest ratio
			if c ==0:
				Lratio = 0
			if perimeter > 0:
				ratio = area / perimeter
				if ratio > Lratio:
					largest=contours[c]
					Lratio = ratio
					Lperimeter=perimeter
					Larea = area
			else:
					pass


		# Draw contours
		cv2.drawContours(imgContours, [largest], -1, (255,0,0), 2)

		epsilon = 0.1 * Lperimeter
		chessboardEdge = cv2.approxPolyDP(largest, epsilon, True)

		# create new all black image
		mask = np.zeros((image.shape[0], image.shape[1]), 'uint8')*125
		# Copy the chessboard edges as a filled white polygon size of chessboard edge
		cv2.fillConvexPoly(mask, chessboardEdge, 255, 1)
		# Assign all pixels that are white (i.e the polygon, i.e. the chessboard)
		extracted = np.zeros_like(image)
		extracted[mask == 255] = image[mask == 255]
		# remove strip around edge
		extracted[np.where((extracted == [125, 125, 125]).all(axis=2))] = [0, 0, 0]

		mask = extracted
		if self.test_flag:
			cv2.imwrite("Mask image.png", mask)

		# Find the Edges
		board_edges = cv2.Canny(mask,400,1000)

		edges = cv2.Canny(mask,200,600) - board_edges

		colorEdges = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)
		

		if self.test_flag:
			cv2.imwrite("Edge image.png", colorEdges)

		# Find the Lines

		lines = cv2.HoughLinesP(edges, 1,  np.pi / 180, 100,np.array([]), 100, 80)
		a,b,c = lines.shape
		for i in range(a):
			cv2.line(colorEdges, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0,255,0),2,cv2.LINE_AA)

		horizontal = []
		vertical = []
		for l in range(a):
			[[x1,y1,x2,y2]] = lines[l]
			newLine = Line(x1,x2,y1,y2)
			if newLine.orientation == 'horizontal':
				horizontal.append(newLine)
			else:
				vertical.append(newLine)
        

		# find corners (Intersection of lines)
		corners = []
		for v in vertical:
			for h in horizontal:
				s1,s2 = v.find_intersection(h)
				corners.append([s1,s2])

		# remove duplicate corners
		dedupeCorners = []
		for c in corners:
			matchingFlag = False
			for d in dedupeCorners:
				if math.sqrt((d[0]-c[0])*(d[0]-c[0]) + (d[1]-c[1])*(d[1]-c[1])) < 20:
					matchingFlag = True
					break
			if not matchingFlag:
				dedupeCorners.append(c)

		for d in dedupeCorners:
			cv2.circle(colorEdges, (d[0],d[1]), 10, (255,0,0))

            
		return dedupeCorners

	def findSquares(self, corners, image):
		'''
		Finds the squares of the chessboard 
		'''
		square_img = image.copy()
        
		corners.sort(key=lambda x: x[1])
		rows = [[],[],[],[],[],[],[],[],[]]
		r = 0
		for c in range(0, 81):
			if c > 0 and c % 9 == 0:
				r = r + 1
			rows[r].append(corners[c])

		letters = ['h','g','f','e','d','c','b','a']
		numbers = ['1','2','3','4','5','6','7','8']
		Squares = []

		# sort corners by column
		for r in rows:
			r.sort(key=lambda y: y[0])
    
		# initialize squares
		for r in range(0,8):
			for c in range (0,8):
				c1 = rows[r][c]
				c2 = rows[r][c + 1]
				c3 = rows[r + 1][c]
				c4 = rows[r + 1][c + 1]

				position = letters[r] + numbers[7-c]
				newSquare = Square(square_img,c1,c2,c3,c4,position)
				newSquare.draw(square_img,(255,0,0),1)
				newSquare.drawROI(square_img,(0,0,255),2)
				newSquare.classify(square_img)
				Squares.append(newSquare)

		if self.test_flag:
			cv2.imwrite("Square image.png", square_img)
        
    
		return Squares
    