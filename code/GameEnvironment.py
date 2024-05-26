from BotFactory import BotFactory
from Maze import Maze
class GameEnvironment:
    def __init__(self):
        width = 10  # example width
        height = 10  # example height
        
        self.maze = Maze(width, height)
        self.bot_factory = BotFactory(self.maze)
        self.bots = []

    def setup_bots(self): # .super goes to this
        self.bots.append(self.bot_factory.create_bot('QLearningBot'))

    def start_game(self):
        self.setup_bots()
        self.game_loop() # From here, causes game start coordinates to be spam printed
        
    def game_loop(self):
        for bot in self.bots:
            #print("(From GameEnvironment.py, GameEnvironment, game_loop(...)) game_Bot: ", bot)
            bot.run_episode()
            #print("(From GameEnvironment.py, GameEnvironment, game_loop(...)) Episode run should be complete.")
            self.reset_environment()
            #print("(From GameEnvironment.py, GameEnvironment, game_loop(...)) Resetting environment")

    def reset_environment(self):
        self.maze.setup_simple_maze()
        for bot in self.bots:
            bot.reset_bot()

if __name__ == "__main__":
    game_env = GameEnvironment()
    game_env.start_game()