#! /usr/bin/env python
"""
 Project: Python Chess
 File name: ChessAI.py
 Description:  Contains the AI classes.
	
 Copyright (C) 2009 Steve Osborne, srosborne (at) gmail.com
 http://yakinikuman.wordpress.com/
 """

from ChessBoard import ChessBoard
from ChessRules import ChessRules
import random
import copy

class Tree(object):
	def __init__(self, board):
		assert isinstance(board,ChessBoard)
		self.board = copy.deepcopy(board) #stores copy of the ChessBoard
		self.hVal = 0 #heuristic value
		self.children = [] #Stores "tree objects," which are the nodes
		self.moveTuple = ((0,0), (0,0)) #Stores the move this node makes
		
	def add_child(self, node):
		assert isinstance(node,Tree) #Checks if the node object is of class Tree
		self.children.append(node)
		
	def create_tree(self,color,rules,ply):
		if ply == 0:
			return ply
		board = self.board.GetState() #Gets the current state of chess board
		if color == 'white':
			player = 'w'
			thisPlayer = 'white'
		if color == 'black':
			player = 'b'
			thisPlayer = 'black'
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
							tempChessBoard.MovePiece((tup, moves))
							#print(tup, moves)
							#if ply == 3 and player == 'b':
							#	print (tup, rules.IsInCheck(tempChessBoard.GetState(), color), color)
							if not rules.IsInCheck(tempChessBoard.GetState(), thisPlayer):
								tempTreeObj = Tree(tempChessBoard)
								tempTreeObj.moveTuple = ((tup, moves))
								self.add_child(tempTreeObj)
								for child in self.children:
									if player == 'b':
										color = 'white'
									elif player == 'w':
										color = 'black'
								child.create_tree(color,rules,ply-1)                                                        

#PROTOTYPE AI CLASS
#class ChessAI:
#	def __init__(self,name,color):
#		#print "In ChessAI __init__"
#		self.name = name
#		self.color = color
#		self.type = 'AI'
#		self.Rules = ChessRules()
#		
#	def GetName(self):
#		return self.name
#		
#	def GetColor(self):
#		return self.color
#		
#	def GetType(self):
#		return self.type

# Creates basic classes for heuristic offense and defense for both teams, indicated by self.type
	
class HeuristicDefense:
	def __init__(self,name,color):
		self.name = name
		self.color = color
		self.type = 'HeuristicDefense'
		self.Rules = ChessRules()
		
	def GetName(self):
		return self.name
		
	def GetColor(self):
		return self.color
		
	def GetType(self):
		return self.type
		
class HeuristicOffense:
	def __init__(self,name,color):
		self.name = name
		self.color = color
		self.type = 'HeuristicOffense'
		self.Rules = ChessRules()
		
	def GetName(self):
		return self.name
		
	def GetColor(self):
		return self.color
		
	def GetType(self):
		return self.type
		
class EnemyDefense:
	def __init__(self,name,color):
		self.name = name
		self.color = color
		self.type = 'EnemyDefense'
		self.Rules = ChessRules()
		
	def GetName(self):
		return self.name
		
	def GetColor(self):
		return self.color
		
	def GetType(self):
		return self.type
		
class EnemyOffense:
	def __init__(self,name,color):
		self.name = name
		self.color = color
		self.type = 'EnemyOffense'
		self.rules = ChessRules()
		
	def GetName(self):
		return self.name
		
	def GetColor(self):
		return self.color
		
	def GetType(self):
		return self.type
		
		
class Off_Heuristic(HeuristicOffense):
	#heuristically pick the best legal move
	def __init__(self, name, color, Board):
		self.Board = Board
		HeuristicOffense.__init__(self, name, color)
	
	def GetMove(self,board,color):
		#print "In ChessAI_random.GetMove"
	
		#THIS IS WHERE WE CREATE THE BOARD STATE MINI-MAX TREE
		#WE THEN APPLY OUR HEURISTIC FUNCTION TO EVERY CHILD NODE AT THE BOTTOM OF THE TREE
		#THEN RETURN THE HEURISTIC VALUES TO THE TOP RECURSIVELY
		#THE MOVE THAT IS THE BEST CHOICE SHOULD BE SELECTED
		#THAT MOVE TUPLE IS CREATED AND RETURN TO MAIN
			
		tree = Tree(self.Board)

		tree.create_tree(color, self.Rules, 3)
		playerIndex = 1
		
		self.MiniMax(tree, 3, playerIndex)
		
		temp = -1000000000
		for child in tree.children:
			#print(child.hVal)
			#print(child.moveTuple)
			if child.hVal > temp:
				temp = child.hVal
				moveTuple = child.moveTuple
					
		#for minNode in tree.children:
		#	minNode.hVal = self.DefenseHeuristicValue(minNode.board.GetState())
		#	print minNode.hVal
			# for maxNode in minNode.children:
			# 	maxNode.hVal = self.DefenseHeuristicValue(maxNode.board.GetState())
			# 	print maxNode.hVal
		
		
		# moveTuple = (myFromTuple,myToTuple)
		#print(moveTuple)
		return moveTuple
		
	def GetMyPiecesWithLegalMoves(self,board,color):
		#print "In ChessAI_random.GetMyPiecesWithLegalMoves"
		if color == "black":
			myColor = 'b'
			enemyColor = 'w'
		else:
			myColor = 'w'
			enemyColor = 'b'
			
		#get list of my pieces
		myPieces = []
		for row in range(8):
			for col in range(8):
				piece = board[row][col]
				if myColor in piece:
					if len(self.Rules.GetListOfValidMoves(board,color,(row,col))) > 0:
						myPieces.append((row,col))	
		return myPieces
		
	def PiecePositions(self,board,color,pieceType):
		#returns list of piece positions; will be empty if color piece doesn't exist on board
		if color == "black":
			myColor = 'b'
		else:
			myColor = 'w'
			
		if pieceType == "king":
			myPieceType = 'K'
		elif pieceType == "queen":
			myPieceType = 'Q'
		elif pieceType == "rook":
			myPieceType = 'R'
		elif pieceType == "knight":
			myPieceType = 'T'
		elif pieceType == "bishop":
			myPieceType = 'B'
		elif pieceType == "pawn":
			myPieceType = 'P'

		piecePositions = []
		for row in range(8):
			for col in range(8):
				piece = board[row][col]
				if myColor in piece and myPieceType in piece:
					# piecePositions.append((row,col))
					return (row, col)	
		return (-1, -1) # When piece is not on a board return this tuple
		
	def OffenseHeuristicValue(self, board):
		whiteKnight = self.PiecePositions(board, "white", "knight")
		whiteKing = self.PiecePositions(board, "white", "king")
		whiteRook = self.PiecePositions(board, "white", "rook")
		blackKing = self.PiecePositions(board, "black", "king")
		blackKnight = self.PiecePositions(board, "black", "knight")
		
		retval = 0
		
		# Board value loses points for missing white rook or knight
		if whiteKnight[0] == -1:
			retval -= 10000
			
		if whiteRook[0] == -1:
			retval -= 10000000		

		if whiteKing[0] == -1:
			retval -= 100000000
		
		# Gain points for taking enemy knight, but not worth risking losing a piece
		if blackKnight[0] == -1:
			retval += 1000
			

		# White king needs to be close to black king for checkmate, lower distance increases value
		retval += 100 * (14 - (abs(whiteKing[0] - blackKing[0]) + abs(whiteKing[1] - blackKing[1])))

		# Good to have knight close to black king to help put in check, but not right next to it
		if whiteKnight[0] != -1:
			retval += 50 * (14 - (abs(whiteKnight[0] - blackKing[0]) + abs(whiteKnight[1] - blackKing[1])))
			if 2 >= (abs(whiteKnight[0] - blackKing[0]) + abs(whiteKnight[1] - blackKing[1])):
				retval -= 100
		
		# We want black king to be at edge
		if blackKing[0] == 0 or blackKing[0] == 7\
			or blackKing[1] == 0 or blackKing[1] == 7:
			retval += 1000
			

		# But don't want white king at edge, could allow black king to move to center
		if whiteKing[0] == 0 or whiteKing[0] == 7\
		   or whiteKing[1] == 0 or whiteKing[1] == 7:
			retval -= 900
			
		
		# Rook can make barrier to block black king from center. Good if 1 row/col away on same side as white king
		if (whiteKing[0] > blackKing[0] and whiteRook[0] == (blackKing[0] + 1))\
		   or (whiteKing[1] > blackKing[1] and whiteRook[1] == (blackKing[1] + 1))\
		   or (whiteKing[0] < blackKing[0] and whiteRook[0] == (blackKing[0] - 1))\
		   or (whiteKing[1] < blackKing[1] and whiteRook[1] == (blackKing[1] - 1)):
			retval += 10000
			

		# Checkmate conditions: black king at edge, kings 2 or 3 apart, rook on same edge as black king
		if (blackKing[0] == 0 or blackKing[0] == 7 or blackKing[1] == 0 or blackKing[1] == 7) \
		   and ((abs(whiteKing[0] - blackKing[0]) + abs(whiteKing[1] - blackKing[1])) == 2) \
		   and ( (blackKing[0] == 0 and whiteRook[0] == 0) or (blackKing[0] == 7 and whiteRook[0] == 7)\
			 or (blackKing[1] == 0 and whiteRook[1] == 0) or (blackKing[1] == 7 and whiteRook[1] == 7)):
			retval += 1000000
			
		#print retval
		return retval

		"""
		knightDistance = abs(whiteKnight[0] - blackKing[0]) + abs(whiteKnight[1] - blackKing[1]) - 4
		kingDistance = abs(whiteKing[0] - blackKing[0]) + abs(whiteKing[1] - blackKing[1]) - 2
		rookDistance = 1
		rookActual = abs(whiteRook[0] - blackKing[0]) + abs(whiteRook[1] - blackKing[1])
		
		bkKnightDistance = abs(whiteKnight[0] - blackKnight[0]) + abs(whiteKnight[1] - blackKnight[1])
		bkKingDistance = abs(whiteKing[0] - blackKnight[0]) + abs(whiteKing[1] - blackKnight[1])
		bkRookDistance = abs(whiteRook[0] - blackKnight[0]) + abs(whiteRook[1] - blackKnight[1])
		
		toKingDistance = knightDistance + kingDistance + rookDistance
		"""
		
	def MiniMax(self, tree, depth, playerIndex):
		if depth == 0 or not tree.children:
			return self.OffenseHeuristicValue(tree.board.GetState())
			
		if playerIndex:	#CURRENT PLY == OFFENSE
			bestValue = -100000000
			for child in tree.children:
				temp = self.MiniMax(child, depth - 1, True)
				bestValue = max(bestValue, temp)
				#print(bestValue)
				tree.hVal = bestValue
			return bestValue
				
		else:		#CURRENT PLY == DEFENSE
			bestValue = 100000000
			for child in tree.children:
				temp = self.MiniMax(child, depth - 1, False)
				bestValue = min(bestValue, temp)
				tree.hVal = bestValue
			return bestValue
		
class Def_Heuristic(HeuristicDefense):
	#heuristically pick the best legal move
	def __init__(self, name, color, Board):
		self.Board = Board
		HeuristicDefense.__init__(self, name, color)

	def GetMove(self,board,color):
		#print "In ChessAI_random.GetMove"
	
		myPieces = self.GetMyPiecesWithLegalMoves(board,color)
		# opponentPieces = self.GetOpponentPieces(board, color)
		opponentPieces = self.GetEnemyPiecesWithLegalMoves(board, color)
		
		#THIS IS WHERE WE CREATE THE BOARD STATE MINI-MAX TREE
		#WE THEN APPLY OUR HEURISTIC FUNCTION TO EVERY CHILD NODE AT THE BOTTOM OF THE TREE
		#THEN RETURN THE HEURISTIC VALUES TO THE TOP RECURSIVELY
		#THE MOVE THAT IS THE BEST CHOICE SHOULD BE SELECTED
		#THAT MOVE TUPLE IS CREATED AND RETURN TO MAIN
		tree = Tree(self.Board)

		tree.create_tree(color, self.Rules, 3)
		playerIndex = 1
		
		self.MiniMax(tree, 3, playerIndex)
		
		temp = -1000000000
		for child in tree.children:
			#print(child.hVal)
			#print(child.moveTuple)
			if child.hVal > temp:
				temp = child.hVal
				moveTuple = child.moveTuple
					
		#for minNode in tree.children:
		#	minNode.hVal = self.DefenseHeuristicValue(minNode.board.GetState())
		#	print minNode.hVal
		# for maxNode in minNode.children:
		# 	maxNode.hVal = self.DefenseHeuristicValue(maxNode.board.GetState())
		# 	print maxNode.hVal
		
		
		# moveTuple = (myFromTuple,myToTuple)
		#print(moveTuple)
		return moveTuple
		
	def GetMyPiecesWithLegalMoves(self,board,color):
		#print "In ChessAI_random.GetMyPiecesWithLegalMoves"
		if color == "black":
			myColor = 'b'
			enemyColor = 'w'
		else:
			myColor = 'w'
			enemyColor = 'b'
			
		#get list of my pieces
		myPieces = []
		for row in range(8):
			for col in range(8):
				piece = board[row][col]
				if myColor in piece:
					if len(self.Rules.GetListOfValidMoves(board,color,(row,col))) > 0:
						myPieces.append((row,col))	
		return myPieces

	def GetEnemyPiecesWithLegalMoves(self,board,color):
		#print "In GetEnemyPiecesWithLegalMoves"

		if color == "black":
			myColor = 'b'
			enemyColor = 'w'
			enemyColor_full = 'white'
		else:
			myColor = 'w'
			enemyColor = 'b'
			enemyColor_full = 'black'

		#get list of opponent pieces that have legal moves
		enemyPieces = []

		for row in range(8):
			for col in range(8):
				piece = board[row][col]
				if enemyColor in piece:
					if len(self.Rules.GetListOfValidMoves(board,enemyColor_full,(row,col))) > 0:
						enemyPieces.append((row,col))
		return enemyPieces
		
	def PiecePositions(self,board,color,pieceType):
		#returns list of piece positions; will be empty if color piece doesn't exist on board
		if color == "black":
			myColor = 'b'
		else:
			myColor = 'w'
			
		if pieceType == "king":
			myPieceType = 'K'
		elif pieceType == "queen":
			myPieceType = 'Q'
		elif pieceType == "rook":
			myPieceType = 'R'
		elif pieceType == "knight":
			myPieceType = 'T'
		elif pieceType == "bishop":
			myPieceType = 'B'
		elif pieceType == "pawn":
			myPieceType = 'P'

		piecePositions = []
		for row in range(8):
			for col in range(8):
				piece = board[row][col]
				if myColor in piece and myPieceType in piece:
					# piecePositions.append((row,col))
					return (row, col)	
		return (-1, -1) # When piece is not on a board return this tuple
		
	def DefenseHeuristicValue(self, board):
		blackKnight = self.PiecePositions(board, "black", "knight")
		blackKing = self.PiecePositions(board, "black", "king")
		whiteKnight = self.PiecePositions(board, "white", "knight")
		whiteKing = self.PiecePositions(board, "white", "king")
		whiteRook = self.PiecePositions(board, "white", "rook")
		
		retval = 0
		
		#Good if white pieces are gone, best to take rook
		if whiteRook[0] == -1:
			retval += 12000
		if whiteKnight[0] == -1:
			retval += 8000
		
		# Bad if black knight is lost, but worth sacrificing to take rook
		if blackKnight[0] == -1:
			retval -= 10000
		
		# Black king should not be near edge
		if blackKing[0] == 0 or blackKing[0] == 7 or blackKing[1] == 0 or blackKing[1] == 7:
			retval -= 200

		# Higher value for king positions near center
		retval += 100 * ((3.5 - abs(3.5 - blackKing[0])) + (3.5 - abs(3.5 - blackKing[1])))
		
		# Knight should try to take out rook, but can't attack from right next to it
		if whiteRook[0] != -1:
			retval += 10 * (10 - (abs(whiteRook[0] - blackKnight[0]) + abs(whiteRook[1] - blackKnight[1])))
			if 2 >= (abs(whiteRook[0] - blackKnight[0]) + abs(whiteRook[1] - blackKnight[1])):
				retval -= 20
		# Knight should avoid being on same row or column as rook
		if blackKnight != -1 and whiteRook != -1:
			if blackKnight[0] == whiteRook[0] or blackKnight[1] == whiteRook[1]:
				retval -= 100
		
		return retval
		
	def MiniMax(self, tree, depth, playerIndex):
		if depth == 0 or not tree.children:
			return self.DefenseHeuristicValue(tree.board.GetState())
			
		if playerIndex:	#CURRENT PLY == DEFENSE
			bestValue = -100000000
			for child in tree.children:
				temp = self.MiniMax(child, depth - 1, False)
				bestValue = max(bestValue, temp)
				tree.hVal = bestValue
			return bestValue
				
		else:		#CURRENT PLY == OFFENSE
			bestValue = 100000000
			for child in tree.children:
				temp = self.MiniMax(child, depth - 1, True)
				bestValue = min(bestValue, temp)
				tree.hVal = bestValue
			return bestValue
				
			
		
class Def_Enemy(EnemyDefense):
	#HERE WE READ THE INPUT OF PLAYER Y TEXT FILE
	#WE USE THIS CLASS WHEN THE OPPONENT GROUP IS ON DEFENSE AND WE ARE ON OFFENSE
	#READ FROM THE TEXT FILE THEN CONVERT TO THE FORMAT OF MOVETUPLE
	#USE THIS MOVE TUPLE TO USE THE MAKEMOVE FUNCTION IN MAIN FOR CURRENT PLAYER TYPE
	#THIS IS FOR THE SAKE OF UPDATING OUR OWN BOARD SO WE CAN MAKE OUR NEXT MOVE
	def __init__(self, name, color, Board):
		self.Board = Board
		EnemyDefense.__init__(self, name, color)
		
	def GetMove(self, board, color):
		#myPieces = self.GetMyPiecesWithLegalMoves(board,color)
		
		defenseMoveNotMade = True
		while defenseMoveNotMade:
			line = ""
			textFile = open("log_Y.txt")
			for line in textFile:
				pass
			
			if line == "":
				textFile.close()
			else:
				line = line.split(" ")
				if line[1][0] == "Y":
					defenseMoveNotMade = False
					token = line[1].split(':')
					pieceType = token[1]
					locationToMove = token[2]
					#break
				textFile.close()
			print("Waiting for defenses move")
			
		#print(pieceType)
		#print(locationToMove)
			
			
			

		mypiecePosition = self.PiecePositions(board, color, pieceType[0])
		#print(mypiecePosition)
		if locationToMove[0] == 'a':
			columnNum = 0
		elif locationToMove[0] == 'b':
			columnNum = 1
		elif locationToMove[0] == 'c':
			columnNum = 2
		elif locationToMove[0] == 'd':
			columnNum = 3
		elif locationToMove[0] == 'e':
			columnNum = 4
		elif locationToMove[0] == 'f':
			columnNum = 5
		elif locationToMove[0] == 'g':
			columnNum = 6
		elif locationToMove[0] == 'h':
			columnNum = 7
	
		#Remove this block if text file writing is backwards against enemy team
		#Add rowNum = locationToMove[1]
	
		if locationToMove[1] == 1:
			rowNum = 7
		elif locationToMove[1] == 2:
			rowNum = 6
		elif locationToMove[1] == 3:
			rowNum = 5
		elif locationToMove[1] == 4:
			rowNum = 4	
		elif locationToMove[1] == 5:
			rowNum = 3
		elif locationToMove[1] == 6:
			rowNum = 2
		elif locationToMove[1] == 7:
			rowNum = 1
		elif locationToMove[1] == 8:
			rowNum = 0
					
		
		r, c = 2, 2 
		moveTuple = [[0 for x in range(r)] for y in range(c)] 
		
		moveTuple[0][0] = mypiecePosition[0]
		moveTuple[0][1] = mypiecePosition[1]
		moveTuple[1][0] = int(rowNum)
		moveTuple[1][1] = columnNum
		#moveTuple = ((rowNum,columnNum),((mypiecePosition[0]),(mypiecePosition[1])))
		print moveTuple
		return moveTuple
		
	def PiecePositions(self,board,color,pieceType):
		#returns list of piece positions; will be empty if color piece doesn't exist on board
		if color == "black":
			myColor = 'b'
		else:
			myColor = 'w'
			
		if pieceType == "K":
			myPieceType = 'K'
		elif pieceType == "R":
			myPieceType = 'R'
		elif pieceType == "T":
			myPieceType = 'T'


		piecePositions = []
		for row in range(8):
			for col in range(8):
				piece = board[row][col]
				if myColor in piece and myPieceType in piece:
					# piecePositions.append((row,col))
					return (row, col)	
		return (-1, -1) # When piece is not on a board return this tuple
		
	def GetMyPiecesWithLegalMoves(self,board,color):
		#print "In ChessAI_random.GetMyPiecesWithLegalMoves"
		if color == "black":
			myColor = 'b'
			enemyColor = 'w'
		else:
			myColor = 'w'
			enemyColor = 'b'
			
		#get list of my pieces
		myPieces = []
		for row in range(8):
			for col in range(8):
				piece = board[row][col]
				if myColor in piece:
					if len(self.Rules.GetListOfValidMoves(board,color,(row,col))) > 0:
						myPieces.append((row,col))	
		return myPieces

		
class Off_Enemy(EnemyOffense):
	def __init__(self, name, color, Board):
		self.Board = Board
		EnemyOffense.__init__(self, name, color)
	
	#HERE WE READ THE INPUT OF PLAYER X TEXT FILE
	#WE USE THIS CLASS WHEN THE OPPONENT GROUP IS ON OFFENSE AND WE ARE ON DEFENSE
	#READ FROM THE TEXT FILE THEN CONVERT TO THE FORMAT OF MOVETUPLE
	#USE THIS MOVE TUPLE TO USE THE MAKEMOVE FUNCTION IN MAIN FOR CURRENT PLAYER TYPE
	#THIS IS FOR THE SAKE OF UPDATING OUR OWN BOARD SO WE CAN MAKE OUR NEXT MOVE
	
	def GetMove(self, board, color):	
		
		offenseMoveNotMade = True
		while offenseMoveNotMade:
			line = ""
			textFile = open("log_X.txt")
			for line in textFile:
				pass
			if line == "":
				textFile.close()
			else:
				line = line.split(" ")
				if line[1][0] == "X":
					offenseMoveNotMade = False
					token = line[1].split(':')
					pieceType = token[1]
					locationToMove = token[2]
					#break
				textFile.close()
			print("Waiting for offenses move")
			
		#print(pieceType)
		#print(locationToMove)
			
			
			

		mypiecePosition = self.PiecePositions(board, color, pieceType[0])
		#print(mypiecePosition)
		if locationToMove[0] == 'a':
			columnNum = 0
		elif locationToMove[0] == 'b':
			columnNum = 1
		elif locationToMove[0] == 'c':
			columnNum = 2
		elif locationToMove[0] == 'd':
			columnNum = 3
		elif locationToMove[0] == 'e':
			columnNum = 4
		elif locationToMove[0] == 'f':
			columnNum = 5
		elif locationToMove[0] == 'g':
			columnNum = 6
		elif locationToMove[0] == 'h':
			columnNum = 7
			
		#Remove this block if enemy team text file writing is reversed
		#Add rowNum = locationToMove[1]
			
		if locationToMove[1] == 1:
			rowNum = 7
		elif locationToMove[1] == 2:
			rowNum = 6
		elif locationToMove[1] == 3:
			rowNum = 5
		elif locationToMove[1] == 4:
			rowNum = 4	
		elif locationToMove[1] == 5:
			rowNum = 3
		elif locationToMove[1] == 6:
			rowNum = 2
		elif locationToMove[1] == 7:
			rowNum = 1
		elif locationToMove[1] == 8:
			rowNum = 0
		
		
		r, c = 2, 2 
		moveTuple = [[0 for x in range(r)] for y in range(c)] 
		
		moveTuple[0][0] = mypiecePosition[0]
		moveTuple[0][1] = mypiecePosition[1]
		moveTuple[1][0] = int(rowNum)
		moveTuple[1][1] = columnNum
		#moveTuple = ((rowNum,columnNum),((mypiecePosition[0]),(mypiecePosition[1])))
		#print moveTuple
		return moveTuple
	
	def PiecePositions(self,board,color,pieceType):
		#returns list of piece positions; will be empty if color piece doesn't exist on board
		if color == "black":
			myColor = 'b'
		else:
			myColor = 'w'
			
		if pieceType == "K":
			myPieceType = 'K'
		elif pieceType == "R":
			myPieceType = 'R'
		elif pieceType == "T":
			myPieceType = 'T'


		piecePositions = []
		for row in range(8):
			for col in range(8):
				piece = board[row][col]
				if myColor in piece and myPieceType in piece:
					# piecePositions.append((row,col))
					return (row, col)	
		return (-1, -1) # When piece is not on a board return this tuple
		
	def GetMyPiecesWithLegalMoves(self,board,color):
		#print "In ChessAI_random.GetMyPiecesWithLegalMoves"
		if color == "black":
			myColor = 'b'
			enemyColor = 'w'
		else:
			myColor = 'w'
			enemyColor = 'b'
			
		#get list of my pieces
		myPieces = []
		for row in range(8):
			for col in range(8):
				piece = board[row][col]
				if myColor in piece:
					if len(self.Rules.GetListOfValidMoves(board,color,(row,col))) > 0:
						myPieces.append((row,col))	
		return myPieces
	



