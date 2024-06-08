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
        self.load_profile_menu()

    
    def register_bots(self):
        from QLearningBot import QLearningBot
        # Register other bots as needed
        self.bot_factory.register_bot('QLearningBot', QLearningBot)
        # self.bot_factory.register_bot('AnotherBot', AnotherBot)

    def setup_new_profile(self):
        profile_name = input("Enter a name for the new profile: ")
        bot_type = input("Enter the bot type (e.g., 'QLearningBot'): ")

        config_mapping = {
            'QLearningBot': QLearningConfig,
            # Add other bot types and their config classes here
        }

        if bot_type in config_mapping:
            config_class = config_mapping[bot_type]
            config = config_class()
            config.customize()
        else:
            raise ValueError(f"Unknown bot type: {bot_type}")

        tools_config = BotToolsConfig()
        tools_config.customize_tools()

        reward_config = RewardConfig()
        reward_config.customize_reward_modifiers()
                        #    name,         bot_type, config, q_learning_config, reward_config, tools_config, q_table, statistics
        profile = BotProfile(profile_name, bot_type, config, reward_config, tools_config, BotStatistics(), {})


        self.profile_manager.save_profile(profile)
        self.setup_bots(profile.bot_type, profile.name, config, reward_config, tools_config, profile.statistics, profile.bot_specific_data)
        
    def game_loop(self):
        print("(From GameEnvironment.py, GameEnvironment, game_loop(...))")
        loop_count = 2
        bot = self.bots[0]
        for i in range(loop_count):
            i += 1
            print(f"Game loop {i}")
            bot.run_episode()
            self.reset_environment()

    def reset_environment(self):
        self.maze.setup_simple_maze()
        for bot in self.bots:
            bot.reset_bot()

    def load_profile_menu(self):
        profiles = self.profile_manager.list_profiles()
        print("Available profiles:")
        for idx, profile_name in enumerate(profiles, start=1):
            print(f"{idx}. {profile_name}")
        choice = input("Select a profile by number, or press Enter to create a new profile: ")
        if choice.isdigit() and 1 <= int(choice) <= len(profiles):
            profile = self.profile_manager.load_profile(profiles[int(choice) - 1])
            self.apply_profile(profile)
        else:
            self.setup_new_profile()


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

        # bot = self.bot_factory.create_bot(profile.bot_type, profile.name)
        # bot.q_learning.config = profile.q_learning_config
        # bot.reward_system.reward_config = profile.reward_config
        # bot.tools.config = profile.tools_config
        # bot.q_learning.q_table = profile.q_table
        # bot.statistics = profile.statistics


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

if __name__ == "__main__":
    game_env = GameEnvironment()
    print("Starting game........")
    game_env.game_loop()
    