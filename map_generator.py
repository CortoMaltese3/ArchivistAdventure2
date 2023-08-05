import tkinter as tk
import pandas as pd

class Grid:
    """Grid is a class that provides a drawing grid on a Tkinter canvas."""

    def __init__(self, master, rows=10, cols=10, cell_size=20):
        """Initializes a new grid with the given dimensions."""
        # Grid dimensions
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size

        # Initialize grid with all cells as 0
        self.grid = [[0]*cols for _ in range(rows)]

        # Dictionary to map colors to numbers
        self.color_map = {"white": 0, "black": 1, "red": 2, "green": 3, "blue": 4}

        # Current color for drawing
        self.current_color = "black"

        # Create canvas for drawing
        self.canvas = tk.Canvas(master, 
                                width=self.cols*self.cell_size, 
                                height=self.rows*self.cell_size)
        self.canvas.pack()

        # Draw all cells
        for row in range(rows):
            for col in range(cols):
                self.draw_cell(row, col)

        # Bind mouse events for drawing
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<B1-Motion>", self.click)

    def click(self, event):
        """Handles a mouse click or drag event on the canvas."""
        # Calculate clicked cell
        row = event.y // self.cell_size
        col = event.x // self.cell_size

        # Update cell if within grid bounds
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = self.color_map[self.current_color]
            self.draw_cell(row, col)

    def draw_cell(self, row, col):
        """Draws a cell on the canvas with the correct color."""
        # Calculate cell boundaries
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        # Determine cell color
        color = list(self.color_map.keys())[list(self.color_map.values()).index(self.grid[row][col])]

        # Draw cell on canvas
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=1)

    def save_grid(self):
        """Saves the current state of the grid to a CSV file."""
        df = pd.DataFrame(self.grid)
        df.to_csv('grid.csv', index=False, header=False)


class ColorChooser:
    """ColorChooser provides a dropdown menu for choosing the drawing color."""

    def __init__(self, master, grid):
        """Initializes a new color chooser for the given grid."""
        self.grid = grid
        self.variable = tk.StringVar(master)

        # Set default color
        self.variable.set(list(grid.color_map.keys())[0]) # default value

        # Create dropdown menu
        self.option_menu = tk.OptionMenu(master, self.variable, *grid.color_map.keys(), command=self.choose_color)
        self.option_menu.pack()

    def choose_color(self, value):
        """Updates the current drawing color."""
        self.grid.current_color = value


def key(event):
    """Handles a keypress event."""
    if event.char == 's':
        g.save_grid()

# Initialize tkinter root window
root = tk.Tk()

# Create drawing grid and color chooser
g = Grid(root)
c = ColorChooser(root, g)

# Bind 's' key for saving
root.bind('<Key>', key)

# Start tkinter main loop
root.mainloop()
