from collections import deque

class Maze:
    def __init__(self, width, height, start=None, end=None):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.start = start
        self.end = end
    
    def is_valid_position(self, x, y):
        """ Check if the position (x, y) is valid within the maze boundaries and not a wall. """
        return 0 <= x < self.height and 0 <= y < self.width and self.grid[x][y] == 0
    
    def set_wall(self, x, y):
        """ Set the wall at position (x, y) by marking it as '1'. """
        if 0 <= x < self.height and 0 <= y < self.width:
            self.grid[x][y] = 1
        else:
            raise ValueError("Position out of maze bounds")
    
    def display(self):
        """ Display the maze visually with walls as '#' and open paths as ' '. """
        for row in self.grid:
            print(''.join('#' if cell == 1 else ' ' for cell in row))
    
    def load_from_file(self, filename):
        """ Load the maze configuration from a file. Each line represents a row of the maze. """
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                self.height = len(lines)
                self.width = len(lines[0].strip())
                self.grid = [[int(char) for char in line.strip()] for line in lines]
        except IOError as e:
            print(f"Error reading file: {e}")

    def is_solvable(self):
        """ Check if there is a path from the start to the end using BFS. """
        if self.grid[self.start[0]][self.start[1]] == 1 or self.grid[self.end[0]][self.end[1]] == 1:
            return False  # Start or end is blocked
        
        queue = deque([self.start])
        visited = set()
        visited.add(self.start)

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

        while queue:
            current = queue.popleft()
            if current == self.end:
                return True

            for direction in directions:
                next_pos = (current[0] + direction[0], current[1] + direction[1])
                if self.is_valid_position(next_pos[0], next_pos[1]) and next_pos not in visited:
                    visited.add(next_pos)
                    queue.append(next_pos)

        return False
    
    def set_start(self, x, y):
        """ Set the start position in the maze. """
        if self.is_valid_position(x, y):
            self.start = (x, y)
        else:
            raise ValueError("Invalid start position")
    
    def set_goal(self, x, y):
        """ Set the goal position in the maze. """
        if self.is_valid_position(x, y):
            self.end = (x, y)
        else:
            raise ValueError("Invalid goal position")