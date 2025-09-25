import random

from board import board

def initialise(newBoard,colour):
    global boardGrid

    boardGrid = board(newBoard,colour)

def moe(newBoard,colour,newGame):

    if newGame:
        initialise(newBoard,colour)

    boardGrid.updateBoard(newBoard)

    validColumns = list(boardGrid.getValidColumns())

    for column in validColumns:

        if any(four == 40 for four in boardGrid.getFoursThroughPlacement(column,1)):
            boardGrid.playInColumn(column)
            return column

    myMove = random.choice(validColumns)

    boardGrid.playInColumn(myMove)

    return myMove