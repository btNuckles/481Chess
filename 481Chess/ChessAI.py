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
														tempChessBoard.MovePiece((tup, moves))
														#print(tup, moves)
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
		
		temp = 64
		for child in tree.children:
			#print(child.hVal)
			#print(child.moveTuple)
			if child.hVal < temp:
				temp = child.hVal
				moveTuple = child.moveTuple
					
		#for minNode in tree.children:
		#	minNode.hVal = self.DefenseHeuristicValue(minNode.board.GetState())
		#	print minNode.hVal
			# for maxNode in minNode.children:
			# 	maxNode.hVal = self.DefenseHeuristicValue(maxNode.board.GetState())
			# 	print maxNode.hVal
		
		
		# moveTuple = (myFromTuple,myToTuple)
		print(moveTuple)
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
						
	#Our 481 heuristic computes distances between our pieces and the enemy king
	def OffenseHeuristicValue(self, board):
		whiteKnight = self.PiecePositions(board, "white", "knight")
		whiteKing = self.PiecePositions(board, "white", "king")
		whiteRook = self.PiecePositions(board, "white", "rook")
		blackKing = self.PiecePositions(board, "black", "king")
		blackKnight = self.PiecePositions(board, "black", "knight")
		
		knightDistance = abs(whiteKnight[0] - blackKing[0]) + abs(whiteKnight[1] - blackKing[1]) - 4
		kingDistance = abs(whiteKing[0] - blackKing[0]) + abs(whiteKing[1] - blackKing[1]) - 2
		rookDistance = 1
		rookActual = abs(whiteRook[0] - blackKing[0]) + abs(whiteRook[1] - blackKing[1])
		
		bkKnightDistance = abs(whiteKnight[0] - blackKnight[0]) + abs(whiteKnight[1] - blackKnight[1])
		bkKingDistance = abs(whiteKing[0] - blackKnight[0]) + abs(whiteKing[1] - blackKnight[1])
		bkRookDistance = abs(whiteRook[0] - blackKnight[0]) + abs(whiteRook[1] - blackKnight[1])
		
		toKingDistance = knightDistance + kingDistance + rookDistance
		
		# a few handlers to deal with heuristic values dealing with taking/prevntion of taking pieces
		# bkKnight protects from black knight
		# kingDistance finds check states
		
		if knightDistance > 1.5*kingDistance:
			toKingDistance = -30
		
		if bkKnightDistance == 3:
			toKingDistance = 50
			
		if bkKingDistance == 3:
			toKingDistance = 50
			
		if bkRookDistance == 3:
			toKingDistance = 50
			
		if knightDistance == -3:
			toKingDistance = -20
			
		if kingDistance == -2:
			toKingDistance = -20
			
		if rookActual == 0:
			toKingDistance = -20
				
		return toKingDistance
		
	def MiniMax(self, tree, depth, playerIndex):
		if depth == 0 or not tree.children:
			return self.OffenseHeuristicValue(tree.board.GetState())
			
		if playerIndex:	#CURRENT PLY == OFFENSE
			bestValue = 64
			for child in tree.children:
				temp = self.MiniMax(tree, depth - 1, True)
				bestValue = min(bestValue, temp)
				tree.hVal = bestValue
			return bestValue
				
		else:		#CURRENT PLY == DEFENSE
			bestValue = -64
			for child in tree.children:
				temp = self.MiniMax(tree, depth - 1, False)
				bestValue = max(bestValue, temp)
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
		
		temp = -64
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
		print(moveTuple)
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
		
		knightDistance = abs(blackKing[0] - whiteKnight[0]) + abs(blackKing[1] - whiteKnight[1]) - 3
		kingDistance = abs(blackKing[0] - whiteKing[0]) + abs(blackKing[1] - whiteKing[1]) - 2
		rookActual = abs(whiteRook[0] - blackKing[0]) + abs(whiteRook[1] - blackKing[1])
		rookDistance = 1
		
		bkKnightDistance = abs(whiteKnight[0] - blackKnight[0]) + abs(whiteKnight[1] - blackKnight[1])
		bkKingDistance = abs(whiteKing[0] - blackKnight[0]) + abs(whiteKing[1] - blackKnight[1])
		bkRookDistance = abs(whiteRook[0] - blackKnight[0]) + abs(whiteRook[1] - blackKnight[1])
		
		fromKingDistance = knightDistance + kingDistance + rookDistance
		
		if bkKnightDistance == 0:
			fromKingDistance = 50
			
		if bkKingDistance == 0:
			fromKingDistance = 50
			
		if bkRookDistance == 0:
			fromKingDistance = 50
		
		if knightDistance == -3:
			fromKingDistance = -20
			
		if kingDistance == -2:
			fromKingDistance = -20
			
		if rookActual == 0:
			fromKingDistance = -20
		
		return fromKingDistance
		
	def MiniMax(self, tree, depth, playerIndex):
		if depth == 0 or not tree.children:
			return self.DefenseHeuristicValue(tree.board.GetState())
			
		if playerIndex:	#CURRENT PLY == DEFENSE
			bestValue = -64
			for child in tree.children:
				temp = self.MiniMax(tree, depth - 1, False)
				bestValue = max(bestValue, temp)
				tree.hVal = bestValue
			return bestValue
				
		else:		#CURRENT PLY == OFFENSE
			bestValue = 64
			for child in tree.children:
				temp = self.MiniMax(tree, depth - 1, True)
				bestValue = min(bestValue, temp)
				tree.hVal = bestValue
			return bestValue
				
			
		
#class Def_Enemy(EnemyDefense):
	#HERE WE READ THE INPUT OF PLAYER Y TEXT FILE
	#WE USE THIS CLASS WHEN THE OPPONENT GROUP IS ON DEFENSE AND WE ARE ON OFFENSE
	#READ FROM THE TEXT FILE THEN CONVERT TO THE FORMAT OF MOVETUPLE
	#USE THIS MOVE TUPLE TO USE THE MAKEMOVE FUNCTION IN MAIN FOR CURRENT PLAYER TYPE
	#THIS IS FOR THE SAKE OF UPDATING OUR OWN BOARD SO WE CAN MAKE OUR NEXT MOVE
		
#class Off_Enemy(EnemyOffense):

	
	#HERE WE READ THE INPUT OF PLAYER X TEXT FILE
	#WE USE THIS CLASS WHEN THE OPPONENT GROUP IS ON OFFENSE AND WE ARE ON DEFENSE
	#READ FROM THE TEXT FILE THEN CONVERT TO THE FORMAT OF MOVETUPLE
	#USE THIS MOVE TUPLE TO USE THE MAKEMOVE FUNCTION IN MAIN FOR CURRENT PLAYER TYPE
	#THIS IS FOR THE SAKE OF UPDATING OUR OWN BOARD SO WE CAN MAKE OUR NEXT MOVE


