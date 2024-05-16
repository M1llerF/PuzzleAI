from collections import deque
import matplotlib.pyplot as plt
import numpy as np

class Maze:
    def __init__(self, width, height, start=None, end=None):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.start = start
        self.end = end

        # Initialize the figure and axes here for reuse
        self.fig, self.ax = plt.subplots()
        plt.ion() # Enable interactive mode for live plotting
    
    def is_valid_position(self, x, y):
        #print(f"x: {x}, y: {y}, self.height: {self.height}, self.width: {self.width}")
        # ! and self.grid[x][y] == 0 causes error
        return 0 <= x < self.height and 0 <= y < self.width and self.grid[x][y] == 0 # 0 is an open path.

    
    def set_wall(self, x, y):
        if 0 <= x < self.height and 0 <= y < self.width:
            self.grid[x][y] = 1
        else:
            raise ValueError("Position out of maze bounds")
    
    def display(self):
        for row in self.grid:
            print(''.join('#' if cell == 1 else ' ' for cell in row))
    
    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                self.height = len(lines)
                self.width = len(lines[0].strip())
                self.grid = [[int(char) for char in line.strip()] for line in lines]
        except IOError as e:
            print(f"Error reading file: {e}")

    def is_solvable(self):
        return True  # Placeholder for now
    
    def set_start(self, x, y):
        if self.is_valid_position(x, y):
            self.start = (x, y)
        else:
            raise ValueError("Invalid start position")
    
    def set_goal(self, x, y):
        if self.is_valid_position(x, y):
            self.end = (x, y)
        else:
            raise ValueError("Invalid goal position")
    
    def setup_simple_maze(self):
        self.grid = [
            [1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 1],
            [1, 1, 0, 1, 0, 1],
            [1, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 1],
            [1, 1, 1, 1, 1, 1]
        ]
        self.set_start(1, 1)
        self.set_goal(4, 4)

    def display_with_bot(self, bot_position):
        """ Display the maze with the bot's current position highlighted. """
        self.ax.cla()  # Clear the current axis to prepare for a new drawing
        color_grid = np.array(self.grid, dtype=int)
        color_grid[self.start] = 2
        color_grid[self.end] = 3
        color_grid[bot_position] = 4

        # Using a simple colormap and normalization
        cmap = plt.cm.viridis
        norm = plt.Normalize(0, 4)
        
        self.ax.imshow(color_grid, cmap=cmap, norm=norm, interpolation='none')
        
        self.ax.set_xticks(np.arange(-.5, self.width, 1), minor=True)
        self.ax.set_yticks(np.arange(-.5, self.height, 1), minor=True)
        self.ax.grid(which='minor', color='w', linestyle='-', linewidth=2)
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])

        plt.pause(0.01)  # Pause briefly to update the plot
    
    def finalize_display(self):
        plt.ioff()  # Turn off interactive mode
        plt.show()