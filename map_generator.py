import tkinter as tk
import pandas as pd

class Grid:
    def __init__(self, master, rows=10, cols=10, cell_size=20):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = [[0]*cols for _ in range(rows)]
        self.color_map = {"white": 0, "black": 1}
        self.current_color = "black"
        self.canvas = tk.Canvas(master, 
                                width=self.cols*self.cell_size, 
                                height=self.rows*self.cell_size)
        self.canvas.pack()

        for row in range(rows):
            for col in range(cols):
                self.draw_cell(row, col)

        self.canvas.bind("<Button-1>", self.click)

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
        self.entry = tk.Entry(master)
        self.entry.pack()
        self.entry.bind("<Return>", self.add_color)
        self.grid = grid

    def add_color(self, event):
        new_color = self.entry.get()
        if new_color not in self.grid.color_map:
            new_number = max(self.grid.color_map.values()) + 1
            self.grid.color_map[new_color] = new_number
        self.grid.current_color = new_color
        self.entry.delete(0, tk.END)

def key(event):
    if event.char == 's':
        g.save_grid()

root = tk.Tk()
g = Grid(root)
c = ColorChooser(root, g)
root.bind('<Key>', key)
root.mainloop()
