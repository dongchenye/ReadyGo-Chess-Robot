#!/usr/bin/env python
# coding: utf-8



import chess
import chess.engine

class ChessEng:
	'''
	This class interacts with the stockfish chess engine using the python-chess
	package. All interactions are done with the Universal Chess Interface protocol (UCI)
	'''
	def __init__(self):
		'''
		Creates chessboard, local chess engine stockfish, and initiates UCI protocol
		'''
		self.engBoard = chess.Board()
		self.engine = chess.engine.SimpleEngine.popen_uci("/Users/dongchenye/Downloads/CheckMates-master-2/ChessGame/stockfish-11-64")
		self.depth = 0
		self.PlayerLastMove = ''
		self.ReadyGoLastMove = ''
		print('Chess Engine Created Successfully ')
        
	def setDifficult(self,difficulty):
		'''
		Update the difficulty of the chess Engine
		'''
		self.depth = difficulty
		print('Chess Engine difficulty level (searching depth) : ', difficulty)
        
	def updateMove(self, Playermove):
		'''
		Updates chess board with the move made. Also checks for illegal moves
		'''

		# convert move to UCI format for engine
		self.PlayerLastMove = chess.Move.from_uci(Playermove)
        
		# check legality
		if self.PlayerLastMove not in self.engBoard.legal_moves:
			return 1
		else:
			# update board
			self.engBoard.push(self.PlayerLastMove)
			return 0
        
        
	def feedToAI(self):
		'''
		Gets the bestmove from the stockfish engine. Writes move choice to Game.txt file
		'''

		# giving the CPU the current board position
		self.ReadyGoLastMove = self.engine.play(self.engBoard, chess.engine.Limit(time=0.1,depth=self.depth)).move
        
		# update board
		self.engBoard.push(self.ReadyGoLastMove)
        
		return self.ReadyGoLastMove

