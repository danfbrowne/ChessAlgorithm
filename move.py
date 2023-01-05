from piece import *

#Global Variables
isWhiteTurn = True
promotionType = None

#(x,y): current position of piece
#(newX,newY): new position of piece
def movePiece(x,y,newX,newY):
    if (pickUp(x,y)):
        return release(newX,newY)

#p: piece
#(x,y): new position of pawn
#return True if successful
def movePawn(p, x, y):
    if contains(x,y) != None:
        if contains(x,y).side != p.side and p.canCaptureOn(x,y):
            capture(x,y)
            update(p,x,y)
            promotionCheck(p,y)
            return True
        return False
    if p.canEnPassant(x,y):
        if p.side == 0:
            capture(x,3)
        if p.side == 1:
            capture(x,4)
        update(p,x,y)
        return True
    if p.canMove(x,y):
        update(p,x,y)
        promotionCheck(p,y)
        return True
    return False

def promotionCheck(p,y):
    global promotionType
    if (y == 7 and p.side == 1) or (y == 0 and p.side == 0):
        promotion = str(promote())
        if promotion == "queen":
            newPiece = Queen(p.xPos,p.yPos,p.side)
        elif promotion == "rook":
            newPiece = Rook(p.xPos,p.yPos,p.side,False)
        elif promotion == "knight":
            newPiece = Knight(p.xPos,p.yPos,p.side)
        else:
            newPiece = Bishop(p.xPos,p.yPos,p.side)
        board.remove(p)
        board.append(newPiece)
        promotionType = None

def promote():
    global promotionType
    valid = False
    validPromotes = ["queen", "bishop", "rook", "knight"]
    if promotionType == None:
        while not valid:
            promote = input("\nWhat should this pawn be promoted to? ('queen', 'rook', 'bishop', or 'knight')\n")
            if promote in validPromotes:
                valid = True
            else:
                print("\nERROR: invalid promotion type!\n")
    else:
        promote = promotionType
    return promote

#p: piece
#(x,y): new position of pawn
#return True if successful
def moveKing(p, x, y):
    if p.canMove(x,y):
        if contains(x,y) != None:
            if contains(x,y).side != p.side:
                capture(x,y)
                update(p,x,y)
                return True
            return False
        if not isAttacked(x,y,p):
            update(p,x,y)
            return True
    if p.canKSC() and x == 6 and ((p.side == 0 and y == 7) or (p.side == 1 and y == 0)):
        p.xPos = 6
        contains(7,p.yPos).xPos = 5
        return True
    if p.canQSC() and x == 2 and ((p.side == 0 and y == 7) or (p.side == 1 and y == 0)):
        p.xPos = 2
        contains(0,p.yPos).xPos = 3
        return True
    return False

#TODO: test all possible moves for the player to test for checkmate
#playerSide: side evaluated for checkmate
#return True if player is in checkmate
def isCheckMated(playerSide):
    newBoard = board
    safecount = 0
    for p in newBoard:
        if pickUp(p.xPos,p.yPos):
            old_p = p.copy()
            old_p.isHeld = False
            for i in range(8):
                for j in range (8):
                    if checkRelease(i,j,p):
                        if not kingInCheck(p.side):
                            safecount += 1
                        return True
                        newBoard.remove(i)
                        newBoard.append(old_p)
                    return False

    if safecount == 0:
        return True
    return False
    """
    savedBoard = board
    newBoard = savedBoard
    p = None
    for i in newBoard:
        if i.side == playerSide and i.pieceType == "king":
            p = i
    safeCheck = 0
    for i in newBoard:
        for j in range(0,8):
            for k in range(0,8):
                newBoard = savedBoard
                if i.canCaptureOn(j,k) and contains(j,k):
                    if contains(j,k).side is not i.side:
                        newBoard.remove(contains(j,k))
                        update(i,j,k)
                elif i.canMove(j,k):
                    update(i,j,k)
                if not isAttacked(p.xPos, p.yPos, p):
                        safeCheck += 1
    if safeCheck is 0:
        return True
    return False
    """

#def kingQuickCheck(playerSide, newBoard):


#playerSide: side evaluated for check
#return True if player is in check
def kingInCheck(playerSide):
    king = None
    for i in board:
        if i.side == playerSide and i.pieceType == "king":
            king = i
    if king is not None:
        if (isAttacked(king.xPos, king.yPos, king)):
            return True
    return False

#(x,y): location for piece to be removed
def capture(x,y):
    board.remove(contains(x,y))

#populates board with pieces to start a standard game
def fillBoard():
    for i in range(8):
        p1 = Pawn(i,1,1)
        board.append(p1)
        p1 = Pawn(i,6,0)
        board.append(p1)
    
    p1 = Rook(0,0,1,False)
    board.append(p1)
    p1 = Rook(7,0,1,True)
    board.append(p1)
    p1 = Rook(0,7,0,False)
    board.append(p1)
    p1 = Rook(7,7,0,True)
    board.append(p1)

    p1 = Knight(1,0,1)
    board.append(p1)
    p1 = Knight(6,0,1)
    board.append(p1)
    p1 = Knight(1,7,0)
    board.append(p1)
    p1 = Knight(6,7,0)
    board.append(p1)

    p1 = Bishop(2,0,1)
    board.append(p1)
    p1 = Bishop(5,0,1)
    board.append(p1)
    p1 = Bishop(2,7,0)
    board.append(p1)
    p1 = Bishop(5,7,0)
    board.append(p1)

    p1 = King(4,0,1)
    board.append(p1)
    p1 = King(4,7,0)
    board.append(p1)

    p1 = Queen(3,7,0)
    board.append(p1)
    p1 = Queen(3,0,1)
    board.append(p1)

def resetBoard():
    global isWhiteTurn
    global moveNum
    board.clear()
    moveNum = 1
    isWhiteTurn = True
    promotionType = None

#returns piece that is "held"
def findHeld():
    for i in board:
        if i.isHeld:
            return i
    return None

#p: piece to be updated
#(x,y): new location of piece
def update(p, x, y):
    if p.pieceType == "pawn":
        if abs(p.yPos - y) == 2:
            p.movedTwo = True
    p.xPos = x
    p.yPos = y
    p.lastMoved = getMoveNum()

#(x,y): location of piece to be picked up
#return True if piece is picked up
def pickUp(x,y):
    if findHeld() == None:
        if contains(x,y) != None:
            if (contains(x,y).side == 0 and isWhiteTurn) or (contains(x,y).side == 1 and not isWhiteTurn):
                contains(x,y).isHeld = True
                return True
    return False

#(x,y): location of the piece to be released
#updates turn counter player's turn
def release(x,y):
    global isWhiteTurn
    if releaseCheck(x,y):
        isWhiteTurn = not isWhiteTurn
        increaseMoveNum()
        return True
    return False

def releaseCheck(x,y):
    p = findHeld()
    old_p = p.copy()
    old_p.isHeld = False
    if checkRelease(x,y,p):
        if kingInCheck(p.side):
            board.remove(p)
            board.append(old_p)
            return False
        return True
    return False

def checkRelease(x,y,p):
    p.isHeld = False
    if p.pieceType == "pawn":
        return movePawn(p,x,y)
    if p.pieceType == "king":
        return moveKing(p,x,y)
    if p.canMove(x,y):
        if contains(x,y) != None:
            if contains(x,y).side != p.side:
                capture(x,y)
                update(p,x,y)
                return True
            return False
        update(p,x,y)
        return True
    return False            

def pieceLetter(Piece):
    if Piece.pieceType == "pawn":
        if Piece.side == 0:
            return "P"
        else:
            return "p"
    elif Piece.pieceType == "rook":
        if Piece.side == 0:
            return "R"
        else:
            return "r"
    elif Piece.pieceType == "knight":
        if Piece.side == 0:
            return "N"
        else:
            return "n"
    elif Piece.pieceType == "bishop":
        if Piece.side == 0:
            return "B"
        else:
            return "b"
    elif Piece.pieceType == "queen":
        if Piece.side == 0:
            return "Q"
        else:
            return "q"
    elif Piece.pieceType == "king":
        if Piece.side == 0:
            return "K"
        else:
            return "k"

def printBoard():
    print("   a b c d e f g h ")
    for i in range(8):
        row = i
        print("%d [" % (8-i), end = '')
        for j in range(8):
            if contains(j,i) != None:
                if not contains(j,i).isHeld:
                    print(pieceLetter(contains(j,i)), end = ''),
                else:
                    print("_", end = '')
            else:
                print("_", end = '')
            if j != 7:
                print("|", end = '')
        print("]",)
    print()

def convertToString():
    emptyCount = 0
    boardlist = []
    for i in range(8):
        emptyCount = 0
        if i >= 1:
            if i <= 7:
                boardlist.append("/")
        for j in range(8):
            if contains(j,i) != None:
                if not contains(j,i).isHeld:
                    if emptyCount > 0:
                        boardlist.append(str(emptyCount))
                        emptyCount = 0
                    pieceString = pieceLetter(contains(j,i))
                    boardlist.append(pieceString)
                else:
                    if j == 7:
                        emptyCount = emptyCount + 1
                        boardlist.append(str(emptyCount))
                    emptyCount = emptyCount + 1
            else:
                if j == 7:
                    emptyCount = emptyCount + 1
                    boardlist.append(str(emptyCount))
                    emptyCount = 0
                emptyCount = emptyCount + 1
    boardString = ''.join(boardlist)
    return boardString

        

def moveParse(string):
    letters = 0
    numbers = 0
    reqX = None
    reqY = None
    destX = None
    destY = None
    for i in range(len(string)-1,-1,-1):
        if (ord(string[i]) > 96 and ord(string[i]) < 105):
            if destX is None:
                destX = ord(string[i]) - 97
            else:
                reqX = ord(string[i]) - 97 
        elif (ord(string[i]) > 48 and ord(string[i]) < 57):
            if destY is None:
                destY = 8 - (ord(string[i]) - 48)
            else:
                reqY = 8 - (ord(string[i]) - 48)

    return (reqX,reqY,destX,destY)

def typeParse(string):
    pType = "None"
    files = ['a','b','c','d','e','f','g','h']
    if string[0] == 'N':
        pType = "knight"
    elif string[0] == 'B':
        pType = "bishop"
    elif string[0] == 'R':
        pType = "rook"
    elif string[0] == 'K':
        pType = "king"
    elif string[0] == 'Q':
        pType = "queen"
    elif string[0] in files:
        pType = "pawn"
    return pType

def convertMove(string):
    (reqX,reqY,destX,destY) = moveParse(string)
    pType = typeParse(string)
    global promotionType
    if pType is None:
        return False
    if "=" in string:
        promotionType = typeParse(string[-1])
    if string[0] == '0' or string[0] == 'O':
        if len(string) == 5:
            if isWhiteTurn:
                return movePiece(4,7,2,7)
            else:
                return movePiece(4,0,2,0)
        else:
            if isWhiteTurn:
                return movePiece(4,7,6,7)
            else:
                return movePiece(4,0,6,0)
    for i in board:
        if (i.pieceType is pType) and (bool(i.side) is not isWhiteTurn):
            if (i.canMove(destX,destY) and not "x" in string) or (i.canCaptureOn(destX,destY) and "x" in string):
                reqFaults = 0
                if reqX is not None:
                    if i.xPos is not reqX:
                        reqFaults += 1
                if reqY is not None:
                    if i.yPos is not reqY:
                        reqFaults += 1
                if reqFaults == 0:
                    return movePiece(i.xPos, i.yPos, destX,destY)
    return False
    
def chessMove(string):
    if (convertMove(string)):
        print("")
        printBoard()
        return True
    else:
        print("\nMove " + string + " is invalid!\n"),
        return False