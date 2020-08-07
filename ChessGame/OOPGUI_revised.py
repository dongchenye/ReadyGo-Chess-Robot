#!/usr/bin/env python
# coding: utf-8

#!/usr/bin/env python
# coding: utf-8
import sys
from PIL import ImageTk, Image
import PIL.Image
import copy
import tkinter as tk
from tkinter import *
from Game import Game
from Speaker import Speaker
# set font sizes
LARGE_FONT = ("system", 20)
MED_FONT = ("system", 15)
SMALL_FONT = ("system", 10)

BOLD_LAR_FONT=('Helvetica', 25, 'bold')
BOLD_MED_FONT = ('Helvetica',18 , 'bold')

test_flag = True

class Application(tk.Tk):
	'''
	This class controls the Graphical User Interface
	'''
	def __init__(self,*args, **kwargs):

		tk.Tk.__init__(self,*args,**kwargs)
		container = tk.Frame(self)

		container.pack(side = "top", fill = "both", expand = True)

		container.grid_rowconfigure(0,weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		self.frames = {}
        
		self.speaker = Speaker(True)
        
		self.game = Game(test_flag)
        
		self.ReadyGoColor = StringVar()
		self.PlayerColor= StringVar()
        
		# holds ReadyGo move information to be displayed in ReadyGoMovePage
		self.move = StringVar()
		self.move.set( "e2e4")
		# holds winner information to be displayed in GameOverPage
		self.winner = StringVar()
		self.winner.set("ReadyGo Wins!")

		# Give page objects to Application to show frame
        
		for F in (StartGamePage, InitializeBoardPage,SetBoardPage,
				ChooseDifficultyPage,ChooseColorPage,GamePage,ChessGui):

			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row = 0, column = 0, sticky = "nsew")

		self.show_frame(StartGamePage)


	def show_frame(self,cont):
		'''
		Raises frame to top, displaying it as the current window
		'''

		frame = self.frames[cont]
		frame.tkraise()

class StartGamePage(tk.Frame):
	'''
	Prompts user to Start New Game
	'''

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		
		# set label
		label = tk.Label(self,text = "Checkmates: ReadyGo Chess Game", font = LARGE_FONT)
		label.pack(pady = 20, padx = 20)

		# set button that takes you to InitializeBoardPage and calls Game.setUp()
		startGameButton = tk.Button(self, text = "Start New Game",font = MED_FONT,
						command = lambda: [controller.show_frame(InitializeBoardPage), controller.game.setUp()])
		startGameButton.pack()


                
class InitializeBoardPage(tk.Frame):
	'''
	Prompts player to clear board so the board may be initialized
	'''

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text = "Clear Board for Initialization", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)
		initBoardButton = tk.Button(self, text = "Done",font = MED_FONT, command = lambda : [controller.show_frame(SetBoardPage), controller.game.analyzeBoard()])

		initBoardButton.pack()



class SetBoardPage(tk.Frame):
	'''
	Prompts user to set board after initialization
	'''

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)

		# set label
		label = tk.Label(self,text = "Game Initialization Done. Set Board", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)

		# set button that takes you to ChooseDifficultyPage and has Game take a picture of the set Board
		setBoardButton = tk.Button(self, text = "Done",font = MED_FONT,
						 command = lambda : [controller.show_frame(ChooseDifficultyPage),controller.game.checkBoardIsSet()])

		setBoardButton.pack()



class ChooseDifficultyPage(tk.Frame):
	'''
	Prompts user to pick a difficulty for the chess engine
	'''

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		label = tk.Label(self,text = "Choose the difficulty")
		label.pack(pady = 10, padx = 10)

		EasyButton = tk.Button(self, text = "Easy",
						command = lambda : [self.setEasy(controller), controller.show_frame(ChooseColorPage)])
		EasyButton.pack()

		IntermediateButton = tk.Button(self, text = "Intermediate",
						command = lambda : [self.setIntermediate(controller), controller.show_frame(ChooseColorPage)])
		IntermediateButton.pack()

		HardButton = tk.Button(self, text = "Hard",
						command = lambda : [self.setHard(controller), controller.show_frame(ChooseColorPage)])
		HardButton.pack()

	def setEasy(self,controller):
		controller.game.chessEngine.setDifficult(5)

	def setIntermediate(self,controller):
		controller.game.chessEngine.setDifficult(10)

	def setHard(self,controller):
		controller.game.chessEngine.setDifficult(20)
		

        
class ChooseColorPage(tk.Frame):
	'''
	Prompts player to choose color and shows appropriate window for first move
	'''

	def __init__(self,parent,controller):

		tk.Frame.__init__(self,parent)
		
		# set label
		label = tk.Label(self,text = "Which color would you like to play?", font = LARGE_FONT)
		label.pack(pady = 10, padx = 10)

		# set button that takes you to PlayerMovePage since the Player will go first  

		whiteButton = tk.Button(self, text = "White",font = MED_FONT,
					command = lambda: [self.setColor(controller,"White"),controller.show_frame(GamePage)])
		whiteButton.pack()

		# set button that takes you to ReadyGoMovePage since Ready will go first
		# gets a default move from ReadyGo and displays it in the next window

		blackButton = tk.Button(self, text = "Black",font = MED_FONT,
					command = lambda : [self.setColor(controller,"Black"),controller.move.set(controller.game.ReadyGoMove()),controller.show_frame(GamePage)])
		blackButton.pack()
                                       
	def setColor(self,controller,color):
		if color == "White":
			controller.PlayerColor.set("Player's color: White")                              
			controller.ReadyGoColor.set("ReadyGo's color: Black") 
		else:
			controller.PlayerColor.set("Player's color: Black")                                     
			controller.ReadyGoColor.set("ReadyGo's color: White") 
		print(controller.PlayerColor.get())
          

        
class GamePage(tk.Frame):
    
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		self.chessGui = ChessGui(self,controller)
        
		self.PlayerColorText = controller.PlayerColor.get()
		self.ReadyGoColorText = controller.ReadyGoColor.get()
        
		self.BeginGameButton = tk.Button(self, text = "Begin the Game!",font = LARGE_FONT,command = lambda : [self.ProcessGame(controller)])
		self.BeginGameButton.pack()
        
		self.Mainlabel = tk.Label(self, text = "Main Game", font = BOLD_LAR_FONT)
        
		# set color label with current color played 
		self.colorlabel = tk.Label(self, text= "", font = MED_FONT)
        
		# set label
		self.label = tk.Label(self,text = "", font = BOLD_MED_FONT)

		# set dynamic label with ReadyGo move
		self.moveLabel = tk.Label(self, textvariable = controller.move, font = BOLD_MED_FONT)      
        
		# set button that updates player move and checks the moves validity and board circumstances
		self.DoneButton = tk.Button(self, text = "Done",font = MED_FONT)

		self.ResignButton = tk.Button(self, text = "Resign",font = MED_FONT,command = lambda : [controller.speaker.GameOver(controller.winner.get()),self.GameOverWindow(controller)])        

        
	def ProcessGame(self,controller):  

		self.BeginGameButton.pack_forget()
		self.Mainlabel.grid(row=0, column=1,columnspan=18)
		self.colorlabel.grid(row=5, column=1,columnspan=8)
		self.label.grid(row=6, column=1,columnspan=8)        
		self.moveLabel.grid(row=7, column=1,columnspan=5) 
		self.DoneButton.grid(row=8, column=3) 
		self.ResignButton.grid(row=8, column=4) 
		self.chessGui.grid(row=4, column=10,columnspan=9, rowspan=9,sticky=W+E+N+S)         
 
		self.chessGui.InitializeBoard() 
        
		self.turn = ''
		color = controller.PlayerColor.get()
		if color[-5:] == "White":
			self.turn = 'Player'
		else:
			self.turn = 'ReadyGo'

		if self.turn == 'Player':
			self.colorlabel.configure(text = controller.PlayerColor.get())
			self.label.configure(text = "Your Turn") 
			controller.move.set("")
			self.DoneButton.config(command = lambda :[controller.game.playerMove(),self.checkPlayerValid(controller),self.LoopGame(controller)])
            
			self.ResignButton.configure(state=NORMAL)
            
		else:
			self.colorlabel.configure(text = controller.ReadyGoColor.get())
			self.label.configure(text = "ReadyGo Move:") 
			self.DoneButton.config(command = lambda : [controller.game.updateCurrent(), self.checkReadyGoValid(controller),self.LoopGame(controller)])            
			self.ResignButton.configure(state=DISABLED)

	def LoopGame(self,controller):
		if controller.game.over:
			return
		if self.turn == 'Player':
			'''
			Prompts player to move
			'''
			if controller.game.isCheck:
				'''
				Alerts user they are in check
				'''
				controller.speaker.inCheck()      
			self.colorlabel.configure(text = controller.PlayerColor.get())
			self.label.configure(text = "Your Turn") 
			controller.move.set("")
 
			self.DoneButton.config(command = lambda :[controller.game.playerMove(),self.checkPlayerValid(controller),self.LoopGame(controller)])
            
			self.ResignButton.configure(state=NORMAL)
            
		else:
			'''
			Displays chess engine move and prompts user to move piece
			'''
			self.colorlabel.configure(text = controller.ReadyGoColor.get())
			self.label.configure(text = "ReadyGo Move:") 
			self.moveLabel.configure(textvariable = controller.move)             
			self.DoneButton.config(command = lambda : [controller.game.updateCurrent(), self.checkReadyGoValid(controller),self.LoopGame(controller)])            
			self.ResignButton.configure(state=DISABLED)
            
	def checkPlayerValid(self,controller):
		'''
		Performs various checks on move validity and board circumstances.
		Shows the appropriate window given the conditions
		'''

		if controller.game.over:
			controller.winner.set(controller.game.winner)
			controller.speaker.GameOver(controller.winner.get())  
			self.GameOverWindow(controller)
            
		elif controller.game.PlayerMoveError:
			controller.game.current = controller.game.previous
			controller.speaker.PlayerMoveError()
			self.PlayerMoveErrorWindow()
		else:
			print('\nPlayer move: ',controller.game.chessEngine.PlayerLastMove)
			print(controller.game.chessEngine.engBoard)
			controller.move.set(controller.game.ReadyGoMove())
			playermove = str(controller.game.chessEngine.PlayerLastMove)
			self.chessGui.MovePieceUpdate(playermove)
			self.turn = 'ReadyGo'      

	def checkReadyGoValid(self,controller):
		'''
		Performs various checks on move validity and board circumstances.
		Shows the appropriate window given the conditions
		'''     
		if controller.game.over:
			controller.winner.set(controller.game.winner)
			controller.speaker.GameOver(controller.winner.get()) 
			self.GameOverWindow(controller)
			self.turn = 'Player'
            
		elif controller.game.ReadyGoMoveError:
			controller.game.current = controller.game.previous
			controller.speaker.ReadyGoMoveError()
			self.ReadyGoMoveErrorWindow()     
		else:
			print('\nReadyGo move: ',controller.game.chessEngine.ReadyGoLastMove)
			print(controller.game.chessEngine.engBoard)
			readyGomove = str(controller.game.chessEngine.ReadyGoLastMove)
			self.chessGui.MovePieceUpdate(readyGomove)          
			self.turn = 'Player'          
      
	def ReadyGoMoveErrorWindow(self):
		popup = tk.Tk()
		popup.wm_title("ReadyGo Move Error Window")
		label = tk.Label(popup, text="That was not the correct ReadyGo move.", font=LARGE_FONT)
		label.pack(pady = 10, padx = 10)
		B1 = tk.Button(popup, text="Try Again", font = MED_FONT, command = popup.destroy)
		B1.pack()
		popup.mainloop()
        
	def PlayerMoveErrorWindow(self):
		popup = tk.Tk()
		popup.wm_title("Player Move Error Window")
		label = tk.Label(popup, text="Error Invalid Move", font=LARGE_FONT)
		label.pack(pady = 10, padx = 10)
		B1 = tk.Button(popup, text="Try Again", font = MED_FONT, command = popup.destroy)
		B1.pack()
		popup.mainloop() 
        
	def GameOverWindow(self,controller):
		'''
		Shows the winner of the game
		''' 
		self.colorlabel.configure(text = "")
		self.label.configure(text = "Game Over") 
		self.moveLabel.configure(textvariable = controller.winner)             
		self.DoneButton.grid_remove()       
		self.ResignButton.grid_remove()
            

class ChessGui(tk.Frame):
    
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        
        self.B_SQUARE = PIL.Image.open("./image/grnSquare_64.png")
        self.W_SQUARE = PIL.Image.open("./image/whtSquare_64.png")

        self.B_PAWN = PIL.Image.open("./image/b_pawn.png") #21
        self.B_ROOK = PIL.Image.open("./image/b_rook.png") #22
        self.B_KNIGHT = PIL.Image.open("./image/b_knight.png") #23
        self.B_BISHOP = PIL.Image.open("./image/b_bishop.png")#24
        self.B_QUEEN = PIL.Image.open("./image/b_queen.png")#25
        self.B_KING = PIL.Image.open("./image/b_king.png")#26

        self.W_PAWN = PIL.Image.open("./image/w_pawn.png") #11
        self.W_ROOK = PIL.Image.open("./image/w_rook.png") #12
        self.W_KNIGHT = PIL.Image.open("./image/w_knight.png") #13
        self.W_BISHOP = PIL.Image.open("./image/w_bishop.png") #14
        self.W_QUEEN = PIL.Image.open("./image/w_queen.png") #15
        self.W_KING = PIL.Image.open("./image/w_king.png") #16
        
        #a 2d array that has a 1 if it is a black square and 0 if white
        self.boardSquares = [[0 for i in range(8)] for j in range(8)]
        self.gameState = [[0 for i in range(8)] for j in range(8)]
        
    def PopulateboardSquares(self):
        #for populating boardSquares
        for row in range(8):
            tempCheck = (row + 1) % 2 == 0
            for column in range(8):
                if tempCheck:
                    if (column+1) % 2 != 0:
                        self.boardSquares[row][column] = 1
                    else:
                        self.boardSquares[row][column] = 0
                else:
                    if (column+1) % 2 == 0:
                        self.boardSquares[row][column] = 1
                    else:
                        self.boardSquares[row][column] = 0

    def PopulateStartingGameState(self):
        for i in range(8):
            self.gameState[1][i] = self.B_PAWN
            self.gameState[6][i] = self.W_PAWN

        #rooks
        self.gameState[0][0] = self.B_ROOK
        self.gameState[0][7] = self.B_ROOK
        self.gameState[7][0] = self.W_ROOK
        self.gameState[7][7] = self.W_ROOK

        #knights
        self.gameState[0][1] = self.B_KNIGHT
        self.gameState[0][6] = self.B_KNIGHT
        self.gameState[7][1] = self.W_KNIGHT
        self.gameState[7][6] = self.W_KNIGHT

        #bishops
        self.gameState[0][2] = self.B_BISHOP
        self.gameState[0][5] = self.B_BISHOP
        self.gameState[7][2] = self.W_BISHOP
        self.gameState[7][5] = self.W_BISHOP

        #queens
        self.gameState[0][3] = self.B_QUEEN
        self.gameState[7][3] = self.W_QUEEN

        #kings
        self.gameState[0][4] = self.B_KING
        self.gameState[7][4] = self.W_KING
        
    def ConvertPosition(self, position):
        row = 8 - int(position[1])
        col = 0
        if position[0] == 'a':
            col = 0
        if position[0] == 'b':
            col = 1
        if position[0] == 'c':
            col = 2
        if position[0] == 'd':
            col = 3
        if position[0] == 'e':
            col = 4
        if position[0] == 'f':
            col = 5
        if position[0] == 'g':
            col = 6
        if position[0] == 'h':
            col = 7
        return row, col

    def MovePieceUpdate(self, move):
        fromRow, fromColum = self.ConvertPosition(move[:2])
        state = self.gameState[fromRow][fromColum] 

        #White short side castle
        if move == "e1g1" and state == self.W_KING :
            self.MovePiece(move[:2], move[-2:])
            self.MovePiece("h1", "f1") 

        #White long side castle 
        elif move == "e1c1" and state == self.W_KING :
            self.MovePiece(move[:2], move[-2:])
            self.MovePiece("a1", "d1")

        #Black short side castle	 
        elif move == "e8g8"and state == self.B_KING :
            self.MovePiece(move[:2], move[-2:])
            self.MovePiece("h8", "f8")

        #Black long side castle	
        elif move == "e8c8"and state == self.B_KING :
            self.MovePiece(move[:2], move[-2:])
            self.MovePiece("a8", "d8")
		
        else:
            self.MovePiece(move[:2], move[-2:])  

    def MovePiece(self, fromPos, toPos):
        fromRow, fromColum = self.ConvertPosition(fromPos)
        toRow, toColum = self.ConvertPosition(toPos)
        self.PopualteBoardArea(fromRow, fromColum, 'none')
        self.PopualteBoardArea(toRow, toColum, self.gameState[fromRow][fromColum])
        
        self.gameState[toRow][toColum] = self.gameState[fromRow][fromColum]
        self.gameState[fromRow][fromColum] = 0

    def PopualteBoardArea(self, row, column, chessPiece):
        sqr = copy.copy(self.B_SQUARE) if self.boardSquares[row][column] == 1 else copy.copy(self.W_SQUARE)
        if chessPiece == 'none':
            img = ImageTk.PhotoImage(sqr)
            temp = tk.Label(self, image = img )
            temp.image = img
            temp.grid(row = row, column = column)
        else:
            sqr.paste(chessPiece, (0,0), chessPiece)
            img = ImageTk.PhotoImage(sqr)
            temp = tk.Label(self, image = img )
            temp.image = img
            temp.grid(row = row, column = column)

    def InitializeBoard(self):
        #for creating the state of the game
        self.PopulateStartingGameState()
        self.PopulateboardSquares()
        for row in range(8):
            for column in range(8):
                if row == 6:
                    self.PopualteBoardArea(row, column, self.W_PAWN)
                elif row == 1:
                    self.PopualteBoardArea(row, column, self.B_PAWN)
                else:
                    self.PopualteBoardArea(row, column, 'none')
        self.PopualteBoardArea(0, 0, self.B_ROOK)
        self.PopualteBoardArea(0, 1, self.B_KNIGHT)
        self.PopualteBoardArea(0, 2, self.B_BISHOP)
        self.PopualteBoardArea(0, 3, self.B_QUEEN)
        self.PopualteBoardArea(0, 4, self.B_KING)
        self.PopualteBoardArea(0, 5, self.B_BISHOP)
        self.PopualteBoardArea(0, 6, self.B_KNIGHT)
        self.PopualteBoardArea(0, 7, self.B_ROOK)
        self.PopualteBoardArea(7, 0, self.W_ROOK)
        self.PopualteBoardArea(7, 1, self.W_KNIGHT)
        self.PopualteBoardArea(7, 2, self.W_BISHOP)
        self.PopualteBoardArea(7, 3, self.W_QUEEN)
        self.PopualteBoardArea(7, 4, self.W_KING)
        self.PopualteBoardArea(7, 5, self.W_BISHOP)
        self.PopualteBoardArea(7, 6, self.W_KNIGHT)
        self.PopualteBoardArea(7, 7, self.W_ROOK)



app = Application()
app.mainloop()

