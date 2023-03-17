#this script will be an AI to play Connect4
#it will generate possible moves, score them, and choose the highest score

import copy
import random
from Connect4 import Connect4
import functools

class AI:
    MOVES_AHEAD = 7
    LOG_SCORES = False

    WIN_SCORE = 1000
    LOSE_SCORE = -5000
    TIE_SCORE = 0
    OPEN_TWO_SCORE = 10
    DOUBLE_OPEN_TWO_SCORE = 50
    OPEN_THREE_SCORE = 250
    DOUBLE_OPEN_THREE_SCORE = 750
    ENEMY_SCORE_MULTIPLIER = -0.9
    OPEN_CELL_UNDER_SCORE = -30

    def __init__(self, game, player):
        self.game = game
        self.player = player

        if self.player == 1:
            self.enemy = 2
        else:
            self.enemy = 1

        self.scores = {}
    
    def turn(self):
        if not self.game.complete:
            score, move = self.branch(self.game, 0)
            if move == -1:
                move = self.game.validMoves[random.randrange(0, len(self.game.validMoves), 1)]
            print(f"Player {self.player} moving {move}, score {score}")
            self.game.move(move)

    def branch(self, game, level):
        #here, make each possible move and calculate a score for that board
        if game.player == self.player:
            max = -10000
        else:
            max = 10000
        
        column = -1
        if level < AI.MOVES_AHEAD:
            for i in self.game.validMoves:
                thisGame = Connect4()
                #thisGame.loadGameState(game.board, game.moveCount, game.player, game.lastChangedRow, game.lastChangedColumn, game.moveList)
                thisGame.loadGameState(game.board, game.moveCount, game.player, game.lastChangedRow, game.lastChangedColumn, game.boardString)
                thisGame.move(i)

                score = self.calculateScore(thisGame)
                #score = 0
                #if AI.LOG_SCORES:
                #    with open('Logs\ScoreLogging.txt', 'a') as f:
                #        f.write(f'\nLevel: {level}, Branch: {i}')
                #        f.write(f'\n{thisGame}')
                #        f.write(f'\n{score}')

                if thisGame.winner is None:
                    branchScore, tempColumn = self.branch(thisGame, level + 1)
                    #if level == 0:
                    #    print((f'Level: {level}, Branch: {i}, Score: {score}, Branch Score: {branchScore}, Final Score: {score + branchScore}'))
                    score += branchScore
                else:
                    max = score
                    column = i
                    #since we already moved, this will be switched
                    if self.player == thisGame.player:
                        #enemy, we know if they win, they will pick this, so we can stop here
                        if thisGame.winner == self.enemy:
                            break
                    else:
                        #us, we know if we win, we will pick this, so we can stop
                        if thisGame.winner == self.player:
                            break
                
                #if level == 0:
                #    print((f'Level: {level}, Branch: {i}, Score: {score}'))

                if game.player == self.player:
                    if score > max:
                        max = score
                        column = i
                else:
                    #assume enemy will make the wors move for you
                    if score < max:
                        max = score
                        #column = 1
                        column = i
                
        else:
            max = 0

        return max, column

    def calculateScore(self, game):
        #here, calculate a score for the passed board
        #score system:
        #bs = game.getBoardString()
        bs = game.boardString
        if bs in self.scores:
            score = self.scores[bs]
        else:
            if game.complete:
                if game.winner == self.player:
                    score = AI.WIN_SCORE
                elif game.winner == self.enemy:
                    score = AI.LOSE_SCORE
                else:
                    score = 0
            else:
                #here go through the board
                score = 0
                enemyScore = 0

                #first check rows
                streak = 0
                enemyStreak = 0
                for r in range(len(game.board) - 1, -1, -1):
                    for c in range(0, len(game.board[r])):
                        value = game.board[r][c]
                        if value == self.player:
                            streak += 1
                            enemyStreak = 0
                        elif value == self.enemy:
                            enemyStreak += 1
                            streak = 0
                        else:
                            if streak > 1:
                                score += self.checkOpenStreaks(game, streak, 'Row', r, c)
                            if enemyStreak > 1:
                                enemyScore += self.checkOpenStreaks(game, enemyStreak, 'Row', r, c)

                            #clear streak, leave them if it's the last item
                            if c != len(game.board[r]) - 1:
                                streak = 0
                                enemyStreak = 0
                    if streak > 1:
                        score += self.checkOpenStreaks(game, streak, 'Row', r, c)
                    if enemyStreak > 1:
                        enemyScore += self.checkOpenStreaks(game, enemyStreak, 'Row', r, c)

                #then check columns
                for c in range(0, len(game.board[0])):
                    streak = 0
                    enemyStreak = 0
                    for r in range(len(game.board) - 1, -1, -1):
                        value = game.board[r][c]
                        if value == self.player:
                            streak += 1
                            enemyStreak = 0
                        elif value == self.enemy:
                            enemyStreak += 1
                            streak = 0
                        else:
                            #now check streaks
                            if streak > 1:
                                score += self.checkOpenStreaks(game, streak, 'Column', r, c)
                            if enemyStreak > 1:
                                enemyScore += self.checkOpenStreaks(game, enemyStreak, 'Column', r, c)

                            #exit, because nothing can be above a 0
                            break

                #lastly check diagonals
                for i in game.diagonals:
                    streak = 0
                    enemyStreak = 0
                    row = i[0]
                    column = i[1]
                    for x in range(0, i[2]):
                        value = game.board[row][column]
                        if  value == self.player:
                            streak += 1
                            enemyStreak = 0
                        elif value == self.enemy:
                            enemyStreak += 1
                            streak = 0
                        else:
                            if streak > 1:
                                score += self.checkOpenStreaks(game, streak, 'Diagonal', row, column, diagonal = i)
                            if enemyStreak > 1:
                                enemyScore += self.checkOpenStreaks(game, enemyStreak, 'Diagonal', row, column, diagonal = i)

                            if x != i[2] - 1:
                                streak = 0
                                enemyStreak = 0
                        #now iterate
                        column += 1
                        row += i[3]

                    if streak > 1:
                        score += self.checkOpenStreaks(game, streak, 'Diagonal', row, column, diagonal = i)
                    if enemyStreak > 1:
                        enemyScore += self.checkOpenStreaks(game, enemyStreak, 'Diagonal', row, column, diagonal = i)

                score += enemyScore * AI.ENEMY_SCORE_MULTIPLIER
                self.scores[bs] = score
        return score

    def checkOpenStreaks(self, game, streak, type, row, column, diagonal=None):
        open = 0

        if type == 'Row':
            startColumn = max(column - streak, 0)
            endColumn = min(column, 6)
            startRow = row
            endRow = row
        elif type == 'Column':
            #start doesn't matter for columns
            startRow = row
            endRow = max(0, row - streak)
            startColumn = column
            endColumn = column
        else:
            #diagonal
            startColumn = max(0, column - streak)
            startRow = min(5, row - streak * diagonal[3])
            endColumn = min(column, 6)
            endRow = min(5, row)

        startValue = game.board[startRow][startColumn]
        endValue = game.board[endRow][endColumn]
        openCellsUnder = self.getOpenCellsUnder(game, startRow, startColumn) + self.getOpenCellsUnder(game, endRow, endColumn)

        score = 0
        if streak == 3:
            if startValue == 0 and endValue == 0:
                score = AI.DOUBLE_OPEN_THREE_SCORE
            elif startValue == 0 or endValue == 0:
                score = AI.OPEN_THREE_SCORE
        else:
            if startValue == 0 and endValue == 0:
                score = AI.DOUBLE_OPEN_TWO_SCORE
            elif startValue == 0 or endValue == 0:
                score = AI.OPEN_TWO_SCORE

        return score - openCellsUnder * AI.OPEN_CELL_UNDER_SCORE

    def getOpenCellsUnder(self, game, row, column):
        cells = 0
        for i in range(row + 1, Connect4.ROW_COUNT):
            if game.board[i][column] == 0:
                cells += 1
            else:
                break
        return cells
