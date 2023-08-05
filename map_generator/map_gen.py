from collections import defaultdict

import tkinter as tk
import pandas as pd

import settings


class Grid:
    def __init__(
        self,
        master,
        rows=settings.ROWS,
        cols=settings.COLS,
        cell_size=settings.CELL_SIZE,
    ):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = [
            [settings.COLOR_MAP.get("air")[1]] * cols for _ in range(rows)
        ]  # using 'air' instead of 'white'
        self.color_map = settings.COLOR_MAP
        self.current_color = "wall"
        self.canvas = tk.Canvas(
            master, width=self.cols * self.cell_size, height=self.rows * self.cell_size
        )
        self.canvas.pack()

        for row in range(rows):
            for col in range(cols):
                self.draw_cell(row, col)

        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<B1-Motion>", self.click)

    def click(self, event):
        row = event.y // self.cell_size
        col = event.x // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = self.color_map[self.current_color][
                1
            ]  # use the numerical code from COLOR_MAP
            self.draw_cell(row, col)

    def draw_cell(self, row, col):
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        color = [
            v[0] for k, v in self.color_map.items() if v[1] == self.grid[row][col]
        ][0]
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=1)

    def save_grid(self):
        """Saves the current state of the grid to multiple CSV files."""
        df = pd.DataFrame(self.grid)

        air_num = settings.COLOR_MAP['air'][1]

        # Mapping of entities to their numerical codes for each category
        map_floor_blocks = {v[1]: v[1] for k, v in settings.COLOR_MAP.items() if k in {"air", "wall"}}
        map_entities = {v[1]: v[1] for k, v in settings.COLOR_MAP.items() if k in {"air", "player", "enemy"}}
        map_grass = {v[1]: v[1] for k, v in settings.COLOR_MAP.items() if k in {"air", "grass"}}
        map_objects = {v[1]: v[1] for k, v in settings.COLOR_MAP.items() if k in {"air", "object"}}

        # Create copies of the DataFrame for each category and replace values not in the category with 'air'
        df_floor_blocks = df.copy().replace({k: air_num for k in set(df.values.flatten()) - set(map_floor_blocks.keys())})
        df_entities = df.copy().replace({k: air_num for k in set(df.values.flatten()) - set(map_entities.keys())})
        df_grass = df.copy().replace({k: air_num for k in set(df.values.flatten()) - set(map_grass.keys())})
        df_objects = df.copy().replace({k: air_num for k in set(df.values.flatten()) - set(map_objects.keys())})

        # Save the modified DataFrames to CSV files
        df_floor_blocks.to_csv(settings.MAP_FLOOR_BLOCKS, index=False, header=False)
        df_entities.to_csv(settings.MAP_ENTITIES, index=False, header=False)
        df_grass.to_csv(settings.MAP_GRASS, index=False, header=False)
        df_objects.to_csv(settings.MAP_OBJECTS, index=False, header=False)


class ColorChooser:
    def __init__(self, master, grid):
        self.grid = grid
        self.variable = tk.StringVar(master)
        self.variable.set(list(grid.color_map.keys())[0])  # default value
        self.option_menu = tk.OptionMenu(
            master, self.variable, *grid.color_map.keys(), command=self.choose_color
        )
        self.option_menu.pack()

    def choose_color(self, value):
        self.grid.current_color = value


def key(event):
    if event.char == "s":
        g.save_grid()


root = tk.Tk()
g = Grid(root)
c = ColorChooser(root, g)
root.bind("<Key>", key)
root.mainloop()
