from Connect4 import Connect4
from AI import AI
import time

GAME = Connect4()
ai = AI(GAME, 2)
#AI.MOVES_AHEAD = 5

print(GAME)
while(not GAME.complete):
    ready = False
    while not ready:
        move = input(f"Player {GAME.player}, make your move:")
        if move == 'C':
            ai.calculateScore(GAME)

        elif int(move) not in GAME.validMoves:
            print("Invalid move.")

        else:
            ready = True

    GAME.move(int(move))
    print(GAME)

    #now AI moves
    if not GAME.complete:
        startTime = time.time()
        ai.turn()
        timeTaken = time.time() - startTime
        print(f"Decision made in {timeTaken} seconds")
        print(GAME)

print("Game Complete")
print(f"Winner: {GAME.winner}")
