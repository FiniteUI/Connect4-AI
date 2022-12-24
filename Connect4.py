#this will be a stripped down more streamlined version of my connect4 engine
#this one will be focused on simply playing the game
#NOT on generating extra data

class Connect4:
    
    ROW_COUNT = 6
    COLUMN_COUNT = 7
    WIN_AMOUNT = 4

    def __init__(self):
        #here define the board for play
        self.player = 1
        self.complete = False
        self.winner = None
        self.validMoves = [0, 1, 2, 3, 4, 5, 6]
        
        self.board = (
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        )

        self.boardString = '000000000000000000000000000000000000000000'
        
        #other state variables
        self.lastChangedRow = None
        self.lastChangedColumn = None
        self.moveCount = 0

        #define diagonals used for checking
        #just starting coordinates: row, column, length, direction
        self.diagonals = (
            #down diagonals
            (2, 0, 4, 1),
            (1, 0, 5, 1),
            (0, 0, 6, 1),
            (0, 1, 6, 1),
            (0, 2, 5, 1),
            (0, 3, 4, 1),

            #up diagonals
            (3, 0, 4, -1),
            (4, 0, 5, -1),
            (5, 0, 6, -1),
            (5, 1, 6, -1),
            (5, 2, 5, -1),
            (5, 3, 4, -1),
        )

    def move(self, column):
        #here, take a move from the player and make it
        if not self.complete:
            if column in self.validMoves:
                for i in range(self.ROW_COUNT - 1, -1, -1):
                    if self.board[i][column] == 0:
                        self.board[i][column] = self.player

                        #check if column is full, update valid move list
                        if i == 0:
                            self.validMoves.remove(column)

                        self.lastChangedColumn = column
                        self.lastChangedRow = i
                        self.moveCount += 1

                        #update board string
                        self.boardString = f'{self.boardString[:i * 7 + column]}{self.player}{self.boardString[i * 7 + column +1:]}'
                        break
                
                #move has been made, check win
                self.checkWin()

                #now make necessary state changes
                self.player += 1
                if self.player == 3:
                    self.player = 1

    def checkWin(self):
        #check rows first
        streak = 0
        for i in range(0, len(self.board[self.lastChangedRow])):
            #here we could speed this up by checking if there are enough available items to even win
            if self.board[self.lastChangedRow][i] == self.player:
                streak += 1
            else:
                streak = 0

            #if there aren't enough cells left to win, back out
            #if streak + 2 < i:
            if i > 2 and streak == 0:
                break

            if streak == Connect4.WIN_AMOUNT:
                self.setWin()
                break
        
        #then check columns
        if not self.complete:
            streak = 0
            for i in range(Connect4.ROW_COUNT - 1, -1, -1):
                if self.board[i][self.lastChangedColumn] == 0:
                    break
                else:
                    if self.board[i][self.lastChangedColumn] == self.player:
                        streak += 1
                    else:
                        streak = 0

                #check if there are even enough cells left to win
                #if i + streak < Connect4.WIN_AMOUNT:
                if i < 4 and streak == 0:
                   break
                
                if streak == Connect4.WIN_AMOUNT:
                    self.setWin()
                    break

        #then diagonals
        if not self.complete:
            #for now we will just loop, but if we could store
            #the last changed up and down diagonal, we'd just need to check that
            for i in self.diagonals:
                #here check if we need to check this diagonal base off lastchangedcolumn
                if self.lastChangedColumn < i[1] or self.lastChangedColumn > i[1] + i[2] - 1: 
                    break

                streak = 0
                row = i[0]
                column = i[1]
                for x in range(0, i[2]):
                    if self.board[row][column] == self.player:
                        streak += 1
                    else:
                        streak = 0

                    #if there are not enough cells left to win, break
                    if  x >= i[2] - Connect4.WIN_AMOUNT and streak == 0:
                        break
                    
                    if streak == Connect4.WIN_AMOUNT:
                        self.setWin()
                        break
                    
                    #now iterate
                    column += 1
                    row += i[3]
                
                if self.complete:
                    break

        #finally check if game is over
        if not self.complete:
            if self.moveCount == 42:
                self.complete = True

    def setWin(self):
        self.complete = True
        self.winner = self.player

    def loadGameState(self, board, moves, player, lastRow, lastColumn, boardString):
        #can't do this as it uses the same object
        #self.board = board

        self.board = [[x for x in y] for y in board]

        self.moveCount = moves
        self.player = player
        self.lastChangedColumn = lastColumn
        self.lastChangedRow = lastRow
        self.boardString = boardString

    def __str__(self):
        boardString = ''
        for i in range(0, len(self.board)):
            boardString = boardString + f'\n{self.board[i]}'
        boardString = boardString.replace('0', ' ')
        boardString = boardString + '\n---------------------\n 0, 1, 2, 3, 4, 5, 6'
        return boardString