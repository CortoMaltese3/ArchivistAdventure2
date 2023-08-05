import tkinter as tk
import pandas as pd

class Grid:
    def __init__(self, master, rows=10, cols=10, cell_size=20):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = [[0]*cols for _ in range(rows)]
        self.color_map = {"white": 0, "black": 1, "red": 2, "green": 3, "blue": 4}
        self.current_color = "black"
        self.canvas = tk.Canvas(master, 
                                width=self.cols*self.cell_size, 
                                height=self.rows*self.cell_size)
        self.canvas.pack()

        for row in range(rows):
            for col in range(cols):
                self.draw_cell(row, col)

        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<B1-Motion>", self.click)

    def click(self, event):
        row = event.y // self.cell_size
        col = event.x // self.cell_size
        self.grid[row][col] = self.color_map[self.current_color]
        self.draw_cell(row, col)

    def draw_cell(self, row, col):
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        color = list(self.color_map.keys())[list(self.color_map.values()).index(self.grid[row][col])]
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=1)

    def save_grid(self):
        df = pd.DataFrame(self.grid)
        df.to_csv('grid.csv', index=False, header=False)

class ColorChooser:
    def __init__(self, master, grid):
        self.grid = grid
        self.variable = tk.StringVar(master)
        self.variable.set(list(grid.color_map.keys())[0]) # default value
        self.option_menu = tk.OptionMenu(master, self.variable, *grid.color_map.keys(), command=self.choose_color)
        self.option_menu.pack()

    def choose_color(self, value):
        self.grid.current_color = value

def key(event):
    if event.char == 's':
        g.save_grid()

root = tk.Tk()
g = Grid(root)
c = ColorChooser(root, g)
root.bind('<Key>', key)
root.mainloop()
