class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
    
    def is_valid_position(self, x, y):
        """ Check if the position (x, y) is valid """
        return 0 <= x < self.height and 0 <= y < self.width and self.grid[x][y] == 0
    
    def set_wall(self, x, y):
        """ Set the wall at position (x, y) """
        self.grid[x][y] = 1
    
    def display(self):
        """ Display the maze visually """
        for row in self.grid:
            print(' '.join(str(cell) for cell in row))
    
    def load_from_file(self, filename):
        """ Load the maze configuration from a file"""
        with open(filename, 'r') as file:
            lines = file.readlines()
            self.height = len(lines)
            self.width = len(lines[0].strip())
            self.grid = [[int(char) for char in line.strip()] for line in lines]
