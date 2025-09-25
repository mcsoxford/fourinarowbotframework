from math import inf
import json

from board import board

with open("Morris/fourToEvaluation.json", "r") as file:
    fourToEvaluation = json.load(file)

class WeWonException(Exception):
    pass

def initialise(newBoard,colour):
    global boardGrid

    boardGrid = board(newBoard,colour)

def evaluateFour(four):
    evaluation = fourToEvaluation[four]

    match evaluation:
        case -1:
            raise WeWonException
        case -2:
            return inf
        case -3:
            print(four)
            raise ValueError
        case _:
            return evaluation

def morris(newBoard, colour, newGame):
    if newGame:
        initialise(newBoard,colour)

    boardGrid.updateBoard(newBoard)

    bestColumn = None
    bestEvaluation = -inf

    for column in boardGrid.getValidColumns():

        evaluation = 0

        for four in boardGrid.getFoursThroughPlacement(column,0):

            try:
                evaluation += evaluateFour(four)
            except WeWonException:
                boardGrid.playInColumn(column)
                return column

        if evaluation > bestEvaluation:
            bestEvaluation = evaluation
            bestColumn = column

    boardGrid.playInColumn(bestColumn)
    return bestColumn

