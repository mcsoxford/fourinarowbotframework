# Moses's (my) bots

# From weakest to strongest

## Moe.py

This bot checks if there is a winning move it can make on this turn. If it can, it makes it. Otherwise it makes a random move.

## Morris

This bot checks each move and decides how good it is, but it only thinks one move ahead. For each move, it sees how many chances it is making for it to win. For example, making a three in a row is better than playing in a four where both players have played (that four can never result in the game being won or lost).

## Monty

Monty runs a Monte Carlo simulation for each move to determine which moves gives it a highest probability of winning. (Many games are played from each position after the move where both players play randomly and if the random player that represents us wins more, the move is better)

## theMobot

Your typical min-max approach, but it does introduce one optimisation which is somewhat interesting. It keeps a rolling evaluation of each position based on the nodes before it. This means it doesn't evaluate the leaves from scratch when it reaches them. (It assumes the opponent will make the best moves and makes its choice based on evaluations of positions far into the future)
