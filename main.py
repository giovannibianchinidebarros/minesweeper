import tkinter as tk
from tkinter import ttk
import settings
from game_engine import *


def play_button_click():
    board.start_game()


window = tk.Tk()

window.configure(bg="black")

window.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
window.title("Minesweeper Game")
window.resizable(False, False)


img_0 = tk.PhotoImage(file="images/btn_smile.png")


top_frame = tk.Frame(
    window,
    bg=settings.TOP_COLOR,
    width=settings.WIDTH,
    height=settings.TOP_FRAME_HEIGHT
)
top_frame.place(x=0, y=0)

center_frame = tk.Frame(
    window,
    padx=5, pady=5,
    bg=settings.CENTER_COLOR,
    width=settings.WIDTH,
    height=settings.CENTER_FRAME_HEIGHT
)
center_frame.place(x=0, y=settings.CENTER_FRAME_Y_POS)


custom_font = ("Arial", 28, "bold italic")


remaining_mines_label = tk.Label(
    top_frame, text="board.mines_left", font=custom_font, foreground="red", background="black")
remaining_cells_label = tk.Label(
    top_frame, text="board.cells_left", font=custom_font, foreground="red", background="black")

play_button = tk.Button(top_frame,
                        image=img_0,
                        text="",
                        width=settings.BTN_SIZE,
                        height=settings.BTN_SIZE,
                        bg='gray',
                        )

play_button.configure(command=play_button_click)


remaining_mines_label.place(x=settings.LEFT_LABEL_X, y=settings.LEFT_LABEL_Y)
play_button.place(x=settings.PLAY_BUTTON_X, y=settings.PLAY_BUTTON_Y)
remaining_cells_label.place(x=settings.RIGHT_LABEL_X, y=settings.RIGHT_LABEL_Y)


board = Board(location=center_frame,
              remaining_cells_label=remaining_mines_label,
              remaining_mines_label=remaining_cells_label,
              play_button=play_button)
board.start_game()

window.mainloop()
