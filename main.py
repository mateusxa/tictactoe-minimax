from tkinter import *
from tictac import TicTac


def callback(event):
    if tictac.finished:
        return
    row, column = tictac.get_row_and_column_from_event(event)
    tictac.punctuate(row, column)
    winner = tictac.check_winner()
    if winner:
        if winner == tictac.tie:
            print(f"It's a Tie!")
        else:
            print(f"Winner is: {winner}")
        tictac.finished = True
        return

    row, column = tictac.ai_move()
    print(f"from callback row: {row}, col: {column}")
    tictac.punctuate(row, column)
    winner = tictac.check_winner()
    if winner:
        if winner == tictac.tie:
            print(f"It's a Tie!")
        else:
            print(f"Winner is: {winner}")
        tictac.finished = True
        return


if __name__ == '__main__':
    root = Tk()

    canvas_height = 600
    canvas_width = 600

    tictac = TicTac(width=600, height=600)

    canvas = tictac.canvas
    canvas.pack()
    canvas.bind("<Button-1>", callback)
    root.mainloop()
