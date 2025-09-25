EMPTY_SPACE = ""

def simpleBot(boardGrid, currColour, isNewGame = False):
    if currColour == "Y":
        opponentColour = "R" 
    else:
        opponentColour = "Y"

    centre = len(boardGrid) // 2
    
    #if about to win/lose
    for col in range(len(boardGrid)):
        if isWinningMove(boardGrid, col, currColour) or isWinningMove(boardGrid, col, opponentColour):
            return col

    #prioritise securing the centre
    if EMPTY_SPACE in boardGrid[centre]:
        return centre

    #once centre is filled, start filling adjacent columns
    for offset in range(1, centre + 1):
        for col in (centre - offset, centre + offset):
            if 0 <= col < len(boardGrid) and EMPTY_SPACE in boardGrid[col]:
                return col



def isWinningMove(boardGrid, col, colour):
    row = getLowestEmptySlot(boardGrid, col)
    if row is not None:
        return checkWin(simulatePlacement(boardGrid, col, row, colour), col, row, colour)
    return False


def simulatePlacement(boardGrid, col, rowIndex, colour):
    simulatedGrid = [col[:] for col in boardGrid]
    simulatedGrid[col][rowIndex] = colour
    return simulatedGrid

def getLowestEmptySlot(boardGrid, col):
    if 0 <= col < len(boardGrid):
        for rowIdx, cell in enumerate(boardGrid[col]):
            if cell == EMPTY_SPACE:
                return rowIdx
    return None

def checkWin(boardGrid, colIdx, rowIdx, colour):
    return any(
        checkDirection(boardGrid, colIdx, rowIdx, colDir, rowDir, colour)
        for colDir, rowDir in [(1, 0), (0, 1), (1, 1), (1, -1)]
    )

def checkDirection(boardGrid, startCol, startRow, colDir, rowDir, colour):
    count = 1 + countInDirection(boardGrid, startCol, startRow, colDir, rowDir, colour) + countInDirection(boardGrid, startCol, startRow, -colDir, -rowDir, colour)
    return count >= 4

def countInDirection(boardGrid, startCol, startRow, colDir, rowDir, colour):
    count = 0
    col, row = startCol + colDir, startRow + rowDir
    while 0 <= col < len(boardGrid) and 0 <= row < len(boardGrid[col]) and boardGrid[col][row] == colour:
        count += 1
        col += colDir
        row += rowDir
    return count
