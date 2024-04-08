from random import randint
from tkinter import *


class TicTac:

    class Players:

        player = "x"
        ai = "o"

    tie = "Tie"

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.turn = self.Players.player
        self.finished = False
        self.data = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
        ]
        self.scores = {
            self.Players.player: -1,
            self.Players.ai: 1,
            self.tie: 0,
        }

        canvas = Canvas(height=height, width=width)

        canvas.create_line(width // 3, 0, width // 3, height, fill="black", width=2)
        canvas.create_line(width * 2 // 3, 0, width * 2 // 3, height, fill="black", width=2)

        canvas.create_line(0, height // 3, width, height // 3, fill="black", width=2)
        canvas.create_line(0, height * 2 // 3, width, height * 2 // 3, fill="black", width=2)

        self.canvas = canvas

    def draw_point(self, row, column):
        if self.turn == self.Players.player:
            if self.Players.player == "x":
                self.draw_x(row, column)
            else:
                self.draw_o(row, column)
        else:
            if self.Players.ai == "x":
                self.draw_x(row, column)
            else:
                self.draw_o(row, column)

    def draw_x(self, row=0, columns=0):
        row = row + 1
        columns = columns + 1

        x_o = (self.width * columns // 3) - (self.width // 3)
        x_i = self.width * columns // 3
        y_o = (self.height * row // 3) - (self.height // 3)
        y_i = self.height * row // 3
        self.canvas.create_line(x_o, y_o, x_i, y_i, width=5)
        self.canvas.create_line(x_o, y_i, x_i, y_o, width=5)

    def draw_o(self, row=None, columns=None):
        row = row + 1
        columns = columns + 1

        x = (self.width * columns // 3) - ((self.width // 3) // 2)
        y = (self.height * row // 3) - ((self.height // 3) // 2)
        r = (self.width // 8)
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        self.canvas.create_oval(x0, y0, x1, y1, width=5)

    def draw_winner_line(self, row, column):
        row = row + 1
        column = column + 1

        x = (self.width * column // 3) - ((self.width // 3) // 2)
        y = (self.height * row // 3) - ((self.height // 3) // 2)
        r = (self.width // 8)
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        self.canvas.create_oval(x0, y0, x1, y1, width=5)

    def get_row_and_column_from_event(self, event):
        mouse_y = event.y
        if mouse_y < self.width // 3:
            row = 0
        elif mouse_y < self.width * 2 // 3:
            row = 1
        else:
            row = 2

        mouse_x = event.x
        if mouse_x < self.height // 3:
            column = 0
        elif mouse_x < self.height * 2 // 3:
            column = 1
        else:
            column = 2

        return row, column

    def punctuate(self, row, column):
        if self.data[row][column] != "":
            return
        self.draw_point(row, column)
        self.data[row][column] = self.turn
        self.turn = self.Players.player if self.turn == self.Players.ai else self.Players.ai

    def check_winner(self, commit_win=True):
        print(self.data)
        # check row
        for row, data_row in enumerate(self.data):
            if data_row[0] == data_row[1] == data_row[2] != "":
                if commit_win:
                    y = (self.height * (row + 1) // 3) - ((self.height // 3) // 2)
                    x0 = (self.width // 3) - ((self.width // 3) // 2)
                    x1 = (self.width * 3 // 3) - ((self.width // 3) // 2)
                    self.canvas.create_line(x0, y, x1, y, width=10, fill="green")
                return data_row[0]

        # check col
        for col in range(3):
            if self.data[0][col] == self.data[1][col] == self.data[2][col] != "":
                if commit_win:
                    x = (self.width * (col + 1) // 3) - ((self.width // 3) // 2)
                    y0 = (self.height // 3) - ((self.height // 3) // 2)
                    y1 = (self.height * 3 // 3) - ((self.height // 3) // 2)
                    self.canvas.create_line(x, y0, x, y1, width=10, fill="green")
                return self.data[0][col]

        # check diagonals
        if self.data[0][0] == self.data[1][1] == self.data[2][2] != "":
            if commit_win:
                x0 = (self.width * 3 // 3) - ((self.width // 3) // 2)
                y0 = (self.height * 3// 3) - ((self.height // 3) // 2)
                x1 = (self.width // 3) - ((self.width // 3) // 2)
                y1 = (self.height // 3) - ((self.height // 3) // 2)
                self.canvas.create_line(x0, y0, x1, y1, width=10, fill="green")
            return self.data[0][0]
        if self.data[2][0] == self.data[1][1] == self.data[0][2] != "":
            if commit_win:
                x0 = (self.width * 3 // 3) - ((self.width // 3) // 2)
                y0 = (self.height // 3) - ((self.height // 3) // 2)
                x1 = (self.width // 3) - ((self.width // 3) // 2)
                y1 = (self.height * 3 // 3) - ((self.height // 3) // 2)
                self.canvas.create_line(x0, y0, x1, y1, width=10, fill="green")
            return self.data[2][0]

        if self.is_board_full():
            return self.tie
        return None

    def is_board_full(self):
        for row in self.data:
            for cell in row:
                if cell == "":
                    return False
        return True

    def ai_move(self):
        if self.turn != self.Players.ai:
            return
        score, row, col = self.minimax(0, True)
        return row, col

    def sim_ai_move(self, x, y):
        self.data[x][y] = self.Players.ai

    def sim_human_move(self, x, y):
        self.data[x][y] = self.Players.player

    def erase_sim_move(self, x, y):
        self.data[x][y] = ""

    def minimax(self, depth, is_maximizing):
        winner = self.check_winner(commit_win=False)
        if winner:
            return self.scores[winner], "", ""
        if is_maximizing:
            best_score = -float("inf")
            best_move = {}
            for x, x_values in enumerate(self.data):
                for y, y_value in enumerate(x_values):
                    if self.data[x][y] == "":
                        self.sim_ai_move(x, y)
                        score, _, _ = self.minimax(depth + 1, False)
                        self.erase_sim_move(x, y)
                        best_score = max(score, best_score)
                        if best_score == score:
                            best_move = {
                                "x": x,
                                "y": y,
                            }
            return best_score, best_move["x"], best_move["y"]
        else:
            best_score = float("inf")
            best_move = {}
            for x, x_values in enumerate(self.data):
                for y, y_value in enumerate(x_values):
                    if self.data[x][y] == "":
                        self.sim_human_move(x, y)
                        score, _, _ = self.minimax(depth + 1, True)
                        self.erase_sim_move(x, y)
                        best_score = min(score, best_score)
                        if best_score == score:
                            best_move = {
                                "x": x,
                                "y": y,
                            }
            return best_score, best_move["x"], best_move["y"]
