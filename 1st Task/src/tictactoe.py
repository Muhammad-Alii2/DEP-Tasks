import tkinter as tk
from tkinter import messagebox
import random


# Evaluate the board to find the score
def evaluateScore(board):
    for i in [0, 3, 6]:
        if board[i] != '-' and board[i] == board[i + 1] == board[i + 2]:
            if board[i] == '0':
                return 1
            else:
                return -1

    for i in [0, 1, 2]:
        if board[i] != '-' and board[i] == board[i + 3] == board[i + 6]:
            if board[i] == '0':
                return 1
            else:
                return -1

    if board[0] != '-' and board[0] == board[4] == board[8]:
        if board[0] == '0':
            return 1
        else:
            return -1
    if board[2] != '-' and board[2] == board[4] == board[6]:
        if board[2] == '0':
            return 1
        else:
            return -1

    return 0


# Normal difficulty algorithm
def normalAlgo(board):
    score = evaluateScore(board)

    if score == 1:
        return score

    if score == -1:
        return score

    if '-' not in board:
        return 0

    best_value = float('inf')
    for i in range(9):
        if board[i] == '-':
            board[i] = 'X'
            best_value = min(best_value, evaluateScore(board))
            board[i] = '-'

    return best_value


# Minimax algorithm for hard difficulty
def miniMax(board, is_max):
    score = evaluateScore(board)

    if score == 1:
        return score

    if score == -1:
        return score

    if '-' not in board:
        return 0

    if is_max:
        best_value = -float('inf')
        for i in range(9):
            if board[i] == '-':
                board[i] = '0'
                best_value = max(best_value, miniMax(board, not is_max))
                board[i] = '-'

        return best_value
    else:
        best_value = float('inf')
        for i in range(9):
            if board[i] == '-':
                board[i] = 'X'
                best_value = min(best_value, miniMax(board, not is_max))
                board[i] = '-'

        return best_value


# Find best move for easy difficulty
def findBestMoveEasy(board):
    empty_spots = [pos for pos in range(len(board)) if board[pos] == '-']
    return random.choice(empty_spots)


# Find best move for normal difficulty
def findBestMoveNormal(board):
    best_value = -float('inf')
    best_pos = -1

    for i in range(9):
        if board[i] == '-':
            board[i] = '0'
            move_value = normalAlgo(board)
            board[i] = '-'
            if move_value > best_value:
                best_value = move_value
                best_pos = i

    return best_pos


# Find best move for hard difficulty
def findBestMoveHard(board):
    best_value = -float('inf')
    best_pos = -1

    for i in range(9):
        if board[i] == '-':
            board[i] = '0'
            move_value = miniMax(board, False)
            board[i] = '-'
            if move_value > best_value:
                best_value = move_value
                best_pos = i

    return best_pos


# Check for winner
def checkWinner(board):
    score = evaluateScore(board)

    if score == 1:
        return 'Computer Won!'
    elif score == -1:
        return 'You Won!'
    elif '-' not in board:
        return "It's a tie!"
    else:
        return None


# User turn handler
def userTurn(row, col):
    if buttons[row][col]['text'] == "" and board[row * 3 + col] == '-':
        buttons[row][col]['text'] = 'X'
        board[row * 3 + col] = 'X'
        winner = checkWinner(board)
        if winner:
            messagebox.showinfo("Game Over", winner)
            resetBoard()
        else:
            aiTurn()


# AI turn handler
def aiTurn():
    best_move = ai_level(board)
    row = best_move // 3
    col = best_move % 3
    buttons[row][col]['text'] = '0'
    board[best_move] = '0'
    winner = checkWinner(board)
    if winner:
        messagebox.showinfo("Game Over", winner)
        resetBoard()


# Reset the board for a new game
def resetBoard():
    global board
    chooseDifficulty()
    board = ['-' for _ in range(9)]
    for row in range(3):
        for col in range(3):
            buttons[row][col]['text'] = ""


# Difficulty selection dialog
def chooseDifficulty():
    root.withdraw()
    difficulty_window = tk.Toplevel(root)
    difficulty_window.title("Choose Difficulty")

    tk.Label(difficulty_window, text="Choose difficulty level:").pack(padx=10,pady=10)

    tk.Button(difficulty_window, text="Easy", command=lambda: setDifficulty(difficulty_window, 1)).pack(side="left",
                                                                                                         padx=10,
                                                                                                         pady=10)
    tk.Button(difficulty_window, text="Normal", command=lambda: setDifficulty(difficulty_window, 2)).pack(side="left",
                                                                                                           padx=10,
                                                                                                           pady=10)
    tk.Button(difficulty_window, text="Hard", command=lambda: setDifficulty(difficulty_window, 3)).pack(side="left",
                                                                                                         padx=10,
                                                                                                         pady=10)
    difficulty_window.protocol("WM_DELETE_WINDOW", onClosing)


def setDifficulty(window, level):
    global ai_level
    if level == 1:
        ai_level = findBestMoveEasy
    elif level == 2:
        ai_level = findBestMoveNormal
    elif level == 3:
        ai_level = findBestMoveHard
    window.destroy()
    root.deiconify()
    startGame()


def startGame():
    # Start the game
    player = random.choice(['X', '0'])
    if player == '0':
        aiTurn()

def onClosing():
    root.quit()
    root.destroy()


# Initialize the board
board = ['-' for _ in range(9)]

# Create the main window
root = tk.Tk()
root.title("Tic-Tac-Toe")

# Set the window close event handler
root.protocol("WM_DELETE_WINDOW", onClosing)

# Create buttons for the board
buttons = [[None for _ in range(3)] for _ in range(3)]
for row in range(3):
    for col in range(3):
        buttons[row][col] = tk.Button(root, text="", font=('normal', 40, 'normal'), width=5, height=2,
                                      command=lambda r=row, c=col: userTurn(r, c))
        buttons[row][col].grid(row=row, column=col)

# Show difficulty selection dialog
chooseDifficulty()

root.mainloop()
