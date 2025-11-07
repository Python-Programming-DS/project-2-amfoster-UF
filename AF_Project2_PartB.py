"""
Ashley Foster
Project 2:

Tic-Tac-Toe

This program is a simple Tic-Tac-Toe game using classes and objects.
    
    
"""
# define Board class to building the Game Board:
class Board:
     # this constructor initiates the board with empty cells
    def __init__(self):
        self.c = [[" "," "," "],
                  [" "," "," "],
                  [" "," "," "]]
      
    # this method prints the board. Recall that class methods are functions
    def printBoard(self):
        # it first prints the BOARD_HEADER constant
        # BOARD_HEADER constant
        BOARD_HEADER = "-----------------\n|R\\C| 0 | 1 | 2 |\n-----------------"
        print(BOARD_HEADER)

        # using a for-loop, it increments through the rows
        for i in range(3):
            print(self.c[i])
            print("-----------------")

# define Game class to implement the Game Logic:
class Game:
    # the constructor
    def __init__(self):
        self.board = Board()
        self.turn = 'X' #X always goes first

    # this method switches players 
    def switchPlayer(self):
        if self.turn == "X":
            self.turn = "O"
        else:
            self.turn = "X"
    
    # this method validates the user's entry
    def validateEntry(self, row, col,board):
        if int(row) >= 3 or int(col) >= 3:
            print("Invalid entry: try again.\nRow & column numbers must be either 0, 1, or 2.")
            return False
        if board.c[row][col] == 'O' or board.c[row][col] == 'X':
            print(f"That cell is already taken.\nPlease make another selection.")
            return False 
        return True

    # this method checks if the board is full
    def checkFull(self):
        for row in self.board.c:
            for col in row:
                if col == ' ':
                    return False
        return True

    # this method checks for a winner
    def checkWin(self):
        win_condition = [[self.board.c[0][0], self.board.c[0][1], self.board.c[0][2]],
                     [self.board.c[1][0], self.board.c[1][1], self.board.c[1][2]],
                     [self.board.c[2][0], self.board.c[2][1], self.board.c[2][2]],
                     [self.board.c[0][0], self.board.c[1][0], self.board.c[2][0]],
                     [self.board.c[0][1], self.board.c[1][1], self.board.c[2][1]],
                     [self.board.c[0][2], self.board.c[1][2], self.board.c[2][2]],
                     [self.board.c[0][0], self.board.c[1][1], self.board.c[2][2]],
                     [self.board.c[0][2], self.board.c[1][1], self.board.c[2][0]]]
        win = [self.turn,self.turn,self.turn]
        for condition in win_condition:
            if condition == win:
                return True
        return False

    # this method checks if the game has met an end condition by calling checkFull() and checkWin()
    # hint: you can call a class method using self.method_name() within another class method, e.g., self.checkFull()
    def checkEnd(self): 
        if self.checkWin():
            print(f"{self.turn} IS THE WINNER!!!")
            self.board.printBoard()
            return True
        #If the board is filled, and no win condition has triggered:
        if self.checkFull():
            print(f"DRAW! NOBODY WINS!")
            self.board.printBoard()
            return True

    #function to get available positions on the board  
    def avail_moves(self):
        avail = []
        for i in range(len(self.board.c)):
            for j in range(len(self.board.c[i])):
                if self.board.c[i][j] == ' ':
                    avail.append((i,j))
        return avail      

    #Minimax algorithm
    def minimax(self,player):
        if player == 'X':
            if self.checkWin():
                return 1, None
            if self.checkFull():
                return 0, None
        else:
            if self.checkWin():
                return -1, None
            if self.checkFull():
                return 0, None

        avail = self.avail_moves()
        if self.turn == 'X': #X's turn
            self.best_score, self.best_move = -float('inf'), None
            for i,j in avail:
                    self.board.c[i][j] = 'X'
                    score, move = self.minimax('O')
                    self.board.c[i][j] = ' '
                    if score > self.best_score:
                        self.best_score, self.best_move = score, (i,j)
            return self.best_score, self.best_move
        else: #O's turn
            self.best_score,self.best_move = float('inf'), None
            for i,j in avail:
                    self.board.c[i][j] = 'O'
                    score,move = self.minimax('X')
                    self.board.c[i][j] = ' '
                    if score < self.best_score:
                        self.best_score, self.best_move = score, (i,j)
            return self.best_score, self.best_move

    # this method runs the tic-tac-toe game
     # hint: you can call a class method using self.method_name() within another class method
    def playGame(self):
        board = Board()
        self.board.printBoard()
        if self.turn == 'X':
            print("New Game: X goes first.")
        else: 
            print("New Game: O goes first.")
        print()

        while True:
            print(f"\n{self.turn}'s turn.")
            print(f"Where do you want your {self.turn} placed?")
            #Insert minimax algorithm prompt here. Shows best move.
            self.minimax(self.turn)
            print(f"The best move is: {self.best_move}")
            print("Please enter row number and column number separated by a comma.")
        
            #Check if the entry is valid
            try:
                row, col = map(int, input().split(','))
            except ValueError:
                print("Invalid input. Please enter numbers separated by a comma.")
                continue
            print(f"You have entered row #{row} \n\t  and column #{col}")

            if self.validateEntry(row,col,self.board):
                print("Thank you for your selection.")
                self.board.c[row][col] = self.turn
                #Check for a win condition or if the board is full
                if self.checkEnd():
                    break 
                self.board.printBoard()
                #switch player turns
                self.switchPlayer()

# main function
def main():
    # first initializes a variable to repeat the game
    again = 'y'

    # using while-loop that runs until the user says no for another game
    while again.lower() == 'y':
        game = Game()
        game.playGame()
        again = input("Another game? Enter Y or y for yes. ")
    # goodbye message 
    print("Thank you for playing!")
    
# call to main() function
if __name__ == "__main__":
    main()
