import tkinter as tk
import tkinter.messagebox
import random
import settings


class Board:

    def __init__(self, location, remaining_mines_label, remaining_cells_label, play_button) -> None:
        self.cells = []
        self.location = location
        self.remaining_mines_label = remaining_mines_label
        self.remaining_cells_label = remaining_cells_label

        self.play_button_img = tk.PhotoImage(file="images/btn_smile.png")
        self.play_button = play_button

        self.has_mines = False
        self.is_playing = False

        self.start_game()

    def start_game(self):
        self.reset_board()
        self.is_playing = True
        self.display_labels()

    def reset_board(self):
        for cell in self.cells:
            cell.btn.destroy()
        self.cells.clear()
        self.create_cells()
        self.randomize_mines()

        self.play_button_img = tk.PhotoImage(file="images/btn_smile.png")
        self.play_button.configure(image=self.play_button_img)

    def display_labels(self):
        self.remaining_cells_label.configure(text=self.remaining_cells)
        self.remaining_mines_label.configure(text=self.remaining_mines)

    def create_cells(self):
        for x in range(settings.GRID_ROWS):
            for y in range(settings.GRID_COLS):
                new_cell = Cell(x, y, self.location)
                new_cell.board = self
                new_cell.btn.grid(column=new_cell.y, row=new_cell.x)
                self.cells.append(new_cell)

    def randomize_mines(self):
        # def randomize_mines(self, selected_cell):
        if not self.has_mines:
            # rand_cell = random.sample(
            #     [cell for cell in cells if cell != selected_cell], settings.MINES_COUNT)
            rand_cell = random.sample(self.cells, settings.MINES_COUNT)

            for cell in rand_cell:
                cell.is_mine = True
            # board_has_mines = True

    def game_over(self, clicked_cell):
        self.is_playing = False
        for cell in self.cells:
            if cell.is_mine:
                cell.img = tk.PhotoImage(file="images/mine.png")
                cell.btn.configure(image=cell.img)
            if cell.is_guess and not cell.is_mine:
                cell.img = tk.PhotoImage(file="images/wrong_flag.png")
                cell.btn.configure(image=cell.img)

        clicked_cell.img = tk.PhotoImage(file="images/clicked_mine.png")
        clicked_cell.btn.configure(image=clicked_cell.img)

        self.play_button_img = tk.PhotoImage(file="images/btn_lost.png")
        self.play_button.configure(image=self.play_button_img)

    def win_game(self):
        if self.remaining_cells == 0:
            self.is_playing = False
            for cell in self.cells:
                if cell.is_mine:
                    cell.img = tk.PhotoImage(file="images/flag.png")
                    cell.btn.configure(image=cell.img)

            self.play_button_img = tk.PhotoImage(file="images/btn_win.png")
            self.play_button.configure(image=self.play_button_img)

    @property
    def remaining_cells(self):
        return len([cell for cell in self.cells if not cell.clicked and not cell.is_mine])

    @property
    def remaining_mines(self):
        return len([cell for cell in self.cells if cell.is_mine]) - len([cell for cell in self.cells if cell.is_guess])


class Cell:
    def __init__(self, x, y, location=None, board=None) -> None:

        self.board = board

        self.x = x
        self.y = y
        self.is_mine = False
        self.is_guess = False
        self.clicked = False

        self.img = tk.PhotoImage(file="images/empty_block.png")

        self.btn = tk.Button(location,
                             text="",
                             image=self.img,
                             width=settings.CELL_WIDTH,
                             height=settings.CELL_HEIGHT,
                             bg='gray',
                             )
        self.btn.bind('<Button-1>', self.left_click)   # Left Click
        self.btn.bind('<Button-3>', self.right_click)  # Right Click

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def _get_surrounding_cells(self):
        surroundings = []

        for cell in self.board.cells:
            if cell.x == self.x - 1 and cell.y == self.y - 1:
                surroundings.append(cell)
            if cell.x == self.x - 1 and cell.y == self.y:
                surroundings.append(cell)
            if cell.x == self.x - 1 and cell.y == self.y + 1:
                surroundings.append(cell)
            if cell.x == self.x and cell.y == self.y - 1:
                surroundings.append(cell)
            if cell.x == self.x and cell.y == self.y + 1:
                surroundings.append(cell)
            if cell.x == self.x + 1 and cell.y == self.y - 1:
                surroundings.append(cell)
            if cell.x == self.x + 1 and cell.y == self.y:
                surroundings.append(cell)
            if cell.x == self.x + 1 and cell.y == self.y + 1:
                surroundings.append(cell)

        return surroundings

    @property
    def surrounding_hidden_cells(self):
        return [cell for cell in self._get_surrounding_cells() if not cell.clicked]

    @property
    def count_surrounding_mines(self):
        return len([cell for cell in self._get_surrounding_cells() if cell.is_mine])

    def left_click(self, event):
        if self.board.is_playing and not self.clicked:
            if self.is_mine:
                self.board.game_over(self)
            else:
                self.reveal()
                self.board.win_game()
                self.board.display_labels()

    def reveal(self):
        if not self.clicked and not self.is_mine:
            self.clicked = True
            self.img = tk.PhotoImage(
                file=f"images/{str(self.count_surrounding_mines)}.png")
            self.btn.configure(image=self.img)

            if self.count_surrounding_mines == 0:
                for cell in self.surrounding_hidden_cells:
                    cell.reveal()

    def right_click(self, event):
        if not self.clicked:
            if self.is_guess:
                self.img = tk.PhotoImage(file="images/empty_block.png")
                self.btn.configure(image=self.img)
                self.is_guess = False
            else:
                self.img = tk.PhotoImage(file="images/flag.png")
                self.btn.configure(image=self.img)
                self.is_guess = True
            self.board.display_labels()


########################################
