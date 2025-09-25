from copy import deepcopy

class board:
    def __init__(self, boardGrid, ourColour):
        self._columnPositions = [0] * len(boardGrid)
        self._height = len(boardGrid[0])
        self._width = len(boardGrid)
        self._top = self._height-1
        self._right = self._width-1

        self._boardGrid = [[0]*self._height for _ in range(self._width)]

        self._validColumns = list(range(self._width))

        self._ourColour = ourColour
        if self._ourColour == "R":
            self._oppositeColour = "Y"
        else:
            self._oppositeColour = "R"

    def updateBoard(self, newboardGrid):
        for column in self._validColumns:
            if newboardGrid[column][self._columnPositions[column]] == self._oppositeColour:

                self._boardGrid[column][self._columnPositions[column]] = 2

                self._columnPositions[column] += 1

                if self._columnPositions[column] == self._height:
                    self._validColumns.remove(column)

                break

    def setSquare(self,column,colour):

        self._boardGrid[column][self._columnPositions[column]] = colour

        self._columnPositions[column] += 1

        if self._columnPositions[column] == self._height:
            self._validColumns.remove(column)

    def unsetSquare(self,column):

        if self._columnPositions[column] == self._height:
            self._validColumns.append(column)

        self._columnPositions[column] -= 1

        self._boardGrid[column][self._columnPositions[column]] = 0

    def playInColumn(self, column):

        self._boardGrid[column][self._columnPositions[column]] = 1

        self._columnPositions[column] += 1
        if self._columnPositions[column] == self._height:
            self._validColumns.remove(column)

    def getValueAtCoordinates(self, x, y):

        if x < 0 or x >= self._width or y < 0 or y >= self._height:
            return None

        return self._boardGrid[x][y]

    def getFoursThroughPlacement(self, column, squareValue):

        row = self._columnPositions[column]

        self._boardGrid[column][row] = squareValue

        top = min(row+3,self._top)
        bottom = max(row-3,0)
        left = max(column-3,0)
        right = min(column+3,self._right)

        distanceToLeft = column-left
        distanceToRight = right-column
        distanceToTop = top-row
        distanceToBottom = row-bottom

        mainDiagonalLeft = min(distanceToLeft, distanceToBottom)
        mainDiagonalRight = min(distanceToRight, distanceToTop)
        antiDiagonalLeft = min(distanceToLeft, distanceToTop)
        antiDiagonalRight = min(distanceToRight, distanceToBottom)

        for four in self.getVerticalFours(bottom,top,column,row):
            yield four

        for four in self.getFoursInLine(left,row,right,0):
            yield four

        for four in self.getFoursInLine(column-mainDiagonalLeft,row-mainDiagonalLeft,column+mainDiagonalRight,1):
            yield four

        for four in self.getFoursInLine(column-antiDiagonalLeft,row+antiDiagonalLeft,column+antiDiagonalRight,-1):
            yield four

        self._boardGrid[column][row] = 0

    def getVerticalFours(self,bottom,top,column,row):
        hash = 0

        for i in range(3-(top-row)):
            hash *= 3
            hash += self._boardGrid[column][row-i]

        for i in range(row - 3+(top-row),bottom-1,-1):
            hash *= 3
            hash += self._boardGrid[column][i]
            yield hash

    def getFoursInLine(self,startX,startY,endX,directionY):
        hash = 0

        lineLength = endX-startX + 1
        if lineLength < 4:
            return

        for i in range(3):
            hash += self._boardGrid[startX+i][startY+i*directionY]
            hash *= 3

        for i in range(3,lineLength):
            hash += self._boardGrid[startX+i][startY+i*directionY]
            yield hash
            hash -= self._boardGrid[startX+i-3][startY+(i-3)*directionY]*27
            hash *= 3

    def getValidColumns(self):
        for column in self._validColumns:
            yield column
    
    def getColumnPositions(self):
        for position in self._columnPositions:
            yield position

    def getOurColour(self):
        return self._ourColour

    def getOppositeColour(self):
        return self._oppositeColour
    
    def getBoard(self):
        return deepcopy(self._boardGrid)

    

class boardCopy(board):
    def __init__(self,boardToCopy):
        self._boardGrid = boardToCopy.getBoard()

        self._height = len(self._boardGrid[0])
        self._width = len(self._boardGrid)
        self._top = self._height - 1
        self._right = self._width - 1
        
        self._columnPositions = list(boardToCopy.getColumnPositions())
        self._validColumns = list(boardToCopy.getValidColumns())
        
        self._ourColour = boardToCopy.getOurColour()
        self._oppositeColour = boardToCopy.getOppositeColour()
        
