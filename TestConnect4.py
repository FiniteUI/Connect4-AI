from Connect4 import Connect4

GAME = Connect4()
print(GAME)
while(not GAME.complete):

    ready = False
    while not ready:
        move = input(f"Player {GAME.player}, make your move:")
        if int(move) not in GAME.validMoves:
            print("Invalid move.")
        else:
            ready = True

    GAME.move(int(move))
    print(GAME)

print("Game Complete")
print(f"Winner: {GAME.winner}")
