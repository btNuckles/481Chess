#! /usr/bin/env python
"""
 Project: Python Chess
 File name: PythonChessMain.py
 Description:  Chess for player vs. player, player vs. AI, or AI vs. AI.
	Uses Tkinter to get initial game parameters.  Uses Pygame to draw the 
	board and pieces and to get user mouse clicks.  Run with the "-h" option 
	to get full listing of available command line flags.  
	
 Copyright (C) 2009 Steve Osborne, srosborne (at) gmail.com
 http://yakinikuman.wordpress.com/
 *******
 This program is free software; you can redistribute it and/or modify 
 it under the terms of the GNU General Public License as published by 
 the Free Software Foundation; either version 2 of the License, or 
 (at your option) any later version.
 
 This program is distributed in the hope that it will be useful, but 
 WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
 or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License 
 for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.

 *******
 Version history:

 v 0.7 - 27 April 2009.  Dramatically lowered CPU usage by using 
   "pygame.event.wait()" rather than "pygame.event.get()" in
   ChessGUI_pygame.GetPlayerInput().
 
 v 0.6 - 20 April 2009.  Some compatibility fixes: 1) Class: instead of 
   Class(), 2) renamed *.PNG to *.png, 3) rendered text with antialias flag on.  
   Also changed exit() to sys.exit(0). (Thanks to tgfcoder from pygame website 
   for spotting these errors.)
 
 v 0.5 - 16 April 2009.  Added new AI functionality - created 
   "ChessAI_defense" and "ChessAI_offense."  Created PythonChessAIStats 
   class for collecting AI vs. AI stats.  Incorporated Python module 
   OptionParser for better command line parsing.
   
 v 0.4 - 14 April 2009.  Added better chess piece graphics from Wikimedia
   Commons.  Added a Tkinter dialog box (ChessGameParams.py) for getting
   the game setup parameters.  Converted to standard chess notation for 
   move reporting and added row/col labels around the board.
 
 v 0.3 - 06 April 2009.  Added pygame graphical interface.  Includes
   addition of ScrollingTextBox class.
   
 v 0.2 - 04 April 2009.  Broke up the program into classes that will
   hopefully facilitate easily incorporating graphics or AI play.
 
 v 0.1 - 01 April 2009.  Initial release.  Draws the board, accepts
   move commands from each player, checks for legal piece movement.
   Appropriately declares player in check or checkmate.

 Possible improvements:
   - Chess Rules additions, ie: Castling, En passant capture, Pawn Promotion
   - Better AI
   - Network play
   
"""

from ChessBoard import ChessBoard
from ChessAI import HeuristicDefense, Def_Heuristic, HeuristicOffense, Off_Heuristic, EnemyDefense, Def_Enemy, EnemyOffense, Off_Enemy
from ChessPlayer import ChessPlayer
from ChessGUI_text import ChessGUI_text
from ChessGUI_pygame import ChessGUI_pygame
from ChessRules import ChessRules
from ChessGameParams import TkinterGameSetupParams

from optparse import OptionParser
import time
import copy

#Node for state tree, used to build the state tree
class Tree(object):
	def __init__(self, board):
		assert isinstance(board,ChessBoard)
		self.board = copy.deepcopy(board) #stores copy of the ChessBoard
		self.hVal = 0 #heuristic value
		self.children = [] #Stores "tree objects," which are the nodes
		
	def add_child(self, node):
		assert isinstance(node,Tree) #Checks if the node object is of class Tree
		self.children.append(node)
		
	def create_tree(self,color,rules,ply):
		if ply == 0:
			return ply
		board = self.board.GetState() #Gets the current state of chess board
		if color == 'white':
			player = 'w'
		if color == 'black':
			player = 'b'
		for r in range(8):
			for c in range(8):
				if board[r][c] != 'e':
					piece = board[r][c]
					if piece[:1] == player: #If the piece is the current play's piece, create the children of this node
						tup = (r,c) #Gets position of piece
						mylist = rules.GetListOfValidMoves(board,color,tup) #Gets list of valid move for that piece
						#This loops through the list of valid moves and makes the move on a temporary ChessBoard.
						#Uses the temporary ChessBoard to create a child, and then appends the child to the children list.
						#Each child contains the state of the board after a valid move has been made.
						for moves in mylist:
							tempChessBoard = copy.deepcopy(self.board)
							tempChessBoard.MovePiece((tup,moves))
							tempTreeObj = Tree(tempChessBoard)
							self.add_child(tempTreeObj)
							for child in self.children:
								if player == 'b':
									color = 'white'
								elif player == 'w':
									color = 'black'
							child.create_tree(color,rules,ply-1)                                                
class PythonChessMain:
	def __init__(self,options):
		if options.debug:
			self.Board = ChessBoard(2)
			self.debugMode = True
		else:
			self.Board = ChessBoard(0)#0 for normal board setup; see ChessBoard class for other options (for testing purposes)
			self.debugMode = False

		self.Rules = ChessRules()
		
	def SetUp(self,options):
		#gameSetupParams: Player 1 and 2 Name, Color, Human/AI level
		if self.debugMode:
			player1Name = 'Kasparov'
			player1Type = 'human'
			player1Color = 'white'
			player2Name = 'Light Blue'
			player2Type = 'randomAI'
			player2Color = 'black'          
		else:
			GameParams = TkinterGameSetupParams()
			(player1Name, player1Color, player1Type, player2Name, player2Color, player2Type) = GameParams.GetGameSetupParams()
		
		self.player = [0,0]
		if player1Type == 'human':
			self.player[0] = ChessPlayer(player1Name,player1Color)
		elif player1Type == 'randomAI':
			self.player[0] = ChessAI_random(player1Name,player1Color)
		elif player1Type == 'HeuristicOffense':
			self.player[0] = Off_Heuristic(player1Name,player1Color, self.Board)
		elif player1Type == 'EnemyOffense':
			self.player[0] = Off_Enemy(player1Name,player1Color, self.Board)
			
		if player2Type == 'human':
			self.player[1] = ChessPlayer(player2Name,player2Color)
		elif player2Type == 'randomAI':
			self.player[1] = ChessAI_random(player2Name,player2Color)
		elif player2Type == 'HeuristicDefense':
			self.player[1] = Def_Heuristic(player2Name,player2Color, self.Board)
		elif player2Type == 'EnemyDefense':
			self.player[1] = Def_Enemy(player2Name,player2Color, self.Board)
			
		if 'AI' in self.player[0].GetType() and 'AI' in self.player[1].GetType():
			self.AIvsAI = True
		else:
			self.AIvsAI = False
			
		if options.pauseSeconds > 0:
			self.AIpause = True
			self.AIpauseSeconds = int(options.pauseSeconds)
		else:
			self.AIpause = False
			
		#create the gui object - didn't do earlier because pygame conflicts with any gui manager (Tkinter, WxPython...)
		if options.text:
			self.guitype = 'text'
			self.Gui = ChessGUI_text()
		else:
			self.guitype = 'pygame'
			if options.old:
				self.Gui = ChessGUI_pygame(0)
			else:
				self.Gui = ChessGUI_pygame(1)
			
	def MainLoop(self):
		currentPlayerIndex = 0
		turnCount = 0
		open("log_X.txt", "w").close()
		open("log_Y.txt", "w").close()
		prevBoards = []  #To compare previous boards
		while not self.Rules.IsCheckmate(self.Board.GetState(),self.player[currentPlayerIndex].color):
			board = self.Board.GetState()
			currentColor = self.player[currentPlayerIndex].GetColor()
			#hardcoded so that player 1 is always white
			turnCount = turnCount + 1
			if turnCount == 101:
				self.Gui.PrintMessage("Maximum moves reached.")
				self.Gui.EndGame(board)
			if currentColor == 'black':  #Only the defense player wants a draw
				#print prevBoards.count(board)
				if prevBoards.count(board) == 2:
					self.Gui.PrintMessage("Black player calls threefold repetition draw.")
					self.Gui.EndGame(board)
				prevBoards.append(copy.deepcopy(board))
			self.Gui.PrintMessage("")
			baseMsg = "TURN %s - %s (%s)" % (str(turnCount),self.player[currentPlayerIndex].GetName(),currentColor)
			self.Gui.PrintMessage("-----%s-----" % baseMsg)
			self.Gui.Draw(board)
			if currentColor == "white":
				currentPlayer = "X"
			if currentColor == "black":
				currentPlayer = "Y"
			if self.Rules.IsInCheck(board,currentColor):
				self.Gui.PrintMessage("Warning..."+self.player[currentPlayerIndex].GetName()+" ("+self.player[currentPlayerIndex].GetColor()+") is in check!") 
			if self.player[currentPlayerIndex].GetType() == 'HeuristicDefense':
			#	then get new move to put into MoveTuple and make move			
				
				if turnCount > 2:
					textFileX = open("log_X.txt", "r")
					for line in textFileX:
						move = line	
					textFileY = open("log_Y.txt", "a")
					textFileY.write(move)
					textFileY.close()
					textFileX.close()
				moveTuple = self.player[currentPlayerIndex].GetMove(self.Board.GetState(), currentColor)
				self.WriteMove(board, moveTuple, currentPlayer, turnCount)
				currentPlayer = "Y"
				
			#	write to text file player_ytext below before changing currentPlayerIndex below
			elif self.player[currentPlayerIndex].GetType() == 'HeuristicOffense':
				currentPlayer = "X"
				
				if turnCount > 1:
					textFileY = open("log_Y.txt", "r")
					for line in textFileY:
						move = line
					textFileX = open("log_X.txt", "a")
					textFileX.write(move)
					textFileX.close()
					textFileY.close()
				moveTuple = self.player[currentPlayerIndex].GetMove(self.Board.GetState(), currentColor)
				self.WriteMove(board, moveTuple, currentPlayer, turnCount)
				
			# #	then get new move to put into Movetuple and make move
			# #	write to text file player_xtext below before changing currentPlayerIndex below
			elif self.player[currentPlayerIndex].GetType() == 'EnemyDefense':
				moveTuple = self.player[currentPlayerIndex].GetMove(self.Board.GetState(), currentColor)
			# 	#CALL READ FUNCTION HERE FOR ENEMY PLAYER == DEFENSE KRUTIK
			# 	#moveTuple = defense read function
			elif self.player[currentPlayerIndex].GetType() == 'EnemyOffense':
				moveTuple = self.player[currentPlayerIndex].GetMove(self.Board.GetState(), currentColor)
			# 	#CALL READ FUNCTION HERE FOR ENEMY PLAYER == OFFENSE KRUTIK
			# 	#moveTuple = offense read function
			else:
				moveTuple = self.Gui.GetPlayerInput(board,currentColor)
			moveReport = self.Board.MovePiece(moveTuple) #moveReport = string like "White Bishop moves from A1 to C3" (+) "and captures ___!"
			self.Gui.PrintMessage(moveReport)
			#	use current player index to determine what file to write to
			#	index = 0 is player x / "white" / offense
			#	index = 1 is player y / "black" / defense
			currentPlayerIndex = (currentPlayerIndex+1)%2 #this will cause the currentPlayerIndex to toggle between 1 and 0
			self.AIvsAI = True
			if self.AIvsAI and self.AIpause:
				time.sleep(self.AIpauseSeconds)
		self.Gui.PrintMessage("CHECKMATE!")
		winnerIndex = (currentPlayerIndex+1)%2
		self.Gui.PrintMessage(self.player[winnerIndex].GetName()+" ("+self.player[winnerIndex].GetColor()+") won the game!")
		self.Gui.EndGame(board)
		


	def WriteMove(self, board, tuple, currentPlayer, turnCount):
		#a-g columns
		#1-8 rows
		pieceRow = tuple[0][0]
		pieceCol = tuple[0][1]
		pieceToMove = board[pieceRow][pieceCol]
		
		if tuple[1][1] == 0:
			columnLetter = 'a'
		elif tuple[1][1] == 1:
			columnLetter = 'b'
		elif tuple[1][1] == 2:
			columnLetter = 'c'
		elif tuple[1][1] == 3:
			columnLetter = 'd'
		elif tuple[1][1] == 4:
			columnLetter = 'e'
		elif tuple[1][1] == 5:
			columnLetter = 'f'
		elif tuple[1][1] == 6:
			columnLetter = 'g'
		elif tuple[1][1] == 7:
			columnLetter = 'h'
			
		fileName = "log_" + currentPlayer + ".txt"
		file = open(fileName, "a")
		file.write(str(turnCount) + " " + currentPlayer + ":" + pieceToMove[1] + ":" + columnLetter + str(tuple[1][0] + 1) + "\n")
		file.close()
		
		if turnCount == 1:
			fileName = open("log_Y.txt", "w")
			fileName.write(str(turnCount) + " " + currentPlayer + ":" + pieceToMove[1] + ":" + columnLetter + str(tuple[1][0] + 1) + "\n")
			fileName.close()
			
			


parser = OptionParser()
parser.add_option("-d", dest="debug",
				  action="store_true", default=False, help="Enable debug mode (different starting board configuration)")
parser.add_option("-t", dest="text",
				  action="store_true", default=False, help="Use text-based GUI")
parser.add_option("-o", dest="old",
				  action="store_true", default=False, help="Use old graphics in pygame GUI")
parser.add_option("-p", dest="pauseSeconds", metavar="SECONDS",
				  action="store", default=0, help="Sets time to pause between moves in AI vs. AI games (default = 0)")


(options,args) = parser.parse_args()

game = PythonChessMain(options)
game.SetUp(options)
game.MainLoop()


	
