from connect4 import ai2_player

def ai2_playerWrapper(newBoard,colour,newGame):

    global width
    global height
    global board
    global towerheights

    if newGame:
        height = len(newBoard[0])
        width = len(newBoard)

        board = [[0] * width for _ in range(height)]
        towerheights = [height - 1] * width

    for i in range(width):

        if towerheights[i] < 0:
            continue

        if newBoard[i][height - 1 - towerheights[i]] != "":
            board[towerheights[i]][i] = -1
            towerheights[i] -= 1
            break

    x = ai2_player(board, towerheights, height, width, 1)
    board[towerheights[x]][x] = 1
    towerheights[x] -= 1

    return x