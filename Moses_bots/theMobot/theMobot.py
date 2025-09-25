from math import inf
import json

import random

from board import board

with open("theMobot/fourToOurEvaluation.json", "r") as file:
    rawFile = json.load(file)

    fourToOurEvaluation = []
    for i in rawFile:
        if i == -1:
            fourToOurEvaluation.append(inf)
        else:
            fourToOurEvaluation.append(i)

with open("theMobot/fourToOpponentEvaluation.json", "r") as file:
    rawFile = json.load(file)

    fourToOpponentEvaluation = []
    for i in rawFile:
        if i == -1:
            fourToOpponentEvaluation.append(inf)
        else:
            fourToOpponentEvaluation.append(i)


def initialise(newBoard, colour):
    global boardGrid
    global moves
    global totalMoves

    boardGrid = board(newBoard, colour)

    moves = 0
    totalMoves = len(newBoard)*len(newBoard[0])


def theMobot(newBoard, colour, newGame):
    global moves
    global totalMoves

    if newGame:
        initialise(newBoard, colour)

        boardLength = len(boardGrid.getBoard())
        if boardLength % 2 == 0:
            boardGrid.updateBoard(newBoard)

            centre = boardLength // 2

            boardGrid.playInColumn(centre)
            return centre

    boardGrid.updateBoard(newBoard)

    bestColumn = None
    bestEvaluation = -inf

    possibleMoves = list(boardGrid.getValidColumns())

    for column in possibleMoves:

        evaluation = evaluateOurColumn(column,4+int(10*moves/totalMoves))

        if evaluation > bestEvaluation:
            bestEvaluation = evaluation
            bestColumn = column

        if evaluation == inf:
            break

    if bestColumn == None:
        bestColumn = random.choice(possibleMoves)

    boardGrid.playInColumn(bestColumn)

    moves += 1

    return bestColumn


def evaluateOurColumn(column, depth=5):

    if depth == 0:
        return 0

    evaluation = 0

    for four in boardGrid.getFoursThroughPlacement(column, 0):
        evaluation += fourToOurEvaluation[four]

    if evaluation == inf:
        return inf

    boardGrid.setSquare(column, 1)

    bestOpponentEvaluation = -inf

    for opponentMove in list(boardGrid.getValidColumns()):

        opponentEvaluation = evaluateOpponentColumn(opponentMove, depth - 1)

        if opponentEvaluation > bestOpponentEvaluation:
            bestOpponentEvaluation = opponentEvaluation

        if opponentEvaluation == inf:
            break

    boardGrid.unsetSquare(column)

    return evaluation - bestOpponentEvaluation


def evaluateOpponentColumn(column, depth):

    if depth == 0:
        return 0

    evaluation = 0

    for four in boardGrid.getFoursThroughPlacement(column, 0):
        evaluation += fourToOpponentEvaluation[four]

    if evaluation == inf:
        return inf

    boardGrid.setSquare(column, 2)

    ourBestNextEvaluation = -inf

    for ourNextMove in list(boardGrid.getValidColumns()):

        ourNextEvaluation = evaluateOurColumn(ourNextMove, depth - 1)

        if ourNextEvaluation > ourBestNextEvaluation:
            ourBestNextEvaluation = ourNextEvaluation

        if ourNextEvaluation == inf:
            break

    boardGrid.unsetSquare(column)

    return evaluation - ourBestNextEvaluation