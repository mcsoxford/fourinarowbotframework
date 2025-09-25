Mr. King's repositiory on gitLab has the following files:
fiar_test_runner.py
fourinarow.py

These are mirrored in this repository.

Mr. King's repositiory on gitLab has the following README:

# FourInARowBotFramework

## What is this?

This project is a framework within which you can create a bot to play four-in-a-row (much better known by a trademarked name).

The idea is to clone or fork the repository, write a bot to choose each move, then run the bot against other bots to see which is more effective at winning the game.

## The game rules

In this version of the game, the 'board' can vary in size from 6 to 10 columns and from 6 to 10 rows (both inclusive).

All the main principles are the same as the trademarked-game-that-shall-not-be-named: 
- 2 players (one with red pieces, the other with yellow)
- the current player chooses a column in which to place their piece (red goes first)
- the piece will fall to the bottom-most empty row in that column
- when a player gets four of their pieces in an uninterrupted line horizontally, vertically or diagonally they win!
- if the board fills up with neither player getting a row of four pieces, the game is a draw
- if the game is not finished, the other player now takes a turn

## The Python Files

### fourinarow.py

This file contains the actual game logic.  You will need this file in the same folder as your bot script, but you will not need to refer to it directly.

### fiar_test_runner.py

This is the file you will need to import to run games with your move-chooser bot.

To compare your move-chooser bot against one which randomly chooses an available slot, you would use code like this:
```
import fiar_test_runner

def my4InARowBot(boardGrid, colour):
	# your logic here
	
	return <your choice between 0 and len(boardGrid)-1>

fiar_test_runner.runAgainstRandom(my4InARowBot)
```

## Writing a Bot

To write a bot, you have to write a subroutine which takes two parameters: boardGrid and colour.

```boardGrid``` is a 2D list of board spaces.  It can be different sizes each game but will not change once a game has started.  It has 6-10 columns (inclusive) and 6-10 rows (inclusive)
A space's value is accessed by: 
```boardGrid[columnIndex][rowIndex]```

```rowIndex``` zero is the bottom row of the board.

```colour``` is the colour your bot is currently playing as: 'R' or 'Y'

## Example Bots

One example bot can be found in ```fiar_test_runner.py```:

```
def randomMoveChooser(boardGrid, colour):
    possibleChoices = []
    for colIdx, column in enumerate(boardGrid):
        if "" in column:
            possibleChoices.append(colIdx)
    return choice(possibleChoices)
```

Four example bots which keep state info can be found near the bottom of ```fourinarow.py```:

```
dumChooserInfo = { "R":0, "Y":0 }

def horizontalChooser(boardGrid, colour):
	choice = dumChooserInfo[colour]
	dumChooserInfo[colour] = (choice+1)%len(boardGrid)
	return choice

def verticalChooser(boardGrid, colour):
	choice = dumChooserInfo[colour]
	return choice

def diagonalHLtoLRChooser(boardGrid, colour):
	choice = dumChooserInfo["R"]
	dumChooserInfo["R"] = (choice+1)%len(boardGrid)
	return choice

def diagonalLLtoHRChooser(boardGrid, colour):
	choice = dumChooserInfo["R"]
	newChoice = choice-1
	if newChoice < 0:
		newChoice = len(boardGrid)-1
	dumChooserInfo["R"] = newChoice
	return choice
```



