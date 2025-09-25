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
