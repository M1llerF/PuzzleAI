from collections import deque
import matplotlib.pyplot as plt
import numpy as np
import random

class Maze:
    def __init__(self, min_width, max_width, min_height, max_height, start=None, end=None):
        self.min_width = min_width
        self.max_width = max_width
        self.min_height = min_height
        self.max_height = max_height
        self.width = random.randint(min_width, max_width)
        self.height = random.randint(min_height, max_height)
        self.grid = [[1 for _ in range(self.width)] for _ in range(self.height)]
        self.start = start
        self.end = end

        # Initialize the figure and axes here for reuse
        self.fig, self.ax = plt.subplots()
        plt.ion()  # Enable interactive mode for live plotting

    def is_valid_position(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width and self.grid[x][y] == 0  # 0 is an open path.

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
        self.width = random.randint(self.min_width, self.max_width)
        self.height = random.randint(self.min_height, self.max_height)
        self.grid = [[1 for _ in range(self.width)] for _ in range(self.height)]
        
        def dfs(x, y):
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + 2 * dx, y + 2 * dy
                if 1 <= nx < self.height - 1 and 1 <= ny < self.width - 1 and self.grid[nx][ny] == 1:
                    self.grid[x + dx][y + dy] = 0
                    self.grid[nx][ny] = 0
                    dfs(nx, ny)

        # Start the maze generation from a random point within the inner grid
        start_x = random.randrange(1, self.height - 1, 2)
        start_y = random.randrange(1, self.width - 1, 2)
        self.grid[start_x][start_y] = 0
        dfs(start_x, start_y)

        # Set random start and goal positions within the inner grid
        start_positions = [(x, y) for x in range(1, self.height - 1) for y in range(1, self.width - 1) if self.grid[x][y] == 0]
        self.start = random.choice(start_positions)
        self.end = random.choice(start_positions)

        self.set_start(*self.start)
        self.set_goal(*self.end)

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

# from collections import deque
# import matplotlib.pyplot as plt
# import random
# import numpy as np

# class Maze:
#     def __init__(self, width, height, start=None, end=None):
#         self.width = width
#         self.height = height
#         self.grid = [[0 for _ in range(width)] for _ in range(height)]
#         self.start = start
#         self.end = end

#         # Initialize the figure and axes here for reuse
#         self.fig, self.ax = plt.subplots()
#         plt.ion() # Enable interactive mode for live plotting
    
#     def is_valid_position(self, x, y):
#         #print(f"x: {x}, y: {y}, self.height: {self.height}, self.width: {self.width}")
#         # ! and self.grid[x][y] == 0 causes error
#         return 0 <= x < self.height and 0 <= y < self.width and self.grid[x][y] == 0 # 0 is an open path.

    
#     def set_wall(self, x, y):
#         if 0 <= x < self.height and 0 <= y < self.width:
#             self.grid[x][y] = 1
#         else:
#             raise ValueError("Position out of maze bounds")
    
#     def display(self):
#         for row in self.grid:
#             print(''.join('#' if cell == 1 else ' ' for cell in row))
    
#     def load_from_file(self, filename):
#         try:
#             with open(filename, 'r') as file:
#                 lines = file.readlines()
#                 self.height = len(lines)
#                 self.width = len(lines[0].strip())
#                 self.grid = [[int(char) for char in line.strip()] for line in lines]
#         except IOError as e:
#             print(f"Error reading file: {e}")

#     def is_solvable(self):
#         return True  # Placeholder for now
    
#     def set_start(self, x, y):
#         if self.is_valid_position(x, y):
#             self.start = (x, y)
#         else:
#             raise ValueError("Invalid start position")
    
#     def set_goal(self, x, y):
#         if self.is_valid_position(x, y):
#             self.end = (x, y)
#         else:
#             raise ValueError("Invalid goal position")
    
#     # def setup_simple_maze(self):
#     #     self.grid = GENERATED_MAZE
#     #     self.set_start(1, 1)
#     #     self.set_goal(4, 4)
    
#     def setup_simple_maze(self):
#         def dfs(x, y):
#             directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
#             random.shuffle(directions)
#             for dx, dy in directions:
#                 nx, ny = x + 2 * dx, y + 2 * dy
#                 if 1 <= nx < self.height - 1 and 1 <= ny < self.width - 1 and self.grid[nx][ny] == 1:
#                     self.grid[x + dx][y + dy] = 0
#                     self.grid[nx][ny] = 0
#                     dfs(nx, ny)

#         # Initialize the grid with walls
#         self.grid = [[1 for _ in range(self.width)] for _ in range(self.height)]

#         # Start the maze generation from a random point within the inner grid
#         start_x = random.randrange(1, self.height - 1, 2)
#         start_y = random.randrange(1, self.width - 1, 2)
#         self.grid[start_x][start_y] = 0
#         dfs(start_x, start_y)

#         # Set random start and goal positions within the inner grid
#         start_positions = [(x, y) for x in range(1, self.height - 1) for y in range(1, self.width - 1) if self.grid[x][y] == 0]
#         self.start = random.choice(start_positions)
#         self.end = random.choice(start_positions)

#         self.set_start(*self.start)
#         self.set_goal(*self.end)

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