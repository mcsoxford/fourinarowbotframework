import random
from math import inf

from board import board,boardCopy

RESOLUTION = 500

def initialise(newBoard,colour):
    global boardGrid

    boardGrid = board(newBoard,colour)

def getResult(winningHash,toPutDown,column,board):
    if any(four == winningHash for four in board.getFoursThroughPlacement(column,toPutDown)):
        return True
    else:
        return False

def playGame(board,column):

    while True:
        toPutDown = 1
        winningHash = 40

        if getResult(winningHash,toPutDown,column,board):
            return True

        board.setSquare(column,toPutDown)
        validColumns = list(board.getValidColumns())

        try:
            column = random.choice(validColumns)
        except IndexError:
            return True

        toPutDown = 2
        winningHash = 80

        if getResult(winningHash,toPutDown,column,board):
            return False

        board.setSquare(column,toPutDown)
        validColumns = list(board.getValidColumns())

        try:
            column = random.choice(validColumns)
        except IndexError:
            return True

def monty(newBoard,colour,newGame):

    if newGame:
        initialise(newBoard,colour)

    boardGrid.updateBoard(newBoard)

    validColumns = list(boardGrid.getValidColumns())

    bestEvaluation = -inf
    bestColumn = None

    for column in validColumns:

        evaluation = 0

        for _ in range(RESOLUTION):
            if playGame(boardCopy(boardGrid),column):
                evaluation += 1

        if evaluation > bestEvaluation:
            bestEvaluation = evaluation
            bestColumn = column

    boardGrid.playInColumn(bestColumn)

    return bestColumn