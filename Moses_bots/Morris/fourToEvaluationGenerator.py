import json

WINNING_CONSTANT = -1
INFINITY_CONSTANT = -2
ERROR_CONSTANT = -3

def evaluateFour(four):
    ourTokens = four.count(1)
    opponentTokens = four.count(2)

    if ourTokens != 0 and opponentTokens != 0:
        return 0

    match (ourTokens,opponentTokens):
        case (3,0):
            return WINNING_CONSTANT
        case (2,0):
            return 100
        case (1,0):
            return 10
        case (0,0):
            return 1
        case (0,1):
            return 3
        case (0,2):
            return 30
        case (0,3):
            return INFINITY_CONSTANT
        case _:
            return ERROR_CONSTANT

hashMap = [-3]*3**4

for firstToken in range(3):
    for secondToken in range(3):
        for thirdToken in range(3):
            for fourthToken in range(3):
                hashMap[firstToken*3**3 + secondToken*3**2 + thirdToken*3 + fourthToken] = evaluateFour([firstToken,secondToken,thirdToken,fourthToken])

with open("fourToEvaluation.json", "w") as file:
    json.dump(hashMap,file)