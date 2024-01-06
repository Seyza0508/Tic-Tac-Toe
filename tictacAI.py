import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, master):
        self.master = master
        master.title("Tic Tac Toe")

        self.current_player = 'X'
        self.board = [' ' for i in range(9)]
        self.difficulty = 'easy'

        # Create the difficulty selection
        self.difficulty_label = tk.Label(master, text="Select difficulty:", font=('Arial', 20))
        self.difficulty_label.pack()

        self.difficulty_var = tk.StringVar(master)
        self.difficulty_var.set("easy")
        self.difficulty_menu = tk.OptionMenu(master, self.difficulty_var, "easy", "medium", "hard")
        self.difficulty_menu.pack()

        # Create the turn label
        self.turn_label = tk.Label(master, text="Player X's turn", font=('Arial', 20))
        self.turn_label.pack()

        # Create the game board
        self.board_frame = tk.Frame(master)
        self.board_frame.pack()

        self.buttons = []
        for i in range(9):
            button = tk.Button(self.board_frame, text=' ', font=('Arial', 60), width=2, height=1,
                               command=lambda idx=i: self.make_move(idx))
            button.grid(row=i//3, column=i%3)
            self.buttons.append(button)

        # Create the reset button
        self.reset_button = tk.Button(master, text='Reset', font=('Arial', 30), command=self.reset_game)
        self.reset_button.pack()

    def make_move(self, idx):
        if self.board[idx] == ' ':
            self.buttons[idx].config(text=self.current_player)
            self.board[idx] = self.current_player

            if self.check_victory():
                self.end_game()
            elif self.check_draw():
                self.end_game(draw=True)
            else:
                self.switch_player()
                if self.current_player == 'O':
                    self.ai_move()

    def switch_player(self):
        if self.current_player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'
        self.turn_label.config(text="Player {}'s turn".format(self.current_player))

    def ai_move(self):
        self.difficulty = self.difficulty_var.get()
        if self.difficulty == 'easy':
            move = self.random_move()
        elif self.difficulty == 'medium':
            move = self.medium_move()
        else:
            move = self.hard_move()

        if move is not None:
            self.make_move(move)

    def random_move(self):
        available_moves = [i for i, cell in enumerate(self.board) if cell == ' ']
        return random.choice(available_moves) if available_moves else None

    def medium_move(self):
        move = self.find_winning_move('O')
        if move is not None:
            return move

        move = self.find_winning_move('X')
        if move is not None:
            return move

        return self.random_move()

    def hard_move(self):
        _, move = self.minimax('O', self.board)
        return move

    def minimax(self, player, board):
        if self.check_victory_board(board):
            return (1 if player == 'X' else -1, None)
        if self.check_draw_board(board):
            return (0, None)

        moves = [i for i, cell in enumerate(board) if cell == ' ']
        scores = []
        for move in moves:
            new_board = board.copy()
            new_board[move] = player
            score, _ = self.minimax('X' if player == 'O' else 'O', new_board)
            scores.append(score)

        if player == 'O':
            best_score = max(scores)
        else:
            best_score = min(scores)

        best_move = moves[scores.index(best_score)]
        return best_score, best_move

    def find_winning_move(self, player):
        for i in range(9):
            if self.board[i] == ' ':
                temp_board = self.board.copy()
                temp_board[i] = player
                if self.check_victory_board(temp_board):
                    return i
        return None

    def check_victory_board(self, board):
        winning_conditions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)             # Diagonals
        ]
        return any(board[a] == board[b] == board[c] != ' ' for a, b, c in winning_conditions)

    def check_draw_board(self, board):
        return ' ' not in board

    def check_victory(self):
        return self.check_victory_board(self.board)

    def check_draw(self):
        return self.check_draw_board(self.board)

    def end_game(self, draw=False):
        for button in self.buttons:
            button.config(state='disabled')

        if draw:
            messagebox.showinfo('Game Over', 'It is a draw!')
        else:
            messagebox.showinfo('Game Over', 'Player {} wins!'.format(self.current_player))

    def reset_game(self):
        for button in self.buttons:
            button.config(text=' ', state='normal')
        self.board = [' ' for i in range(9)]
        self.current_player = 'X'
        self.turn_label.config(text="Player X's turn")


root = tk.Tk()
tictactoe = TicTacToe(root)
root.mainloop()