#========================================================
# Four-in-a-row test runner
#========================================================

import fourinarow
from random import choice

from fourinarow import runSingleGame


def randomMoveChooser(boardGrid, colour):

    possibleChoices = []
    for colIdx, column in enumerate(boardGrid):
        if "" in column:
            possibleChoices.append(colIdx)

    return choice(possibleChoices)

def runNGames(moveChooserA, moveChooserB, numGames):
    testData = { "A": [], "B": [], "Draw": [], "totalMoves": 0}
    
    boardWHList = []
    for W in range(6,11):
        for H in range(6, 11):
            boardWHList.append((W,H))
    
    gameNum = 1
    for gameNum in range(1, int(numGames/2)):
        print(f"\rGame {gameNum}: A: {len(testData['A'])} wins; B: {len(testData['B'])} wins    ", end="")
        boardWH = boardWHList[gameNum % len(boardWHList)]
        result = fourinarow.runSingleGame(moveChooserA, moveChooserB, boardWH)
        winner = {"R":"A", "Y":"B", "Draw":"Draw"}[result["winner"]]
        testData[winner].append(result)
        testData["totalMoves"] += len(result["moveSequence"])

    for gameNum in range(int(numGames/2), numGames+1):
        print(f"\rGame {gameNum}: A: {len(testData['A'])} wins; B: {len(testData['B'])} wins    ", end="")
        boardWH = boardWHList[gameNum % len(boardWHList)]
        result = fourinarow.runSingleGame(moveChooserB, moveChooserA, boardWH)
        winner = {"R":"B", "Y":"A", "Draw":"Draw"}[result["winner"]]
        testData[winner].append(result)
        testData["totalMoves"] += len(result["moveSequence"])
        
    print(f"\rAfter {numGames} games: A: {len(testData['A'])} wins; B: {len(testData['B'])} wins    ")
    print(f"\rA total of {testData["totalMoves"]} moves were played    ")
    return testData

def printResultSummary(resultData):
    print("="*40)
    print("Final results:")
    print(f"Your chooser won {len(resultData['A'])} game(s).")
    print(f"Random chooser won {len(resultData['B'])} game(s).")
    print(f"With {len(resultData['Draw'])} draw(s).")
    print("="*40)

def runAgainstRandom(myMoveChooser, numGames=1000):
    data = runNGames(myMoveChooser, randomMoveChooser, numGames)
    printResultSummary(data)

def runAgainstOther(myMoveChooser, otherMoveChooser, numGames=1000):
    data = runNGames(myMoveChooser, otherMoveChooser, numGames)
    printResultSummary(data)

import time
from theMobot.theMobot import theMobot
from Moe import moe
from Monty import monty
from Morris.Morris import morris
from human import human
from ai4_player import ai4_playerWrapper
from ai3_player import ai3_playerWrapper
from ai2_player import ai2_playerWrapper
from ai1_player import ai1_playerWrapper

if __name__ == "__main__":

    began = time.time()
    # print(runSingleGame(theMobot,human),(6,7))
    runAgainstOther(ai1_playerWrapper, human,50)
    print(time.time() - began)
    exit()

    boardGrid = [['' for _ in range(7)] for __ in range(7)]
    began = time.time()
    for _ in range(100000):
        morris(boardGrid, "R", True)
    print(time.time()-began)
