from Maze import Maze
from SolverBot import SolverBot, BotConfig
from ReinforcementAgent import QLearning, RewardSystem

max_episodes_number = 100 #12560
class EnvironmentSetup:
    def __init__(self, width, height):
        self.maze = Maze(width, height)
        self.maze.setup_simple_maze() #* Assumes this sets start and goal
        self.q_learning = QLearning()
        self.reward_system = RewardSystem(self.maze)
        
    
    def reset_environment(self):
        """Reset the environment for the next episode."""
        self.maze.setup_simple_maze()
        self.q_learning.reset()

class GameEnvironment:
    def __init__(self, width, height, max_episodes=max_episodes_number):
        self.env_setup = EnvironmentSetup(width, height)
        self.maze = self.env_setup.maze
        config = BotConfig()
        self.maze_solver_bot = SolverBot(self.maze, self.env_setup.q_learning, self.env_setup.reward_system, config)
        self.max_episodes = max_episodes
        self.episode_count = 0

    def start_game(self):
        """Start the game loop."""
        self.is_running = True
        self.game_loop()

    def game_loop(self):
        """Main game loop that runs the episodes."""
        modValue = 0
        if(max_episodes_number < 10):
            modValue = max_episodes_number
        else:
            max_episodes_number / 2


        while self.episode_count < self.max_episodes:
            if(self.episode_count % 100 == 0):
                print(f"Running episode {self.episode_count + 1}")
            if self.maze.is_solvable():
                #print("Maze is solvable, running episode...")
                self.maze_solver_bot.run_episode()
            else:
                print("Maze is not solvable, resetting...")
                self.env_setup.reset_environment()
            self.episode_count += 1
            self.maze_solver_bot.reset_bot()
            self.env_setup.reset_environment()  # Reset for the next episode

    
    def stop_game(self):
        """Stop the game loop."""
        print("Stopping the game...")
        self.is_running = False
        print("Game stopped!")
    
    def display_heatmap(self):
        self.maze.display_with_heatmap('code/NonCodeFiles/HeatmapData.txt')

if __name__ == "__main__":
    game_env = GameEnvironment(25, 15, max_episodes=max_episodes_number)
    game_env.start_game()
    game_env.display_heatmap()
