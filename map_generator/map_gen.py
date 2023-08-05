import tkinter as tk
import pandas as pd

import settings


class Grid:
    """
    Class that provides a grid of cells in a Tkinter window, allowing
    interactive coloring of cells that can be saved to a CSV file.

    ...

    Attributes
    ----------
    rows : int
        Number of rows in the grid
    cols : int
        Number of columns in the grid
    cell_size : int
        Size of each cell in pixels
    grid : List[List[int]]
        2D list representing the grid state
    color_map : Dict[str, int]
        Mapping from color names to integer values
    current_color : str
        Current color selected for drawing
    canvas : tk.Canvas
        The Tkinter Canvas for drawing
    """

    def __init__(
        self,
        master,
        rows=settings.ROWS,
        cols=settings.COLS,
        cell_size=settings.CELL_SIZE,
    ):
        """
        Creates a new Grid instance.

        Parameters
        ----------
        master : tk.Root
            The root Tkinter window
        rows : int, optional
            Number of rows in the grid, by default 10
        cols : int, optional
            Number of columns in the grid, by default 10
        cell_size : int, optional
            Size of each cell in pixels, by default 20
        """
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = [[0] * cols for _ in range(rows)]
        self.color_map = settings.COLOR_MAP
        self.current_color = "black"
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
        """
        Event handler for mouse clicks and drags. Updates the clicked cell's
        color and redraws it.

        Parameters
        ----------
        event : tk.Event
            The event information
        """
        row = event.y // self.cell_size
        col = event.x // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = self.color_map[self.current_color]
            self.draw_cell(row, col)

    def draw_cell(self, row, col):
        """
        Draws a cell on the canvas with the color corresponding to its
        current state.

        Parameters
        ----------
        row : int
            Row number of the cell
        col : int
            Column number of the cell
        """
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        color = list(self.color_map.keys())[
            list(self.color_map.values()).index(self.grid[row][col])
        ]
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=1)

    def save_grid(self):
        """Saves the current state of the grid to a CSV file."""
        df = pd.DataFrame(self.grid)
        df.to_csv(settings.MAP_FLOOR_BLOCKS, index=False, header=False)


class ColorChooser:
    """
    Class that provides a dropdown menu for choosing a color in a Tkinter window.

    ...

    Attributes
    ----------
    grid : Grid
        The grid on which to operate
    variable : tk.StringVar
        The variable for the dropdown menu
    option_menu : tk.OptionMenu
        The dropdown menu
    """

    def __init__(self, master, grid):
        """
        Creates a new ColorChooser instance.

        Parameters
        ----------
        master : tk.Root
            The root Tkinter window
        grid : Grid
            The grid on which to operate
        """
        self.grid = grid
        self.variable = tk.StringVar(master)
        self.variable.set(list(grid.color_map.keys())[0])  # default value
        self.option_menu = tk.OptionMenu(
            master, self.variable, *grid.color_map.keys(), command=self.choose_color
        )
        self.option_menu.pack()

    def choose_color(self, value):
        """
        Sets the current color of the grid to the chosen value.

        Parameters
        ----------
        value : str
            The chosen color value
        """
        self.grid.current_color = value


def key(event):
    """
    Event handler for keypresses. If 's' key is pressed, the current state of
    the grid is saved to a CSV file.

    Parameters
    ----------
    event : tk.Event
        The event information
    """
    if event.char == "s":
        g.save_grid()


# Create and start the application
root = tk.Tk()
g = Grid(root)
c = ColorChooser(root, g)
root.bind("<Key>", key)
root.mainloop()
