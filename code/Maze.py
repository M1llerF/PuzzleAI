from collections import deque
import matplotlib.pyplot as plt
import numpy as np
import random
import matplotlib.colors as mcolors
import mplcursors
class Maze:
    def __init__(self, width, height, start=None, end=None):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.start = start
        self.end = end
        self.minimum_distance = max(width, height) // 2
        self.setup_simple_maze()

        # Initialize the figure and axes here for reuse
        self.fig, self.ax = plt.subplots()
        plt.ion() # Enable interactive mode for live plotting
    
    def is_valid_position(self, x, y):
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
    
    def get_start(self):
        print("(From Maze.py, get_start(...)) Printing start: ",self.start)
        return self.start
    
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

    # def setup_simple_maze(self):
    #     self.grid = [
    #         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #         [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #         [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    #         [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    #         [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    #         [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    #         [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
    #         [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    #         [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    #         [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    #         [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    #         [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    #         [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    #         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    #         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    #     ]
    #     self.start = (1, 1)
    #     self.end = (13, 13)

    #     self.set_start(*self.start)
    #     self.set_goal(*self.end)
    def setup_simple_maze(self):
        # Randomly adjust width and height
        self.width = random.randrange(self.width, self.width + 3, 1)
        self.height = random.randrange(self.height, self.height + 3, 1)

        # Initialize grid with walls
        self.grid = [[1 for _ in range(self.width)] for _ in range(self.height)]
        
        def dfs_iterative(x, y):
            chosenAlgorithm = random.randint(1, 2)
            if(chosenAlgorithm == 1):
                stack = [(x, y)]
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

                while stack:
                    cx, cy = stack.pop()
                    random.shuffle(directions)
                    for dx, dy in directions:
                        nx, ny = cx + 2 * dx, cy + 2 * dy
                        if 1 <= nx < self.height - 1 and 1 <= ny < self.width - 1 and self.grid[nx][ny] == 1:
                            self.grid[cx + dx][cy + dy] = 0
                            self.grid[nx][ny] = 0
                            stack.append((cx, cy))
                            stack.append((nx, ny))
                            break
            else:
                stack = [(x, y)]
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

                while stack:
                    cx, cy = stack.pop()
                    random.shuffle(directions)
                    for dx, dy in directions:
                        nx, ny = cx + 2 * dx, cy + 2 * dy
                        if 1 <= nx < self.height - 1 and 1 <= ny < self.width - 1 and self.grid[nx][ny] == 1:
                            self.grid[cx + dx][cy + dy] = 0
                            self.grid[nx][ny] = 0
                            stack.append((nx, ny))

        # Randomly choose a starting position
        start_x = random.randrange(1, self.height - 1, 2)
        start_y = random.randrange(1, self.width - 1, 2)
        self.grid[start_x][start_y] = 0
        dfs_iterative(start_x, start_y)

        # Collect all path positions
        start_positions = [(x, y) for x in range(1, self.height - 1) for y in range(1, self.width - 1) if self.grid[x][y] == 0]
        self.start = random.choice(start_positions)
        
        # Ensure the goal is at least minimum_distance away from the start
        valid_end_positions = [pos for pos in start_positions if np.linalg.norm(np.array(pos) - np.array(self.start)) >= self.minimum_distance]
        
        if valid_end_positions:
            self.end = random.choice(valid_end_positions)
        else:
            # If no valid end positions, fallback to the farthest position
            self.end = max(start_positions, key=lambda pos: np.linalg.norm(np.array(pos) - np.array(self.start)))

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

        plt.pause(0.01)  # Pause briefly to update the plot. Default is 0.01 seconds.
    

    def display_with_heatmap(self, heatmap_file):
        """ Display the maze with the bot's current position highlighted. """
        self.ax.cla()  # Clear the current axis to prepare for a new drawing
        color_grid = np.array(self.grid, dtype=int)
        color_grid[self.start] = 2
        color_grid[self.end] = 3
        # Using a simple colormap and normalization
        
        cmap = plt.cm.tab20c
        norm = plt.Normalize(0, 4)
        
        self.ax.imshow(color_grid, cmap=cmap, norm=norm, interpolation='none')
        
        self.ax.set_xticks(np.arange(-.5, self.width, 1), minor=True)
        self.ax.set_yticks(np.arange(-.5, self.height, 1), minor=True)
        self.ax.grid(which='minor', color='w', linestyle='-', linewidth=2)
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])

        """Display the maze with a heatmap overlay from the heatmap file."""
    # Display the maze with a heatmap overlay from the heatmap file
        heatmap = np.zeros((self.height, self.width))
        total_visits = 0
        try:
            with open(heatmap_file, 'r') as f:
                for line in f:
                    x, y, count = map(int, line.strip().split(','))
                    heatmap[x, y] = count
                    total_visits += count
        except IOError as e:
            print(f"Error reading heatmap file: {e}")

        # Normalize percentages
        percentages = (heatmap / total_visits) * 100

        # Overlay the heatmap only on visited positions
        for x in range(self.height):
            for y in range(self.width):
                if heatmap[x, y] > 0:
                    percentage = percentages[x, y]
                    color_value = percentage / 2 # Normalize percentages to the 0%-2% range
                    rect = plt.Rectangle((y - 0.5, x - 0.5), 1, 1, color=plt.cm.hot(color_value), alpha=0.6)
                    self.ax.add_patch(rect)
                    font_size = max(8, 12 - len(f"{int(percentage)}%"))  # Adjust font size based on the number of digits
                    self.ax.text(y, x, f"{percentage:.2f}", color="black", ha='center', va='center', fontsize=font_size)

            # Highlight start and end positions
            self.ax.scatter(self.start[1], self.start[0], color='blue', s=100, edgecolor='black', label='Start')
            self.ax.scatter(self.end[1], self.end[0], color='green', s=100, edgecolor='black', label='End')


        self.finalize_display()
    
    #? Is this really needed? :
    def finalize_display(self):
        """Finalize the display by turning off interactive mode and showing the plot."""
        plt.ioff()
        plt.show()
