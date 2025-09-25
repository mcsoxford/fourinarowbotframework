# Isaac's bots

Isaac's bots were created before this competition ran. This meant Moses had to make wrappers for them to make them compatible with Mr. King's API. These wrappers are ai1\_player.py, ai2\_player.py etc. The actual code written by Isaac is in connect4.py.

The following descriptions are written by Isaac and taken from comments in the code. Bots are ordered from weakest to strongest.

## ai1_player
my own algorithm with summed values (based on depth of win/loss) for scoring

## ai2_player
minimax: 1 for win, -1 for loss, 0 for else

## ai3_player
minimax + alpha-beta pruning: 1 for win, -1 for loss, 0 for else

## ai4_player
minimax + alpha-beta pruning: scoring based on board or win/loss
win = +∞, loss = -∞, smaller values for other draws
