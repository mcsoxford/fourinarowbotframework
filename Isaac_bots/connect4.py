from random import shuffle
from itertools import permutations

def display(board, height, width):

    chars = {1:"●", -1:"●"}
    lines = ("+", "-", "|")

    red = "\033[38;5;196m"
    yellow = "\033[38;5;226m" 
    end = "\033[0;0;0m"

    icons = {1:red + chars[1] + end, -1:yellow + chars[-1] + end, 0:" "}
    lastline = "|" + "|".join([str(x) for x in range(0, width)]) + "|"
    for y in range(2*height+1):
        string = ""
        for x in range(2*width+1):
            value = 2*(y%2) + (x%2)
            if value == 3:
                string += icons[board[y//2][x//2]]
            else:
                string += lines[value]
        print(string)
    print(lastline)

def check_win(board, height, width, towerheights, prevx):
    winnum = 4

    prevy = towerheights[prevx]
    player = board[prevy][prevx]
    
    # x shifts
    total = 1
    x = prevx
    while x < width-1 and board[prevy][x+1] == player:
        total += 1
        x += 1
    x = prevx
    while x > 0 and board[prevy][x-1] == player:
        total += 1
        x -= 1
    if total >= winnum:
        return True

    # x-y same sign shifts
    total = 1
    x = prevx
    y = prevy
    while x < width-1 and y < height-1 and board[y+1][x+1] == player:
        total += 1
        x += 1
        y += 1
    x = prevx
    y = prevy
    while x > 0 and y > 0 and board[y-1][x-1] == player:
        total += 1
        x -= 1
        y -= 1
    if total >= winnum:
        return True

    # x-y opposite sign shifts
    total = 1
    x = prevx
    y = prevy
    while x < width-1 and y > 0 and board[y-1][x+1] == player:
        total += 1
        x += 1
        y -= 1
    x = prevx
    y = prevy
    while x > 0 and y < height-1 and board[y+1][x-1] == player:
        total += 1
        x -= 1
        y += 1
    if total >= winnum:
        return True

    # y shifts (only down)
    total = 1
    y = prevy
    while y < height-1 and board[y+1][prevx] == player:
        total += 1
        y += 1
    if total >= winnum:
        return True

    return False

def ai1_recursion(board, towerheights, height, width, player0, player, depth):
    if depth == 0:
        return 0
    total = 0
    for x in range(width):
        if towerheights[x] >= 0:
            board[towerheights[x]][x] = player
            if check_win(board, height, width, towerheights, x):
                if player == player0:
                    v = 0
                else:
                    v = -1
                board[towerheights[x]][x] = 0
                return v * (width**depth)
            towerheights[x] -= 1
            total += ai1_recursion(board, towerheights, height, width, player0, -player, depth-1) 
            towerheights[x] += 1
            board[towerheights[x]][x] = 0 
    return total

def ai1_player(board, towerheights, height, width, player):
    # my own algorithm with summed values (based on depth of win/loss) for scoring
    depth = 8

    bestx = 0
    bestvalue = -(7**depth)
    for x in range(width):
        if towerheights[x] >= 0:
            board[towerheights[x]][x] = player
            if check_win(board, height, width, towerheights, x):
                return x
            towerheights[x] -= 1
            value = ai1_recursion(board, towerheights, height, width, player, -player, depth-1)
            towerheights[x] += 1
            board[towerheights[x]][x] = 0
            if value > bestvalue:
                bestx = x
                bestvalue = value
    return bestx

def ai2_recursion(board, towerheights, height, width, depth, player, player0, prevx):
    if prevx != width:
        towerheights[prevx] += 1
        if check_win(board, height, width, towerheights, prevx):
            towerheights[prevx] -= 1
            return -(player*player0)
        towerheights[prevx] -= 1
    if depth == 0:
        return 0
    if player == player0:
        bvalue = -2
        for x in range(width):
            if towerheights[x] >= 0:
                board[towerheights[x]][x] = player
                towerheights[x] -= 1
                value = ai2_recursion(board, towerheights, height, width, depth-1, -player, player0, x)
                towerheights[x] += 1
                board[towerheights[x]][x] = 0
                bvalue = max(bvalue, value)
    else:
        bvalue = 2
        for x in range(width):
            if towerheights[x] >= 0:
                board[towerheights[x]][x] = player
                towerheights[x] -= 1
                value = ai2_recursion(board, towerheights, height, width, depth-1, -player, player0, x)
                towerheights[x] += 1
                board[towerheights[x]][x] = 0
                bvalue = min(bvalue, value)
    if bvalue == -2 or bvalue == 2:
        return 0
    return bvalue

def ai2_player(board, towerheights, height, width, player):
    # minimax: 1 for win, -1 for loss, 0 for else
    depth = 8

    bvalue = -2
    bx = 0
    for x in range(width):
        if towerheights[x] >= 0:
            board[towerheights[x]][x] = player
            towerheights[x] -= 1
            value = ai2_recursion(board, towerheights, height, width, depth-1, -player, player, x)
            towerheights[x] += 1
            board[towerheights[x]][x] = 0
            if value == 1:
                return x
            if value > bvalue:
                bx = x
                bvalue = value
    return bx

def ai3_recursion(board, towerheights, height, width, depth, player, player0, prevx, alpha, beta):
    towerheights[prevx] += 1
    if check_win(board, height, width, towerheights, prevx):
        towerheights[prevx] -= 1
        return -(player*player0)
    towerheights[prevx] -= 1
    if depth == 0:
        return 0
    if player == player0:
        bvalue = -2
        for x in range(width):
            if towerheights[x] >= 0:
                board[towerheights[x]][x] = player
                towerheights[x] -= 1
                value = ai3_recursion(board, towerheights, height, width, depth-1, -player, player0, x, alpha, beta)
                towerheights[x] += 1
                board[towerheights[x]][x] = 0
                bvalue = max(bvalue, value)
                alpha = max(alpha, bvalue)
                if bvalue >= beta:
                    break
    else:
        bvalue = 2
        for x in range(width):
            if towerheights[x] >= 0:
                board[towerheights[x]][x] = player
                towerheights[x] -= 1
                value = ai3_recursion(board, towerheights, height, width, depth-1, -player, player0, x, alpha, beta)
                towerheights[x] += 1
                board[towerheights[x]][x] = 0
                bvalue = min(bvalue, value)
                beta = min(beta, bvalue)
                if bvalue <= alpha:
                    break
    if bvalue == -2 or bvalue == 2:
        return 0
    return bvalue

def ai3_player(board, towerheights, height, width, player):
    # minimax + alpha-beta pruning: 1 for win, -1 for loss, 0 for else
    depth = 11

    bvalue = -2
    bx = 0
    for x in (3, 2, 4, 1, 5, 0, 6):
        if towerheights[x] >= 0:
            board[towerheights[x]][x] = player
            towerheights[x] -= 1
            value = ai3_recursion(board, towerheights, height, width, depth-1, -player, player, x, -2, 2)
            towerheights[x] += 1
            board[towerheights[x]][x] = 0
            if value == 1:
                return x
            if value > bvalue:
                bx = x
                bvalue = value
    return bx

def func(x):
    return x**2

def scorefinalboard(board, height, width, player):
    total_score = 0

    for opp in (1, -1):
        score = 0
        # horizontal
        for y in range(height):
            for x in range(width-3):
                win_possible = True
                total = 0
                for delta in range(4):
                    if board[y][x+delta] == opp*player:
                        total += 1
                    elif board[y][x+delta] == -opp*player:
                        win_possible = False
                        break
                if win_possible:
                    score += func(total)
        # vertical
        for x in range(width):
            for y in range(height-3):
                win_possible = True
                total = 0
                for delta in range(4):
                    if board[y+delta][x] == opp*player:
                        total += 1
                    elif board[y+delta][x] == -opp*player:
                        win_possible = False
                        break
                if win_possible:
                    score += func(total)
        # diagonal /
        for y in range(height-3):
            for x in range(width-3):
                win_possible = True
                total = 0
                for delta in range(4):
                    if board[y+delta][x+delta] == opp*player:
                        total += 1
                    elif board[y+delta][x+delta] == -opp*player:
                        win_possible = False
                        break
                if win_possible:
                    score += func(total)
        # diagonal \
        for y in range(3, height):
            for x in range(width-3):
                win_possible = True
                total = 0
                for delta in range(4):
                    if board[y-delta][x+delta] == opp*player:
                        total += 1
                    elif board[y-delta][x+delta] == -opp*player:
                        win_possible = False
                        break
                if win_possible:
                    score += func(total)

        total_score += score*opp
    return total_score

def ai4_recursion(board, towerheights, height, width, depth, player, player0, prevx, alpha, beta):
    towerheights[prevx] += 1
    if check_win(board, height, width, towerheights, prevx):
        towerheights[prevx] -= 1
        return -(player*player0) * (10**6)
    towerheights[prevx] -= 1
    if depth == 0:
        return scorefinalboard(board, height, width, player0)
    if player == player0:
        bvalue = -10**6-1
        for x in range(width):
            if towerheights[x] >= 0:
                board[towerheights[x]][x] = player
                towerheights[x] -= 1
                value = ai4_recursion(board, towerheights, height, width, depth-1, -player, player0, x, alpha, beta)
                towerheights[x] += 1
                board[towerheights[x]][x] = 0
                bvalue = max(bvalue, value)
                alpha = max(alpha, bvalue)
                if bvalue >= beta:
                    break
    else:
        bvalue = 10**6+1
        for x in range(width):
            if towerheights[x] >= 0:
                board[towerheights[x]][x] = player
                towerheights[x] -= 1
                value = ai4_recursion(board, towerheights, height, width, depth-1, -player, player0, x, alpha, beta)
                towerheights[x] += 1
                board[towerheights[x]][x] = 0
                bvalue = min(bvalue, value)
                beta = min(beta, bvalue)
                if bvalue <= alpha:
                    break
    if bvalue == -10**6-1 or bvalue == 10**6+1:
        return 0
    return bvalue

def ai4_player(board, towerheights, height, width, player):

    # minimax + alpha-beta pruning: scoring based on board or win/loss
    # win = +∞, loss = -∞, smaller values for other draws
    depth = 7

    bvalue = -10**6-1
    bx = 0
    for x in range(width):
        if towerheights[x] >= 0:
            board[towerheights[x]][x] = player
            towerheights[x] -= 1
            value = ai4_recursion(board, towerheights, height, width, depth-1, -player, player, x, -10**6-1, 10**6+1)
            towerheights[x] += 1
            board[towerheights[x]][x] = 0
            if value == 10**6:
                return x
            if value > bvalue:
                bx = x
                bvalue = value
    return bx

def real_player(board, towerheights, height, width, player):
    return int(input("Input a column number: "))

def random_player(board, towerheights, height, width, player):
    possible = []
    for index in range(7):
        if towerheights[index] >= 0:
            possible.append(index)
    shuffle(possible)
    return possible[0]

def game(player1, player2):
    height = 6
    width = 7
    players = {1:player1, -1:player2}

    board = [[0]*width for _ in range(height)]
    towerheights = [height-1]*width
    player = 1
    moves = 0
    totalmoves = width*height
    win = False
    display(board, height, width)

    while ((not win) and (moves < totalmoves)):

        x = players[player](board, towerheights, height, width, player)
        
        board[towerheights[x]][x] = player
        win = check_win(board, height, width, towerheights, x)
        towerheights[x] -= 1
        display(board, height, width)
        player = -player
        moves += 1

    if win:
        return -player
    else:
        return 0

def roundrobin():
    players = [ai1_player, ai2_player, ai3_player, ai4_player]
    
    results = []
    for player1, player2 in permutations(players, 2):
        result = game(player1, player2)
        results.append((player1, player2, result))

    for result in results:
        winners = {1:result[0].__name__, -1:result[1].__name__, 0:"draw"}
        print(winners[1] + " vs. " + winners[-1] + " -> " + winners[result[2]])

if __name__ == "__main__":
    game(real_player,ai3_player)