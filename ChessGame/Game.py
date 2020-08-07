#!/usr/bin/env python
# coding: utf-8


import imutils
import cv2
import argparse
import chess
from ChessEng import ChessEng
from initialize_Board import initialize_Board
from Board import Board
from Camera import Camera


class Game:
	'''
	This class holds Game information interacting with the Board and Chess Engine
	'''
    
	def __init__(self, test_flag):
		'''
		Initializes Game object	and creates several boolean values regarding game's status
		Sets game winner as place holder
		'''
		self.over = False
		self.ReadyGoMoveError = False
		self.PlayerMoveError = False
		self.isCheck = False
		self.winner = ""
		self.test_flag = test_flag
        
	def setUp(self):
		'''
		Initializes objects with which the Game will interact
		'''	
		self.camera = Camera(self.test_flag)
		self.chessEngine = ChessEng()
		self.board = 0
		self.current = 0   # image
		self.previous = 0  # image
		self.ReadyGoLastMove = "0"
		print('controller.game.setUp() Successfully ')
        
	def analyzeBoard(self):
		'''
		Calls initialize_Board to take image and initialize Board
		'''
		boardRec = initialize_Board(self.camera,self.test_flag)
		self.board = boardRec.create_board()
		self.board.assignState()
		print('controller.game.analyzeBoard() Successfully ')
        
	def checkBoardIsSet(self):
		'''
		Takes inital picture of set board
		'''	
		self.current = self.camera.takePicture()
		if self.test_flag:
			img = cv2.imread("./test_image/board_set.bmp")
			image = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
			image = imutils.resize(image, width=500, height = 500)
			self.current = image
		print('controller.game.checkBoardIsSet() Successfully')
              
	def playerMove(self):
		'''
		Compares previous Board to current board to determine the movement made by the player
		'''
		self.previous = self.current

		self.current = self.camera.takePicture()
		if self.test_flag:
			img = cv2.imread("./test_image/board_set.bmp")
			image = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
			image = imutils.resize(image, width=500, height = 500)
			self.previous = image
            
			img = cv2.imread("./test_image/test_move1.bmp")
			image = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
			image = imutils.resize(image, width=500, height = 500)
			self.current = image           
		move = self.board.determineChanges(self.previous,self.current)
		print(move)
        

            
		code = self.chessEngine.updateMove(move)
		if code == 1:
			# illegal move prompt GUI to open Player Move Error Page
			self.PlayerMoveError = True
		else:
			self.PlayerMoveError = False

		# check for Game Over
		if  self.chessEngine.engBoard.is_checkmate():
			self.winner = "You win!"
			self.over = True
            

	def ReadyGoMove(self):
		'''
		Gets the ReadyGo Move from the chess engine 
		'''	

		# get move from chess engine
		self.ReadyGoLastMove = self.chessEngine.feedToAI()

		# if check，GUI will open Check Window alerting user
		self.isCheck = self.chessEngine.engBoard.is_check()

		# Check Game Over
		if self.chessEngine.engBoard.is_checkmate():
			self.winner = "ReadyGo Wins!"
			self.over = True

		return self.ReadyGoLastMove
    
	def updateCurrent(self):
		'''
		Compares previous image of the board to the current picture to update.
		Ensures player has moved the ReadyGo piece properly
		'''
		self.previous = self.current
		self.current = self.camera.takePicture()

		# determine move
		move = self.board.determineChanges(self.previous, self.current)
		move = chess.Move.from_uci(move)

		# Ensure player has moved the ReadyGo piece properly
		if move == self.ReadyGoLastMove:
			self.ReadyGoMoveError = False
		else:
			# GUI will open ReadyGoMoveError Page
			self.ReadyGoMoveError = True
		
		if self.test_flag:
			self.ReadyGoMoveError = False
'''
	def playerPromotion(self, move):

#!!		Compares previous Board to current board to determine the movement made by the player

		
		print(move)
		code = self.chessEngine.updateMove(move)
		if code == 1:
			# illegal move prompt GUI to open PlayerMoveError Page
			print("Error")
			self.PlayerMoveError = True
		else:
			self.PlayerMoveError = False
			
			# write to Game.txt file
			f = open("Game.txt", "a+")
			f.write(chess.Move.from_uci(move).uci() + "\r\n")
			f.close()

		# check Game Over
		if  self.chessEngine.engBoard.is_checkmate():
			self.winner = "You win!"
			self.over = True
'''


# In[ ]:




