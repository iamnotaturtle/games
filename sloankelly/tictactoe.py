#!/usr/bin/python3

board = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
currentToken = 'X' 
winningToken = ''
slotsFilled = 0

print('Tic Tac Toe')
print('Match 3 lines vertically, horizontally or diagonally')
print('X goes first')

def printBoard(board):
    print("\n")
    print("%s|%s|%s" % (board[0], board[1], board[2])) 
    print("-+-+-")
    print("%s|%s|%s" % (board[3], board[4], board[5])) 
    print("-+-+-")
    print("%s|%s|%s" % (board[6], board[7], board[8]))

def isWon(board, currentToken):
    row1 = board[0] == currentToken and board[1] == currentToken and board[2] == currentToken 
    row2 = board[3] == currentToken and board[4] == currentToken and board[5] == currentToken 
    row3 = board[6] == currentToken and board[7] == currentToken and board[8] == currentToken

    col1 = board[0] == currentToken and board[3] == currentToken and board[6] == currentToken
    col2 = board[1] == currentToken and board[4] == currentToken and board[7] == currentToken
    col3 = board[2] == currentToken and board[5] == currentToken and board[8] == currentToken

    diag1 = board[0] == currentToken and board[4] == currentToken and board[8] == currentToken
    diag2 = board[2] == currentToken and board[4] == currentToken and board[6] == currentToken

    row = row1 or row2 or row3 
    col = col1 or col2 or col3 
    diag = diag1 or diag2

    return row or col or diag

def handleTurn(slotsFilled, currentToken):
    pos = -1
    while pos == -1:
        pos = int(input(f"{currentToken}'s turn. Where to? "))
        if pos < 1 or pos > 9 or board[pos - 1] != str(pos):
            pos = -1
            print('Invalid postition. 1 - 9 only.')
        
        board[pos - 1] = currentToken
        slotsFilled += 1

while not winningToken and slotsFilled < 9:
    printBoard(board)

    handleTurn(slotsFilled, currentToken)

    if isWon(board, currentToken):
        winningToken = currentToken
        print("Congratulations %s! You won!!" % currentToken)

    currentToken = 'O' if currentToken == 'X' else 'X'
