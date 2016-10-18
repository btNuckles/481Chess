#! /usr/bin/env python
"""
 Project: Python Chess
 File name: ChessAI.py
 Description:  Contains the AI classes.
	
 Copyright (C) 2009 Steve Osborne, srosborne (at) gmail.com
 http://yakinikuman.wordpress.com/
 """
 
from ChessRules import ChessRules
import random

class Tree(object):
        def __init__(self, board):
                self.board = copy.deepcopy(board) #stores copy of the ChessBoard
                self.hVal = 0 #heuristic value
                self.children = [] #Stores "tree objects," which are the nodes
                
        def add_child(self, node):
                assert isinstance(node,Tree) #Checks if the node object is of class Tree
                self.children.append(node)
                
        def create_tree(self,color,rules):
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
	
	def GetMove(self,board,color):
		#print "In ChessAI_random.GetMove"
	
		#THIS IS WHERE WE CREATE THE BOARD STATE MINI-MAX TREE
		#WE THEN APPLY OUR HEURISTIC FUNCTION TO EVERY CHILD NODE AT THE BOTTOM OF THE TREE
		#THEN RETURN THE HEURISTIC VALUES TO THE TOP RECURSIVELY
		#THE MOVE THAT IS THE BEST CHOICE SHOULD BE SELECTED
		#THAT MOVE TUPLE IS CREATED AND RETURN TO MAIN
			
		
		moveTuple = (myFromTuple,myToTuple)
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
					piecePositions.append((row,col))	
		return piecePositions
		
						
	#Our 481 heuristic computes distances between our pieces and the enemy king
	def OffenseHeuristicValue(board):
		whiteKnight = PiecePositions(self, board, white, knight)
		whiteKing = PiecePositions(self, board, white, king)
		whiteRook = PiecePositions(self, board, white, rook)
		blackKing = PiecePositions(self, board, black, king)
		blackKnight = PiecePositions(self, board, black, knight)
		
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
		
class Def_Heuristic(HeuristicDefense):
	#heuristically pick the best legal move
	
	def GetMove(self,board,color):
		#print "In ChessAI_random.GetMove"
	
		myPieces = self.GetMyPiecesWithLegalMoves(board,color)
		opponentPieces = self.GetOpponentPieces(board, color)
		
		#THIS IS WHERE WE CREATE THE BOARD STATE MINI-MAX TREE
		#WE THEN APPLY OUR HEURISTIC FUNCTION TO EVERY CHILD NODE AT THE BOTTOM OF THE TREE
		#THEN RETURN THE HEURISTIC VALUES TO THE TOP RECURSIVELY
		#THE MOVE THAT IS THE BEST CHOICE SHOULD BE SELECTED
		#THAT MOVE TUPLE IS CREATED AND RETURN TO MAIN
		
		moveTuple = (myFromTuple,myToTuple)
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
					piecePositions.append((row,col))	
		return piecePositions
		
	def DefenseHeuristicValue(board):
		blackKnight = PiecePositions(self, board, black, knight)
		blackKing = PiecePositions(self, board, black, king)
		whiteKnight = PiecePositions(self, board, white, knight)
		whiteKing = PiecePositions(self, board, white, king)
		whiteRook = PiecePositions(self, board, white, rook)
		
		knightDistance = abs(blackKing[0] - whiteKnight[0]) + abs(blackKing[1] - whiteKnight[1]) - 3
		kingDistance = abs(blackKing[0] - whiteKing[0]) + abs(blackKing[1] - whiteKing[1]) - 2
		rookActual = abs(whiteRook[0] - blackKing[0]) + abs(whiteRook[1] - blackKing[1])
		rookDistance = 1
		
		bkKnightDistance = abs(whiteKnight[0] - blackKnight[0]) + abs(whiteKnight[1] - blackKnight[1])
		bkKingDistance = abs(whiteKing[0] - blackKnight[0]) + abs(whiteKing[1] - blackKnight[1])
		bkRookDistance = abs(whiteRook[0] - blackKnight[0]) + abs(whiteRook[1] - blackKnight[1])
		
		fromKingDistance = knightDistance + kingDistance + rookDistance
		
		if bkKnightDistance == 0:
			toKingDistance = 50
			
		if bkKingDistance == 0:
			toKingDistance = 50
			
		if bkRookDistance == 0:
			toKingDistance = 50
		
		if knightDistance == -3:
			fromKingDistance = -20
			
		if kingDistance == -2:
			fromKingDistance = -20
			
		if rookActual == 0:
			fromKingDistance = -20
		
		return fromKingDistance
		
class Def_Enemy(EnemyDefense):
	#HERE WE READ THE INPUT OF PLAYER Y TEXT FILE
	#WE USE THIS CLASS WHEN THE OPPONENT GROUP IS ON DEFENSE AND WE ARE ON OFFENSE
	#READ FROM THE TEXT FILE THEN CONVERT TO THE FORMAT OF MOVETUPLE
	#USE THIS MOVE TUPLE TO USE THE MAKEMOVE FUNCTION IN MAIN FOR CURRENT PLAYER TYPE
	#THIS IS FOR THE SAKE OF UPDATING OUR OWN BOARD SO WE CAN MAKE OUR NEXT MOVE
		
class Off_Enemy(EnemyOffense):
	#HERE WE READ THE INPUT OF PLAYER X TEXT FILE
	#WE USE THIS CLASS WHEN THE OPPONENT GROUP IS ON OFFENSE AND WE ARE ON DEFENSE
	#READ FROM THE TEXT FILE THEN CONVERT TO THE FORMAT OF MOVETUPLE
	#USE THIS MOVE TUPLE TO USE THE MAKEMOVE FUNCTION IN MAIN FOR CURRENT PLAYER TYPE
	#THIS IS FOR THE SAKE OF UPDATING OUR OWN BOARD SO WE CAN MAKE OUR NEXT MOVE


		
		
"""class ChessAI_defense(ChessAI_heuristic):
	#For each piece, find it's legal moves.
	#Find legal moves for all opponent pieces.
	#Throw out my legal moves that the opponent could get next turn.
	#From remaining moves, if it puts opponent in check by performing the move, take it.
	#Otherwise pick a random remaining move.	
	
	#Limitation(s): Doesn't include blocking or sacrificial moves of a lesser piece to protect better one.
	
	def __init__(self,name,color,protectionPriority=("queen","rook","bishop","knight","pawn")):
		self.piecePriority = protectionPriority
		ChessAI.__init__(self,name,color)
	
	def GetMove(self,board,color):
		#print "In ChessAI_defense.GetMove"

		myPieces = self.GetMyPiecesWithLegalMoves(board,color)
		enemyPieces = self.GetEnemyPiecesWithLegalMoves(board,color)
		
		#Get "protected" moves - move piece such that opponent can't capture it next turn
		protectedMoveTuples = self.GetProtectedMoveTuples(board,color,myPieces,enemyPieces)
		
		#Top priority - pick a protected move that puts the enemy in check
		#print "Looking for move that puts enemy in check..."
		movesThatPutEnemyInCheck = self.GetMovesThatPutEnemyInCheck(board,color,protectedMoveTuples)
		if len(movesThatPutEnemyInCheck) > 0:
			#print "Picking move that puts enemy in check"
			return movesThatPutEnemyInCheck[random.randint(0,len(movesThatPutEnemyInCheck)-1)]
		
		#Priority #2 - pick a protected move that will move one of player's pieces out of the line of fire
		#piecePriority set when class instantiated
		for pieceType in self.piecePriority:
			#print "Looking for move that protects my "+pieceType+"..."
			piecesProtectedMoves = self.GetMovesThatProtectPiece(board,color,pieceType,protectedMoveTuples)
			if len(piecesProtectedMoves) > 0:
				#print "Picking move that removes "+pieceType+" from danger"
				return piecesProtectedMoves[random.randint(0,len(piecesProtectedMoves)-1)]
		
		#Priority #3 - pick a protected move that will capture one of the enemy's pieces
		for pieceType in self.piecePriority:
			#print "Looking for move that captures enemy "+pieceType+"..."
			capturePieceMoves = self.GetMovesThatCaptureEnemyPiece(board,color,pieceType,protectedMoveTuples)
			if len(capturePieceMoves) > 0:
				#print "Picking move that captures enemy "+pieceType
				return capturePieceMoves[random.randint(0,len(capturePieceMoves)-1)]
		
		#If nothing from priority 1,2,and 3, then just pick any protected move
		if len(protectedMoveTuples) > 0:
			#print "Picking random protected move"
			return protectedMoveTuples[random.randint(0,len(protectedMoveTuples)-1)]
		else:
			#If there aren't any protected moves, revert to random AI
			#print "No protected move exists; going to random's GetMove"
			return ChessAI_random.GetMove(self,board,color)
	
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
		
	def GetProtectedMoveTuples(self,board,color,myPieces,enemyPieces):
		#print "In GetProtectedMoveTuples"
		if color == "black":
			myColor = 'b'
			enemyColor = 'w'
			enemyColor_full = 'white'
		else:
			myColor = 'w'
			enemyColor = 'b'
			enemyColor_full = 'black'
		#Get possible moves that opponent can't get next turn
		protectedMoveTuples = []
		for my_p in myPieces:
			my_legalMoves = self.Rules.GetListOfValidMoves(board,color,my_p)
			toBeRemoved = []
			for my_m in my_legalMoves:
				#make hypothetical move
				fromSquare_r = my_p[0]
				fromSquare_c = my_p[1]
				toSquare_r = my_m[0]
				toSquare_c = my_m[1]
				fromPiece = board[fromSquare_r][fromSquare_c]
				toPiece = board[toSquare_r][toSquare_c]
				board[toSquare_r][toSquare_c] = fromPiece
				board[fromSquare_r][fromSquare_c] = 'e'
				
				for enemy_p in enemyPieces:
					enemy_moves = self.Rules.GetListOfValidMoves(board,enemyColor_full,enemy_p)
					for enemy_m in enemy_moves:
						if enemy_m in my_legalMoves:
							toBeRemoved.append(enemy_m)
				
				#undo temporary move
				board[toSquare_r][toSquare_c] = toPiece
				board[fromSquare_r][fromSquare_c] = fromPiece
				
			for remove_m in toBeRemoved:
				if remove_m in my_legalMoves:
					my_legalMoves.remove(remove_m)
				
			for my_m in my_legalMoves: #now, "dangerous" moves are removed
				protectedMoveTuples.append((my_p,my_m))
		
		return protectedMoveTuples
		
	def GetMovesThatProtectPiece(self,board,color,pieceType,protectedMoveTuples):
		piecesProtectedMoves = []
		piecePositions = self.PiecePositions(board,color,pieceType)
		if len(piecePositions)>0:
			for p in piecePositions:
				if self.PieceCanBeCaptured(board,color,p):
					piecesProtectedMoves.extend(self.GetPiecesMovesFromMoveTupleList(p,protectedMoveTuples))
		return piecesProtectedMoves
	
	def GetMovesThatCaptureEnemyPiece(self,board,color,pieceType,protectedMoveTuples):
		if color == "black":
			myColor = 'b'
			enemyColor = 'w'
			enemyColor_full = 'white'
		else:
			myColor = 'w'
			enemyColor = 'b'
			enemyColor_full = 'black'		
			
		capturePieceMoves = []
		enemyPiecePositions = self.PiecePositions(board,enemyColor,pieceType)
		if len(enemyPiecePositions)>0:
			for p in enemyPiecePositions:
				if self.PieceCanBeCaptured(board,enemyColor,p):
					capturePieceMoves.extend(self.GetCapturePieceMovesFromMoveTupleList(p,protectedMoveTuples))
		return capturePieceMoves
	
	def GetMovesThatPutEnemyInCheck(self,board,color,protectedMoveTuples):
		#print "In GetMovesThatPutEnemyInCheck"
		if color == "black":
			myColor = 'b'
			enemyColor = 'w'
			enemyColor_full = 'white'
		else:
			myColor = 'w'
			enemyColor = 'b'
			enemyColor_full = 'black'		
			
		movesThatPutEnemyInCheck = []
		for mt in protectedMoveTuples:
			if self.Rules.DoesMovePutPlayerInCheck(board,enemyColor_full,mt[0],mt[1]):
				movesThatPutEnemyInCheck.append(mt)
				
		return movesThatPutEnemyInCheck

	def PieceCanBeCaptured(self,board,color,p):	
		#true if opponent can capture the piece as board currently exists.
		if color == "black":
			myColor = 'b'
			enemyColor = 'w'
			enemyColorFull = 'white'
		else:
			myColor = 'w'
			enemyColor = 'b'
			enemyColorFull = 'black'
			
		for row in range(8):
			for col in range(8):
				piece = board[row][col]
				if enemyColor in piece:
					if self.Rules.IsLegalMove(board,enemyColorFull,(row,col),p):
						return True
		return False
		
	def GetCapturePieceMovesFromMoveTupleList(self,p,possibleMoveTuples):
		#returns a subset of possibleMoveTuples that end with p
		moveTuples = []
		for m in possibleMoveTuples:
			if m[1] == p:
				moveTuples.append(m)
		return moveTuples
		
	def GetPiecesMovesFromMoveTupleList(self,p,possibleMoveTuples):
		#returns a subset of possibleMoveTuples that start with p
		moveTuples = []
		for m in possibleMoveTuples:
			if m[0] == p:
				moveTuples.append(m)
		return moveTuples
		
class ChessAI_offense(ChessAI_defense):
	#Same as defense AI, except capturing enemy piece is higher priority than protecting own pieces
	def GetMove(self,board,color):
		#print "In ChessAI_offense.GetMove"

		myPieces = self.GetMyPiecesWithLegalMoves(board,color)
		enemyPieces = self.GetEnemyPiecesWithLegalMoves(board,color)
		
		#Get "protected" moves - move piece such that opponent can't capture it next turn
		protectedMoveTuples = self.GetProtectedMoveTuples(board,color,myPieces,enemyPieces)
		
		#Top priority - pick a protected move that puts the enemy in check
		#print "Looking for move that puts enemy in check..."
		movesThatPutEnemyInCheck = self.GetMovesThatPutEnemyInCheck(board,color,protectedMoveTuples)
		if len(movesThatPutEnemyInCheck) > 0:
			#print "Picking move that puts enemy in check"
			return movesThatPutEnemyInCheck[random.randint(0,len(movesThatPutEnemyInCheck)-1)]

		#Priority #2 - pick a protected move that will capture one of the enemy's pieces
		for pieceType in self.piecePriority:
			#print "Looking for move that captures enemy "+pieceType+"..."
			capturePieceMoves = self.GetMovesThatCaptureEnemyPiece(board,color,pieceType,protectedMoveTuples)
			if len(capturePieceMoves) > 0:
				#print "Picking move that captures enemy "+pieceType
				return capturePieceMoves[random.randint(0,len(capturePieceMoves)-1)]
			
		#Priority #3 - pick a protected move that will move one of player's pieces out of the line of fire
		#piecePriority set when class instantiated
		for pieceType in self.piecePriority:
			#print "Looking for move that protects my "+pieceType+"..."
			piecesProtectedMoves = self.GetMovesThatProtectPiece(board,color,pieceType,protectedMoveTuples)
			if len(piecesProtectedMoves) > 0:
				#print "Picking move that removes "+pieceType+" from danger"
				return piecesProtectedMoves[random.randint(0,len(piecesProtectedMoves)-1)]
		
		#If nothing from priority 1,2,and 3, then just pick any protected move
		if len(protectedMoveTuples) > 0:
			#print "Picking random protected move"
			return protectedMoveTuples[random.randint(0,len(protectedMoveTuples)-1)]
		else:
			#If there aren't any protected moves, revert to random AI
			#print "No protected move exists; going to random's GetMove"
			return ChessAI_heuristic.GetMove(self,board,color)
	
if __name__ == "__main__":
	
	from ChessBoard import ChessBoard
	cb = ChessBoard(3)
	board = cb.GetState()
	color = 'black'
	
	from ChessGUI_pygame import ChessGUI_pygame
	gui = ChessGUI_pygame()
	gui.Draw(board,highlightSquares=[])
	defense = ChessAI_defense('Bob','black')
	
	myPieces = defense.GetMyPiecesWithLegalMoves(board,color)
	enemyPieces = defense.GetEnemyPiecesWithLegalMoves(board,color)
	protectedMoveTuples = defense.GetProtectedMoveTuples(board,color,myPieces,enemyPieces)
	movesThatPutEnemyInCheck = defense.GetMovesThatPutEnemyInCheck(board,color,protectedMoveTuples)
	print "MyPieces = ", cb.ConvertSquareListToAlgebraicNotation(myPieces)
	print "enemyPieces = ", cb.ConvertSquareListToAlgebraicNotation(enemyPieces)
	print "protectedMoveTuples = ", cb.ConvertMoveTupleListToAlgebraicNotation(protectedMoveTuples)
	print "movesThatPutEnemyInCheck = ", cb.ConvertMoveTupleListToAlgebraicNotation(movesThatPutEnemyInCheck)
	c = raw_input("Press any key to quit.")#pause at the end
	"""