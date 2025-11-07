"""
Ashley Foster
Project 2:

Tic-Tac-Toe

This program is a simple Tic-Tac-Toe game using classes and objects.  
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

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

    def comp_move(self):
        tictac = pd.read_csv('tictac_single.txt', sep = ' ', header = None)
        #using the optimized parameters from Lab Week 10C
        x_train, x_test, y_train, y_test = train_test_split(tictac.iloc[:, :-1], tictac.iloc[:, -1], test_size=0.2, random_state=29, shuffle=True)
        knn = KNeighborsClassifier(n_neighbors = 9)
        knn.fit(x_train,y_train)
        mapped = {'X' : 1, 'O': -1, ' ' : 0}
        flat_board = []
        for row in range(len(self.board.c)):
            for col in range(len(self.board.c[row])):
                flat_board.append(mapped.get(self.board.c[row][col],0))
        predict = knn.predict([flat_board])[0] #predicting best move for computer
        row,col = divmod(int(predict), 3) #converting y index value to row, col 
        return row, col
        
    # this method runs the tic-tac-toe game
     # hint: you can call a class method using self.method_name() within another class method
    def playGame(self):
        board = Board()
        self.board.printBoard()
        print("New Game: X goes first.")
        print()

        while True:
            if self.turn == 'X': #Player move = 'X'
                print(f"\n{self.turn}'s turn.")
                print(f"Where do you want your {self.turn} placed?")
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
            else: #Computer move = 'O'
                row, col = self.comp_move() #determining best move for computer
                self.board.c[row][col] = self.turn
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