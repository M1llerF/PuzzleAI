from Maze import Maze
from SolverBot import SolverBot

max_episodes_number = 2
class GameEnvironment:
    def __init__(self, width, height, max_episodes=max_episodes_number):
        self.maze = Maze(width, height)
        self.maze.setup_simple_maze()  # Ensure this sets start and goal
        self.maze_solver_bot = SolverBot(self.maze)
        self.is_running = False
        self.max_episodes = max_episodes
        self.episode_count = 0
    
    def start_game(self):
        print("Starting the game...")
        
        self.is_running = True
        self.game_loop()

    def game_loop(self):
        while self.episode_count < self.max_episodes:
            print(f"Running episode {self.episode_count + 1}")
            if self.maze.is_solvable():
                print ("Maze is solvable, running episode...")
                self.maze_solver_bot.run_episode()
            else:
                print("Maze is not solvable, resetting...")
                self.reset_environment()
            self.episode_count += 1
            self.reset_environment()  # Reset for the next episode
    
    def reset_environment(self):
        self.maze.setup_simple_maze()  # Re-setup the maze to its initial configuration
        self.maze_solver_bot.reset_bot()  # Reset bot's position and state
    
    def stop_game(self):
        print("Stopping the game...")
        self.is_running = False
        print("Game stopped!")

# Ensure this block is present
if __name__ == "__main__":
    game_env = GameEnvironment(10, 10, max_episodes=max_episodes_number)
    game_env.start_game()
