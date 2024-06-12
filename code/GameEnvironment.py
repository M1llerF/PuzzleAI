from BotFactory import BotFactory
from Maze import Maze
from QLearningBot import QLearningBot, QLearningConfig
from RewardSystem import RewardConfig, RewardSystem
from BotTools import BotToolsConfig
from BotStatistics import BotStatistics
from BotProfile import BotProfile, ProfileManager
from BotConfigs import QLearningConfig

class GameEnvironment:
    def __init__(self):
        width = 10  # example width
        height = 10  # example height
        
        self.maze = Maze(width, height)
        self.bot_factory = BotFactory(self.maze)
        self.profile_manager = ProfileManager('profiles')
        self.bots = []
        self.register_bots()
        # Removed terminal-based profile loading
        # self.load_profile_menu()

    def register_bots(self):
        from QLearningBot import QLearningBot
        # Register other bots as needed
        self.bot_factory.register_bot('QLearningBot', QLearningBot)
        # self.bot_factory.register_bot('AnotherBot', AnotherBot)
        
    def setup_new_profile(self, profile_name, bot_type, config, reward_config, tools_config):
        profile = BotProfile(profile_name, bot_type, config, reward_config, tools_config, BotStatistics(), {})
        self.profile_manager.save_profile(profile)
        self.setup_bots(profile.bot_type, profile.name, config, reward_config, tools_config, profile.statistics, profile.bot_specific_data)

    def game_loop(self, rounds, bot_index, progress_callback, visualize=False, visualization_window=None):
        print("(From GameEnvironment.py, GameEnvironment, game_loop(...))")
        print(bot_index)
        print(self.bots)
        bot = self.bots[bot_index]
        for i in range(rounds):
            bot.run_episode()
            self.reset_environment()
            progress_callback(i + 1, rounds)
            if visualize and visualization_window:
                visualization_window.update_visualization()

    def reset_environment(self):
        self.maze.setup_simple_maze()
        for bot in self.bots:
            bot.reset_bot()

    def load_profile(self, profile_name):
        profile = self.profile_manager.load_profile(profile_name)
        self.apply_profile(profile)

    def apply_profile(self, profile):
        bot = self.bot_factory.create_bot(profile.bot_type, profile.name, profile.config, profile.reward_config, profile.tools_config, profile.statistics, profile.bot_specific_data)
        print("Applying profile:")
        print("Config:")
        print(profile.config.__dict__)
        print("Tools Config:")
        print(profile.tools_config.__dict__)
        print("Statistics:")
        print(profile.statistics.__dict__)
        self.bots.append(bot)

    def setup_bots(self, bot_type, bot_name, config, reward_config, tools_config, statistics, bot_specific_data):
        self.bots.append(self.bot_factory.create_bot(bot_type=bot_type, profile_name=bot_name, config=config, reward_config=reward_config, tools_config=tools_config, statistics=statistics, bot_specific_data=bot_specific_data))

    def save_profiles(self):
        for bot in self.bots:
            profile = BotProfile(
                name = bot.profile_name,
                bot_type=type(bot).__name__,
                config=bot.config,
                reward_config=bot.reward_system.reward_config,
                tools_config=bot.tools.tools_config,
                bot_specific_data=bot.get_bot_specific_data(),
                statistics=bot.statistics
            )
            self.profile_manager.save_profile(profile)
