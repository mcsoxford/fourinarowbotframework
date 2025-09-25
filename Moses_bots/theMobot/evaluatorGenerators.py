import json

INFINITY_CONSTANT = -1
ERROR_CONSTANT = -2

def evaluateFour(ourTokens,opponentTokens):
    if ourTokens != 0 and opponentTokens != 0:
        return 0

    match (ourTokens, opponentTokens):
        case (3, 0):
            return INFINITY_CONSTANT
        case (2, 0):
            return 9
        case (1, 0):
            return 4
        case (0, 0):
            return 1
        case (0, 1):
            return 1
        case (0, 2):
            return 4
        case (0, 3):
            return 9
        case _:
            return ERROR_CONSTANT

def evaluateOurFour(four):
    return evaluateFour(four.count(1),four.count(2))

def evaluateOpponentFour(four):
    return evaluateFour(four.count(2),four.count(1))

ourEvaluation = [-2]*3**4
opponentEvaluation = [-2]*3**4

for firstToken in range(3):
    for secondToken in range(3):
        for thirdToken in range(3):
            for fourthToken in range(3):
                hash = firstToken*3**3 + secondToken*3**2 + thirdToken*3 + fourthToken
                ourEvaluation[hash] = evaluateOurFour([firstToken,secondToken,thirdToken,fourthToken])
                opponentEvaluation[hash] = evaluateOpponentFour([firstToken,secondToken,thirdToken,fourthToken])

with open("fourToOurNewEvaluation.json", "w") as file:
    json.dump(ourEvaluation,file)

with open("fourToOpponentNewEvaluation.json","w") as file:
    json.dump(opponentEvaluation,file)