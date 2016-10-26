#import ChessAI

def PiecePositions(board,color,pieceType):
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

def OffenseHeuristicValue(board):
		whiteKnight = PiecePositions(board, "white", "knight")
		whiteKing = PiecePositions(board, "white", "king")
		whiteRook = PiecePositions(board, "white", "rook")
		blackKing = PiecePositions(board, "black", "king")
		blackKnight = PiecePositions(board, "black", "knight")
		#removed self, copy below this line
		
		retval = 0
		
		# Board value loses points for missing white rook or knight
		if whiteKnight[0] == -1:
			retval -= 10000
			print "No white knight, -10000"
		if whiteRook[0] == -1:
			retval -= 10000
			print "No white rook, -10000"
		
		# Gain points for taking enemy knight
		if blackKnight[0] == -1:
			retval += 10000
			print "No black knight, +10000"

		# White king needs to be close to black king for checkmate, lower distance increases value
		retval += 100 * (14 - (abs(whiteKing[0] - blackKing[0]) + abs(whiteKing[1] - blackKing[1])))

		# Good to have knight close to black king to help put in check
		if whiteKnight[0] != -1:
			retval += 50 * (14 - (abs(whiteKnight[0] - blackKing[0]) + abs(whiteKnight[1] - blackKing[1])))
		
		# We want black king to be at edge
		if blackKing[0] == 0 or blackKing[0] == 7\
		   or blackKing[1] == 0 or blackKing[1] == 7:
			retval += 1000
			print "Black king at edge, +1000"

		# But don't want white king at edge, could allow black king to move to center
		if whiteKing[0] == 0 or whiteKing[0] == 7\
		   or whiteKing[1] == 0 or whiteKing[1] == 7:
			retval -= 900
			print "White king at edge, -900"
		
		# Rook can make barrier to block black king from center. Good if +/- 1 row/col
		if (whiteKing[0] > blackKing[0] and whiteRook[0] == (blackKing[0] + 1))\
		   or (whiteKing[1] > blackKing[1] and whiteRook[1] == (blackKing[1] + 1))\
		   or (whiteKing[0] < blackKing[0] and whiteRook[0] == (blackKing[0] - 1))\
		   or (whiteKing[1] < blackKing[1] and whiteRook[1] == (blackKing[1] - 1)):
			retval += 500
			print "Rook barrier"

		# Checkmate conditions: black king at edge, kings 2 or 3 apart, rook on same edge as black king
		if (blackKing[0] == 0 or blackKing[0] == 7 or blackKing[1] == 0 or blackKing[1] == 7) \
		   and ((abs(whiteKing[0] - blackKing[0]) + abs(whiteKing[1] - blackKing[1])) == 2) \
		   and ( (blackKing[0] == 0 and whiteRook[0] == 0) or (blackKing[0] == 7 and whiteRook[0] == 7)\
                         or (blackKing[1] == 0 and whiteRook[1] == 0) or (blackKing[1] == 7 and whiteRook[1] == 7)):
			retval += 100000
			print "Checkmate"

		return retval

board = [['e','e','e','bK','e','e','wR','e'],\
	['e','e','e','e','e','e','e','e'],\
	['e','e','e','wK','e','e','e','e'],\
	['e','e','e','e','e','e','e','e'],\
	['e','e','e','e','e','e','e','e'],\
	['e','e','e','e','e','e','e','e'],\
	['e','e','e','e','e','e','e','e'],\
	['e','e','e','e','e','e','e','e']]



print OffenseHeuristicValue(board)
