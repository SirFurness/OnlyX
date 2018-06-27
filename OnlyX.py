import os

class Board:
    def __init__(self, boardSideLength):
        self.boardSideLength = boardSideLength
        self.usedCoordinates = []
        self.dead = False

    def place(self, column, row):
        coordinate = (column, row)
        if self.dead:
            print("That board is dead")
        elif coordinate in self.usedCoordinates:
            print("That square already has an X")
        else:
            self.usedCoordinates.append(coordinate)
            print("Nice move!")

    def checkIfDead(self):
        if (not self.checkForDeadColumn()) and\
           (not self.checkForDeadRow()) and\
           (not self.checkForDeadDiagonal()):
            return False
        self.dead = True
        return True

    def checkForDeadColumn(self):
        for column in range(self.boardSideLength):
            if self.checkNextRowsForColumn(column):
                return True

    def checkNextRowsForColumn(self, column):
        for row in range(self.boardSideLength):
            if not self.hasX(column, row):
                return False
        return True

    def checkForDeadRow(self):
        for row in range(self.boardSideLength):
            if self.checkNextColumnsForRow(row):
                return True

    def checkNextColumnsForRow(self, row):
        for column in range(self.boardSideLength):
            if not self.hasX(column, row):
                return False
        return True

    def checkForDeadDiagonal(self):
        isLeftDiagDead = True
        isRightDiagDead = True
        for number in range(self.boardSideLength):
            if not self.hasX(number, number):
                isLeftDiagDead = False
            if not self.hasX(self.boardSideLength-number-1, number):
                isRightDiagDead = False
            if (not isLeftDiagDead) and (not isRightDiagDead):
                return False
        return True

    def hasX(self, column, row):
        return (column, row) in self.usedCoordinates

class Game:
    def __init__(self):
        self.playerOneWins = 0
        self.playerTwoWins = 0

        self.getBoardInfo()
        self.turnNumber = 0
        self.deadBoardsAmt = 0

        self.createBoards()

        self.play()

    def getBoardInfo(self):
        self.boardSideLength = self.getBoardSideLength()
        self.totalBoardAmt = self.getTotalBoardAmt()

    def getBoardSideLength(self):
        try:
            boardSideLength = int(input("Choose side length for the board: "))
            if boardSideLength < 1:
                raise Exception()
            return boardSideLength
        except Exception:
            print("Invalid Board Side Length")
            return self.getBoardSideLength()

    def getTotalBoardAmt(self):
        try:
            totalBoardAmt = int(input("Choose number of rounds to play: "))
            if totalBoardAmt < 1:
                raise Exception()
            return totalBoardAmt
        except Exception:
            print("Invalid Round Number")
            return self.getTotalBoardAmt()

    def createBoards(self):
        self.boards = []
        for i in range(self.totalBoardAmt):
            self.boards.append(Board(self.boardSideLength))

    def play(self):
        self.displayBoard()
        while self.deadBoardsAmt < self.totalBoardAmt:
            self.turnNumber += 1
            self.placeSquare(self.getUserSquare())
            self.displayBoard()
            self.checkForDeadBoard()

    def getUserSquare(self):
        if self.turnNumber % 2 == 0:
            print("Player 2")
        else:
            print("Player 1")
        return {'Column': self.getColumnNum(),
                'Row': self.getRowNum()}

    def getBoard(self):
       try:
           boardNum = int(input("Choose Board: "))
           if boardNum < 1:
               raise Exception()
           boardIndex = boardNum - 1
           return self.boards[boardIndex]
       except Exception:
           print("Invalid Board Number")
           return self.getBoard()

    def getColumnNum(self):
        try:
            columnNum = int(input("Choose Column: "))
            if columnNum > self.boardSideLength or columnNum < 1:
                raise Exception("")
            return columnNum-1
        except Exception:
            print("Invalid Column Number")
            return self.getColumnNum()

    def getRowNum(self):
        try:
            rowNum = int(input("Choose Row: "))
            if rowNum > self.boardSideLength or rowNum < 1:
                raise Exception("")
            return rowNum-1
        except Exception:
            print("Invalid Row Number")
            return self.getRowNum()

    def placeSquare(self, square):
        self.boards[self.deadBoardsAmt].place(square["Column"], square["Row"])

    def checkForDeadBoard(self):
        if self.boards[self.deadBoardsAmt].checkIfDead():
            self.deadBoardsAmt += 1
            self.turnNumber = 0
            self.congratulateRoundWinner()

    def congratulateRoundWinner(self):
        if self.turnNumber % 2 == 0:
            print("Player 1 won that round!")
            self.playerOneWins += 1
        else:
            print("Player 2 won that round!")
            self.playerTwoWins += 1

        if self.deadBoardsAmt == self.totalBoardAmt:
            self.congratulateWinner()
        else:
            input("Enter anything to continue... ")

    def congratulateWinner(self):
        if self.playerTwoWins > self.playerOneWins:
            print("Player 2 won by " + str(self.playerTwoWins-self.playerOneWins) + " round(s)!")
        else:
            print("Player 1 won by " + str(self.playerOneWins-self.playerTwoWins) + " round(s)!")

    def displayBoard(self):
        separator = "+---"
        separatorEnd = "+"
        side = "|"

        board = self.boards[self.deadBoardsAmt]

        os.system('cls' if os.name == 'nt' else 'clear')

        for row in range(board.boardSideLength):
            self.displaySeparator(separator, separatorEnd)
            for column in range(board.boardSideLength):
                self.displayRow(side, column, row)
            print("")
        self.displaySeparator(separator, separatorEnd)

    def displaySeparator(self, separator, separatorEnd):
        board = self.boards[self.deadBoardsAmt]

        for column in range(board.boardSideLength):
            print(separator, end='')
            if column == board.boardSideLength-1:
                print(separatorEnd, end='')
        print("")

    def displayRow(self, side, column, row):
        board = self.boards[self.deadBoardsAmt]

        print(side, end='')
        if board.hasX(column, row):
            print(' X ', end='')
        else:
            print('   ', end='')

        if column == board.boardSideLength-1:
            print(side, end='')


if __name__ == '__main__':
    while True:
        Game()

        shouldReplay = input("Play Again? Y or N\n")
        if shouldReplay == "N":
            break
