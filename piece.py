board = []
moveNum = 1

def contains(x,y):
        for i in board:
            if i.xPos is x and i.yPos is y:
                return i
        return None

def isAttacked(x,y,piece):
    for i in board:
        if piece.side != i.side:
            if i.canCaptureOn(x,y):
                return True
    return False

def increaseMoveNum():
    global moveNum
    moveNum += 1

def getMoveNum():
    global moveNum 
    return moveNum

class Piece:
    def __init__(self, xPos, yPos, side, pieceType):
        self.xPos = xPos
        self.yPos = yPos
        self.side = side
        self.pieceType = pieceType
        self.isHeld = False
        self.lastMoved = 0
    
    def canMove(self,x,y):
        if x <= 7 and y <= 7:
            return True
        return False

    def pieceBlocking(self,x,y):
        if contains(x,y) != None:
            if contains(x,y).side == self.side:
                return True
        return False
    
    def canCaptureOn(self,x,y):
        if self.canMove(x,y) and not self.pieceBlocking(x,y):
            return True
        return False
    
    def copy(self):
        copy = Piece(self.xPos,self.yPos,self.side,self.pieceType)
        copy.isHeld = self.isHeld
        copy.lastMoved = self.lastMoved
        return copy

##################################################
#                      PAWN                      #
##################################################                                         

class Pawn(Piece):
    def __init__(self, xPos, yPos, side):
        Piece.__init__(self,xPos,yPos,side,"pawn")
        self.movedTwo = False
    
    def canMove(self,x,y):
        if ((self.yPos == 1 and self.side == 1 and x == self.xPos and y == 3 and contains(x,2) == None and contains(x,3) == None) or        #first move black
                (self.yPos == 6 and self.side == 0 and x == self.xPos and y == 4 and contains(x,5) == None and contains(x,4) == None) or    #first move white
                (y - self.yPos == 1 and x == self.xPos and self.side == 1 and contains(x,y) == None) or                                     #normal move black
                (y - self.yPos == -1 and x == self.xPos and self.side == 0 and contains(x,y) == None)):                                     #normal move white
            return True
        return False
    
    def pieceBlocking(self,x,y):
        Piece.pieceBlocking(x,y)
    
    def canCaptureOn(self,x,y):
        if abs(self.xPos - x) == 1 and ((self.side == 0 and y - self.yPos == -1) or (self.side == 1 and y - self.yPos == 1)):
            return True
        return False

    def canEnPassant(self,x,y):
        if abs(self.xPos - x) == 1 and ((self.side == 0 and y - self.yPos == -1 and y == 2 and contains(x,3) != None) or (self.side == 1 and y - self.yPos == 1 and y == 5 and contains(x,4) != None)):
            if (self.side == 0) and (contains(x,3).side == 1) and (contains(x,3).pieceType == "pawn") and (contains(x,3).lastMoved == moveNum - 1) and contains(x,3).movedTwo:
                return True
            if self.side == 1 and contains(x,4).side == 0 and contains(x,4).pieceType == "pawn" and contains(x,4).lastMoved == moveNum - 1 and contains(x,4).movedTwo:
                return True
        return False
    
    def copy(self):
        copy = Pawn(self.xPos,self.yPos,self.side)
        copy.isHeld = self.isHeld
        copy.lastMoved = self.lastMoved
        copy.movedTwo = self.movedTwo
        return copy
    
##################################################
#                     KNIGHT                     #
##################################################

class Knight(Piece):
    def __init__(self, xPos, yPos, side):
        Piece.__init__(self,xPos,yPos,side,"knight")
    
    def canMove(self,x,y):
        if ((abs(x - self.xPos) == 1 and abs(y - self.yPos) == 2) or 
        abs(x - self.xPos) == 2 and abs(y - self.yPos) == 1):
            return True
        return False

    def pieceBlocking(self,x,y):
        if contains(x,y) != None:
            if contains(x,y).side == self.side:
                return True
        return False
    
    def canCaptureOn(self,x,y):
        if self.canMove(x,y) and not self.pieceBlocking(x,y):
            return True
        return False
    
    def copy(self):
        copy = Knight(self.xPos,self.yPos,self.side)
        copy.isHeld = self.isHeld
        copy.lastMoved = self.lastMoved
        return copy

##################################################
#                     BISHOP                     #
##################################################

class Bishop(Piece):
    def __init__(self, xPos, yPos, side):
        Piece.__init__(self,xPos,yPos,side,"bishop")
    
    def canMove(self,x,y):
        if abs(x - self.xPos) == abs(y - self.yPos) and x != self.xPos and not self.pieceBlocking(x,y):
            return True
        return False

    def pieceBlocking(self,x,y):
        if contains(x,y) != None:
            if contains(x,y).side == self.side:
                return True
        if self.xPos < x and self.yPos < y:
            for i in range(1,x-self.xPos):
                if contains(self.xPos+i,self.yPos+i) != None:
                    return True
        elif self.xPos < x and self.yPos > y:
            for i in range(1,x-self.xPos):
                if contains(self.xPos+i,self.yPos-i) != None:
                    return True
        elif self.xPos > x and self.yPos < y:
            for i in range(1,self.xPos-x):
                if contains(self.xPos-i,self.yPos+i) != None:
                    return True
        else:
            for i in range(1,self.xPos-x):
                if contains(self.xPos-i,self.yPos-i) != None:
                    return True
        return False
    
    def canCaptureOn(self,x,y):
        if self.canMove(x,y) and not self.pieceBlocking(x,y):
            return True
        return False
    
    def Bishop(self):
        copy = Pawn(self.xPos,self.yPos,self.side)
        copy.isHeld = self.isHeld
        copy.lastMoved = self.lastMoved
        return copy

##################################################
#                      ROOK                      #
##################################################

class Rook(Piece):
    def __init__(self, xPos, yPos, side, isKingSide):
        Piece.__init__(self,xPos,yPos,side,"rook")
        self.isKingSide = isKingSide
    
    def canMove(self,x,y):
        if ((x == self.xPos and y != self.yPos) or (x != self.xPos and y == self.yPos)) and not self.pieceBlocking(x,y):
            return True
        return False

    def pieceBlocking(self,x,y):
        if contains(x,y) != None:
            if contains(x,y).side == self.side:
                return True
        if (self.xPos < x):
            for i in range(self.xPos+1, x):
                if contains(i,self.yPos) != None:
                    return True
        elif (self.xPos > x):
            for i in range(self.xPos-1, x, -1):
                if contains(i,self.yPos) != None:
                    return True
        elif (self.yPos < y):
            for i in range(self.yPos+1, y):
                if contains(self.xPos,i) != None:
                    return True
        else:
            for i in range(self.yPos-1, y, -1):
                if contains(self.xPos,i) != None:
                    return True
        return False
    
    def canCaptureOn(self,x,y):
        if self.canMove(x,y) and not self.pieceBlocking(x,y):
            return True
        return False

    def copy(self):
        copy = Rook(self.xPos,self.yPos,self.side,self.isKingSide)
        copy.isHeld = self.isHeld
        copy.lastMoved = self.lastMoved
        return copy

##################################################
#                      KING                      #
##################################################

class King(Piece):
    def __init__(self, xPos, yPos, side):
        Piece.__init__(self,xPos,yPos,side,"king")
    
    def canMove(self,x,y):
        if (contains(x,y) is not None):
            if (abs(x - self.xPos) <= 1 and abs(y - self.yPos) <= 1) and not (x == self.xPos and y == self.yPos) and contains(x,y).side is not self.side:
                return True
        if (abs(x - self.xPos) <= 1 and abs(y - self.yPos) <= 1) and not (x == self.xPos and y == self.yPos) and not isAttacked(x,y,self):
            return True
        return False

    def pieceBlocking(self,x,y):
        if contains(x,y) != None:
            if contains(x,y).side == self.side:
                return True
        return False
    
    def canCaptureOn(self,x,y):
        if self.canMove(x,y) and not self.pieceBlocking(x,y):
            return True
        return False
    
    def canKSC(self):
        for i in board:
            if i.pieceType == "rook":
                if i.isKingSide and i.side == self.side and i.lastMoved == 0 and self.lastMoved == 0:
                    if self.side == 0:
                        if contains(5,7) == None and contains(6,7) == None and not isAttacked(6,7,self) and not isAttacked(5,7,self) and not isAttacked(4,7,self):
                            return True
                    if self.side == 1:
                        if contains(5,0) == None and contains(6,0) == None and not isAttacked(6,0,self) and not isAttacked(5,0,self) and not isAttacked(4,0,self):
                            return True
        return False
    
    def canQSC(self):
        for i in board:
            if i.pieceType == "rook":
                if not i.isKingSide and i.side == self.side and i.lastMoved == 0 and self.lastMoved == 0:
                    if self.side == 0:
                        if contains(3,7) == None and contains(2,7) == None and contains(1,7) == None and not isAttacked(4,7,self) and not isAttacked(3,7,self) and not isAttacked(2,7,self) and not isAttacked(1,7,self):
                            return True
                    if self.side == 1:
                        if contains(3,0) == None and contains(2,0) == None and contains(1,0) == None and not isAttacked(4,0,self) and not isAttacked(3,0,self) and not isAttacked(2,0,self) and not isAttacked(1,0,self):
                            return True
        return False

    def copy(self):
        copy = King(self.xPos,self.yPos,self.side)
        copy.isHeld = self.isHeld
        copy.lastMoved = self.lastMoved
        return copy

##################################################
#                     QUEEN                      #
##################################################

class Queen(Piece):
    def __init__(self, xPos, yPos, side):
        Piece.__init__(self,xPos,yPos,side,"queen")
    
    def canMove(self,x,y):
        if (((x == self.xPos and y != self.yPos) or (x != self.xPos and y == self.yPos)) and not self.pieceBlocking(x,y)):
            return True
        if (abs(x - self.xPos) == abs(y - self.yPos)) and (x != self.xPos) and not(self.pieceBlocking(x,y)):
            return True
        return False

    def pieceBlocking(self,x,y):
        if contains(x,y) != None:
            if contains(x,y).side == self.side:
                return True
        if self.xPos < x and self.yPos < y:
            for i in range(1,x-self.xPos):
                if contains(self.xPos+i,self.yPos+i) != None:
                    return True
        elif self.xPos < x and self.yPos > y:
            for i in range(1,x-self.xPos):
                if contains(self.xPos+i,self.yPos-i) != None:
                    return True
        elif self.xPos > x and self.yPos < y:
            for i in range(1,self.xPos-x):
                if contains(self.xPos-i,self.yPos+i) != None:
                    return True
        elif self.xPos > x and self.yPos > y:
            for i in range(1,self.xPos-x):
                if contains(self.xPos-i,self.yPos-i) != None:
                    return True
        elif (self.xPos < x and self.yPos == y):
            for i in range(self.xPos+1, x):
                if contains(i,self.yPos) != None:
                    return True
        elif (self.xPos > x and self.yPos == y):
            for i in range(self.xPos-1, x, -1):
                if contains(i,self.yPos) != None:
                    return True
        elif (self.yPos < y and self.xPos == x):
            for i in range(self.yPos+1, y):
                if contains(self.xPos,i) != None:
                    return True
        else:
            for i in range(self.yPos-1, y, -1):
                if contains(self.xPos,i) != None:
                    return True
        return False
    
    def canCaptureOn(self,x,y):
        if self.canMove(x,y) and not self.pieceBlocking(x,y):
            return True
        return False
    
    def copy(self):
        copy = Queen(self.xPos,self.yPos,self.side)
        copy.isHeld = self.isHeld
        copy.lastMoved = self.lastMoved
        return copy