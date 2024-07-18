import matplotlib.pyplot as plt
import numpy as np
import random
from BotStatistics import BotStatistics
class Maze:
    def __init__(self, width, height, start=None, end=None):
        """
        Initialize the maze with given dimensions and optionally set start and end points.
        """
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
    
    def is_valid_position(self, bot_name, x, y):
        """
        Check if a position is valid (within bounds and not a wall).
        Optionally update the bot's statistics if it hits a wall.
        """
        is_valid = 0 <= x < self.height and 0 <= y < self.width and self.grid[x][y] == 0
        if not is_valid and bot_name != None:
            BotStatistics().update_times_hit_wall(bot_name)
        return is_valid # 0 is an open path.

    def set_wall(self, x, y):
        """
        Set a wall at the specified position.
        Raise an error if the position is out of bounds.
        """
        if 0 <= x < self.height and 0 <= y < self.width:
            self.grid[x][y] = 1
        else:
            raise ValueError("Position out of maze bounds")
    
    def get_start(self):
        """
        Get the start position of the maze.
        """
        return self.start
    
    def set_start(self, x, y):
        if self.is_valid_position(None, x, y):
            self.start = (x, y)
        else:
            raise ValueError("Invalid start position")
    
    def set_goal(self, x, y):
        """
        Set the goal position of the maze if it's valid.
        Raise an error if the position is invalid.
        """
        if self.is_valid_position(None, x, y):
            self.end = (x, y)
        else:
            raise ValueError("Invalid goal position")
        
    def setup_simple_maze(self):
        # Randomly adjust width and height
        self.width = random.randint(self.width, self.width + 2)
        self.height = random.randint(self.height, self.height + 2)

        # Initialize grid with walls
        self.grid = [[1 for _ in range(self.width)] for _ in range(self.height)]

        def dfs_iterative(x, y, algorithm_type):
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
                        if algorithm_type == 1:
                            stack.append((cx, cy))
                        stack.append((nx, ny))
                        break

        # Randomly choose a starting position
        start_x = random.randrange(1, self.height - 1, 2)
        start_y = random.randrange(1, self.width - 1, 2)
        self.grid[start_x][start_y] = 0

        # Randomly choose an algorithm type
        algorithm_type = random.randint(1, 2)
        dfs_iterative(start_x, start_y, algorithm_type)

        # Collect all path positions
        start_positions = [(x, y) for x in range(1, self.height - 1) for y in range(1, self.width - 1) if self.grid[x][y] == 0]
        self.start = random.choice(start_positions)

        # Ensure the goal is at least minimum_distance away from the start
        self.end = self.get_farthest_valid_end_position(start_positions)

        self.set_start(*self.start)
        self.set_goal(*self.end)

    def get_farthest_valid_end_position(self, start_positions):
        """
        Get the farthest valid end position that is at least minimum_distance away from the start.
        """
        valid_end_positions = [
            pos for pos in start_positions if np.linalg.norm(np.array(pos) - np.array(self.start)) >= self.minimum_distance
        ]

        if valid_end_positions:
            return random.choice(valid_end_positions)
        else:
            return max(start_positions, key=lambda pos: np.linalg.norm(np.array(pos) - np.array(self.start)))

        
    def display_with_bot(self, bot_position, canvas):
        """
        Display the maze with the bot's current position highlighted on the canvas.
        """
        canvas.delete("all")
        cell_width = canvas.winfo_width() / self.width
        cell_height = canvas.winfo_height() / self.height

        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 1:
                    canvas.create_rectangle(x * cell_width, y * cell_height,
                                            (x + 1) * cell_width, (y + 1) * cell_height,
                                            fill="black")

        start = self.get_start()
        end = self.end

        canvas.create_rectangle(start[1] * cell_width, start[0] * cell_height,
                                (start[1] + 1) * cell_width, (start[0] + 1) * cell_height,
                                fill="blue")

        canvas.create_rectangle(end[1] * cell_width, end[0] * cell_height,
                                (end[1] + 1) * cell_width, (end[0] + 1) * cell_height,
                                fill="green")

        canvas.create_oval(bot_position[1] * cell_width, bot_position[0] * cell_height,
                        (bot_position[1] + 1) * cell_width, (bot_position[0] + 1) * cell_height,
                        fill="red")    
    
    def finalize_display(self):
        """Finalize the display by turning off interactive mode and showing the plot."""
        plt.ioff()
        plt.show()
