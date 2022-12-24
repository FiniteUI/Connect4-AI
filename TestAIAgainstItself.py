from Connect4 import Connect4
from AI import AI

GAME = Connect4()
ai_1 = AI(GAME, 1)
ai_2 = AI(GAME, 2)
print(GAME)
while(not GAME.complete):
    if GAME.player == 1:
        ai_1.turn()
    else:
        ai_2.turn()
    
    print(GAME)

print("Game Complete")
print(f"Winner: {GAME.winner}")
