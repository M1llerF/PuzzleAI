from Maze import Maze
from MazeCreatorBot import MazeCreatorBot
from MazeSolverBot import MazeSolverBot

class GameEnvironment:
    def __init__ (self, width, height):
        self.maze = Maze(width, height)
        self.maze_creator_bot = MazeCreatorBot(self.maze)
        self.maze_solver_bot = MazeSolverBot(self.maze)
        self.is_running = False
    
    def start_game(self):
        """"Start the game environment"""
        self.is_running = True
        self.maze_creator_bot.create_maze() #! Assumes that the maze is created before the game starts
        self.game_loop()

    def game_loop(self):
        """"Run the main game loop"""
        while self.is_running:
            if(self.maze.is_solvable()): # Check if the maze is solvable. MazeCreator should already have created a solvable maze.
                path = self.maze_solver_bot.solve_maze() #! Assumes that the method
                if path:
                    print("Maze solved!")
                    self.display_solution(path)
                else:
                    print("No solution found!")
            else:
                print("Maze is not solvable!")
            self.stop_game() #* For now we are stopping after one 
    
    def display_solution(self, path):
            """Optional: Display the solution path."""
            for position in path:
                self.maze.grid[position[0]][position[1]] = 2  # Mark the path on the maze
            self.maze.display()
    
    def stop_game(self):
        """Stop the game environment"""
        self.is_running = False
        print("Game stopped!")
    
    #* Not sure if this is needed
    def pause_game(self):
        """Pause the game environment"""
        self.is_running = False
        print("Game paused!")
