# Four-in-a-row Bot Framework
#
#
#

from inspect import signature
from copy import deepcopy

# result constants
RESULT_DRAW = 'Draw'

# space constants
EMPTY_SPACE = ''


# Run a single game returning the result
# moveChooserR/Y need to be functions like:
#
#   def myMoveChooser(boardGrid, myColour)
#       ...
#       return columnIndex
#
# moveChooserR will always go first
#
# boardGrid is a 2D list of board spaces.
# The boardGrid can be different sizes each game but will not change once a game has started.
# 6-10 columns (inclusive) and 6-10
# A space's value is accessed by: boardGrid[columnIndex][rowIndex]
#
# Row index 0 is the bottom of the board
# (i.e. a new piece will occupy the available slot with the lowest rowIndex)
#
# The possible values in a space are:
#     empty string = no piece in the space
#     R = red piece in the space
#     Y = yellow piece in the space
#
# returns a dictionary with the following entries:
#    'boardWH': tuple with the (width, height) of board in spaces
#    'winner': 'R' or 'Y' or 'Draw'
#    'moveSequence': a list of column indexes representing the moves taken by both players
#    'finalBoard': the board grid showing the end of the game
#

def runSingleGame(moveChooserR, moveChooserY, boardWH=(7, 6)):
    boardGrid = [['' for _ in range(boardWH[1])] for __ in range(boardWH[0])]

    moveChoosers = {"R": moveChooserR, "Y": moveChooserY}
    isNewGame = {"R": True, "Y": True}
    currColour = "R"

    moveSequence = []

    winner = None
    while winner == None:
        # get and record the bot's movement choice
        # horrible hack due to API change mid-project
        sig = signature(moveChoosers[currColour])
        if len(sig.parameters) == 3:
            chosenColumnIdx = moveChoosers[currColour](deepcopy(boardGrid), currColour, isNewGame[currColour])

        else:
            chosenColumnIdx = moveChoosers[currColour](deepcopy(boardGrid), currColour)

        moveSequence.append(chosenColumnIdx)
        isNewGame[currColour] = False

        # get the row the piece will fall into in that column
        row = __getLowestEmptySlot(chosenColumnIdx, boardGrid)
        if row is not None:
            # set the cell in the board
            boardGrid[chosenColumnIdx][row] = currColour

            # check for win/draw
            if __moveWins(chosenColumnIdx, row, boardGrid):
                winner = currColour
            elif __boardFull(boardGrid):
                winner = RESULT_DRAW
            else:
                # neither win nor draw, so swap to next player
                currColour = __getOpponentOf(currColour)
        else:
            # invalid move: bot loses through calamitous stupidity
            winner = __getOpponentOf(currColour)

    # construct return structure
    gameInfo = {
        "boardWH": boardWH,
        "winner": winner,
        "moveSequence": moveSequence,
        "finalBoard": boardGrid
    }

    return gameInfo


def displayBoard(boardGrid):
    numCols = len(boardGrid)
    if numCols > 0:
        numRows = len(boardGrid[0])
        if numRows > 0:
            dividerStr = "+" + ("-+" * numCols)
            print(dividerStr)

            for rowIdx in range(numRows - 1, -1, -1):
                rowStr = "|"
                for colIdx in range(numCols):
                    piece = boardGrid[colIdx][rowIdx]
                    if piece == EMPTY_SPACE:
                        piece = " "
                    rowStr += piece + "|"
                print(rowStr)
                print(dividerStr)


def __getLowestEmptySlot(columnIdx, boardGrid):
    result = None

    if columnIdx >= 0 and columnIdx < len(boardGrid):
        column = boardGrid[columnIdx]
        if EMPTY_SPACE in column:
            result = column.index(EMPTY_SPACE)

    return result


def __getOpponentOf(player):
    opponent = None

    if player == "Y":
        opponent = "R"
    elif player == "R":
        opponent = "Y"

    return opponent


def __moveWins(colIdx, rowIdx, boardGrid):
    result = False
    colour = boardGrid[colIdx][rowIdx]

    # check horizontal
    if not result:
        result = __checkForLine(boardGrid, colIdx - 3, rowIdx, colIdx + 3, rowIdx)

    # check vertical
    if not result:
        result = __checkForLine(boardGrid, colIdx, rowIdx - 3, colIdx, rowIdx + 3)

    # check low-left to high-right
    if not result:
        result = __checkForLine(boardGrid, colIdx - 3, rowIdx - 3, colIdx + 3, rowIdx + 3)

    # check high-left to low-right
    if not result:
        result = __checkForLine(boardGrid, colIdx - 3, rowIdx + 3, colIdx + 3, rowIdx - 3)

    return result


def sign(value):
    result = 0
    if value > 0:
        result = 1
    elif value < 0:
        result = -1
    return result


def __safeGet(boardGrid, col, row):
    result = None
    if 0 <= col < len(boardGrid) and \
            0 <= row < len(boardGrid[0]):
        result = boardGrid[col][row]
    return result

def __checkForLine(boardGrid, startCol, startRow, endCol, endRow):
    # print(f"Check {startCol}:{startRow} -> {endCol}:{endRow}")
    colSpan = abs(endCol - startCol) + 1
    rowSpan = abs(endRow - startRow) + 1
    colDir = sign(endCol - startCol)
    rowDir = sign(endRow - startRow)
    # print(f"colSpan,rowSpan = {colSpan},{rowSpan}")
    currCol = startCol
    currRow = startRow
    lineCol = __safeGet(boardGrid, currCol, currRow)
    lineLength = 0

    for _ in range(max(colSpan, rowSpan)):

        colour = __safeGet(boardGrid, currCol, currRow)
        # print(f"\tGot {colour} at {currCol}:{currRow}")
        if colour is not None:
            if colour == lineCol:
                lineLength += 1
                # print(f"\t\tincreased lineLength to {lineLength}")
                if lineLength >= 4:
                    return True
            else:
                # print(f"\t\treset lineLength to 1")
                lineLength = 1
                lineCol = colour
        else:
            # print(f"\t\treset lineLength to 0")
            lineLength = 0
            lineCol = None
        currCol += colDir
        currRow += rowDir

def __boardFull(boardGrid):
    result = True
    for column in boardGrid:
        if EMPTY_SPACE in column:
            result = False
    return result


if __name__ == "__main__":
    def testCheckForLine():
        boardGrid = [["R", "R", "R", ""],
                     ["Y", "Y", "Y", ""],
                     ["R", "R", "R", ""],
                     ["Y", "Y", "Y", ""],
                     ["R", "R", "R", ""],
                     ["Y", "Y", "Y", ""]
                     ]
        print("Should be None: ", __checkForLine(boardGrid, 0, -3, 0, 3))
        print("Should be None: ", __checkForLine(boardGrid, -3, 0, 3, 0))
        # should have more tests here, but MEH


    # run a game
    def testRunGame():
        def horizontalChooser(boardGrid, colour):
            choice = dumChooserInfo[colour]
            dumChooserInfo[colour] = (choice + 1) % len(boardGrid)
            return choice

        def verticalChooser(boardGrid, colour):
            choice = dumChooserInfo[colour]
            return choice

        def diagonalHLtoLRChooser(boardGrid, colour):
            choice = dumChooserInfo["R"]
            dumChooserInfo["R"] = (choice + 1) % len(boardGrid)
            return choice

        def diagonalLLtoHRChooser(boardGrid, colour):
            choice = dumChooserInfo["R"]
            newChoice = choice - 1
            if newChoice < 0:
                newChoice = len(boardGrid) - 1
            dumChooserInfo["R"] = newChoice
            return choice

        dumChooserInfo = {"R": 0, "Y": 1}
        result = runSingleGame(verticalChooser, verticalChooser)
        expected = {'boardWH': (7, 6), 'winner': 'R', 'moveSequence': [0, 1, 0, 1, 0, 1, 0],
                    'finalBoard': [['R', 'R', 'R', 'R', '', ''], ['Y', 'Y', 'Y', '', '', ''], ['', '', '', '', '', ''],
                                   ['', '', '', '', '', ''], ['', '', '', '', '', ''], ['', '', '', '', '', ''],
                                   ['', '', '', '', '', '']]}
        if result != expected:
            print("FAIL!")
            displayBoard(result["finalBoard"])
            print(result)

        dumChooserInfo = {"R": 0, "Y": 0}
        result = runSingleGame(horizontalChooser, horizontalChooser)
        expected = {'boardWH': (7, 6), 'winner': 'R', 'moveSequence': [0, 0, 1, 1, 2, 2, 3],
                    'finalBoard': [['R', 'Y', '', '', '', ''], ['R', 'Y', '', '', '', ''], ['R', 'Y', '', '', '', ''],
                                   ['R', '', '', '', '', ''], ['', '', '', '', '', ''], ['', '', '', '', '', ''],
                                   ['', '', '', '', '', '']]}
        if result != expected:
            print("FAIL!")
            displayBoard(result["finalBoard"])
            print(result)

        dumChooserInfo = {"R": 0, "Y": 0}
        result = runSingleGame(diagonalHLtoLRChooser, diagonalHLtoLRChooser)
        expected = {'boardWH': (7, 6), 'winner': 'Y',
                    'moveSequence': [0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0],
                    'finalBoard': [['R', 'Y', 'R', 'Y', '', ''], ['Y', 'R', 'Y', '', '', ''],
                                   ['R', 'Y', 'R', '', '', ''], ['Y', 'R', 'Y', '', '', ''],
                                   ['R', 'Y', 'R', '', '', ''], ['Y', 'R', 'Y', '', '', ''],
                                   ['R', 'Y', 'R', '', '', '']]}
        if result != expected:
            print("FAIL!")
            displayBoard(result["finalBoard"])
            print(result)

        dumChooserInfo = {"R": 6, "Y": 6}
        result = runSingleGame(diagonalLLtoHRChooser, diagonalLLtoHRChooser)
        expected = {'boardWH': (7, 6), 'winner': 'Y',
                    'moveSequence': [6, 5, 4, 3, 2, 1, 0, 6, 5, 4, 3, 2, 1, 0, 6, 5, 4, 3, 2, 1, 0, 6],
                    'finalBoard': [['R', 'Y', 'R', '', '', ''], ['Y', 'R', 'Y', '', '', ''],
                                   ['R', 'Y', 'R', '', '', ''], ['Y', 'R', 'Y', '', '', ''],
                                   ['R', 'Y', 'R', '', '', ''], ['Y', 'R', 'Y', '', '', ''],
                                   ['R', 'Y', 'R', 'Y', '', '']]}
        if result != expected:
            print("FAIL!")
            displayBoard(result["finalBoard"])
            print(result)


    testCheckForLine()
    testRunGame()