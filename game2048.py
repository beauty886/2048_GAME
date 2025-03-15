import tkinter as tk
import random

# Game Constants
GRID_SIZE = 4
CELL_SIZE = 100
FONT = ("Arial", 24, "bold")
BACKGROUND_COLOR = "#faf8ef"
CELL_COLORS = {
    0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
    32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61", 512: "#edc850",
    1024: "#edc53f", 2048: "#edc22e"
}

class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 Game")
        self.root.configure(bg=BACKGROUND_COLOR)
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.cells = []
        self.create_ui()
        self.start_game()
        self.root.bind("<Key>", self.handle_key)

    def create_ui(self):
        self.frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        self.frame.grid()
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Arial", 16), bg=BACKGROUND_COLOR)
        self.score_label.grid(row=0, column=0, columnspan=GRID_SIZE, pady=10)
        for i in range(GRID_SIZE):
            row = []
            for j in range(GRID_SIZE):
                cell = tk.Label(self.frame, text="", width=4, height=2, font=FONT, bg=CELL_COLORS[0], relief="ridge", bd=5)
                cell.grid(row=i, column=j, padx=5, pady=5)
                row.append(cell)
            self.cells.append(row)
        self.new_game_button = tk.Button(self.root, text="New Game", font=("Arial", 14), command=self.start_game, bg="#8f7a66", fg="white")
        self.new_game_button.grid(row=1, column=0, columnspan=GRID_SIZE, pady=10)

    def start_game(self):
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.add_new_2()
        self.add_new_2()
        self.update_ui()

    def add_new_2(self):
        empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if self.grid[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = 2

    def update_ui(self):
        self.score_label.config(text=f"Score: {self.score}")
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.grid[i][j]
                self.cells[i][j].config(text=str(value) if value != 0 else "", bg=CELL_COLORS.get(value, "#3c3a32"))

    def handle_key(self, event):
        prev_grid = [row[:] for row in self.grid]
        if event.keysym == "Up":
            self.move_up()
        elif event.keysym == "Down":
            self.move_down()
        elif event.keysym == "Left":
            self.move_left()
        elif event.keysym == "Right":
            self.move_right()
        if self.grid != prev_grid:
            self.add_new_2()
        self.update_ui()
        self.check_state()

    def compress(self):
        new_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        for i in range(GRID_SIZE):
            pos = 0
            for j in range(GRID_SIZE):
                if self.grid[i][j] != 0:
                    new_grid[i][pos] = self.grid[i][j]
                    pos += 1
        self.grid = new_grid

    def merge(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE - 1):
                if self.grid[i][j] == self.grid[i][j+1] and self.grid[i][j] != 0:
                    self.grid[i][j] *= 2
                    self.grid[i][j+1] = 0
                    self.score += self.grid[i][j]

    def move_left(self):
        self.compress()
        self.merge()
        self.compress()

    def move_right(self):
        self.grid = [row[::-1] for row in self.grid]
        self.move_left()
        self.grid = [row[::-1] for row in self.grid]

    def move_up(self):
        self.grid = [list(row) for row in zip(*self.grid)]
        self.move_left()
        self.grid = [list(row) for row in zip(*self.grid)]

    def move_down(self):
        self.grid = [list(row) for row in zip(*self.grid)][::-1]
        self.move_left()
        self.grid = [list(row) for row in zip(*self.grid)][::-1]

    def check_state(self):
        if any(2048 in row for row in self.grid):
            self.show_result("WON")
        elif not any(0 in row for row in self.grid) and not self.can_merge():
            self.show_result("LOST")

    def can_merge(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE - 1):
                if self.grid[i][j] == self.grid[i][j+1] or self.grid[j][i] == self.grid[j+1][i]:
                    return True
        return False

    def show_result(self, result):
        popup = tk.Toplevel(self.root)
        popup.title(result)
        tk.Label(popup, text=f"You {result}!", font=("Arial", 20)).pack(pady=10)
        tk.Button(popup, text="Play Again", command=self.restart_game).pack(pady=5)

    def restart_game(self):
        self.start_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
