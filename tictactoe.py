import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, master):
        self.master = master
        master.title("Tic Tac Toe")

        self.current_player = 'X'
        self.board = [' ' for i in range(9)]

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

    def switch_player(self):
        if self.current_player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'

    def check_victory(self):
        return (self.board[0] == self.board[1] == self.board[2] != ' ' or
                self.board[3] == self.board[4] == self.board[5] != ' ' or
                self.board[6] == self.board[7] == self.board[8] != ' ' or
                self.board[0] == self.board[3] == self.board[6] != ' ' or
                self.board[1] == self.board[4] == self.board[7] != ' ' or
                self.board[2] == self.board[5] == self.board[8] != ' ' or
                self.board[0] == self.board[4] == self.board[8] != ' ' or
                self.board[2] == self.board[4] == self.board[6] != ' ')

    def check_draw(self):
        return ' ' not in self.board

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


root = tk.Tk()
tictactoe = TicTacToe(root)
root.mainloop()