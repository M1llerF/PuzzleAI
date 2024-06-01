from BotFactory import BotFactory
from Maze import Maze
from QLearningBot import QLearningBot, QLearningConfig
from RewardSystem import RewardConfig, RewardSystem
from BotTools import BotToolsConfig
from BotStatistics import BotStatistics
from BotProfile import BotProfile, ProfileManager

class GameEnvironment:
    def __init__(self):
        width = 10  # example width
        height = 10  # example height
        
        self.maze = Maze(width, height)
        self.bot_factory = BotFactory(self.maze)
        self.profile_manager = ProfileManager('profiles')
        self.bots = []
        self.load_profile_menu()

    def setup_bots(self, bot_type, bot_name): # .super goes to this
        self.bots.append(self.bot_factory.create_bot(bot_type=bot_type,profile_name=bot_name))
        
    def game_loop(self):
        print("(From GameEnvironment.py, GameEnvironment, game_loop(...))")
        loop_count = 100
        bot = self.bots[0]
        for i in range(loop_count):
            i += 1
            print(f"Game loop {i}")
            #print("(From GameEnvironment.py, GameEnvironment, game_loop(...)) game_Bot: ", bot)
            bot.run_episode()
            #print("(From GameEnvironment.py, GameEnvironment, game_loop(...)) Episode run should be complete.")
            self.reset_environment()
            #print("(From GameEnvironment.py, GameEnvironment, game_loop(...)) Resetting environment")

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
        print("Applying profile:")
        print("Q-Learning Config:")
        print(profile.q_learning_config.__dict__)
        print("Reward Config:")
        print(profile.reward_config.__dict__)
        print("Tools Config:")
        print(profile.tools_config.__dict__)
        print("Statistics:")
        print(profile.statistics.__dict__)


        bot = self.bot_factory.create_bot(profile.bot_type, profile.name)
        bot.q_learning.config = profile.q_learning_config
        bot.reward_system.reward_config = profile.reward_config
        bot.tools.config = profile.tools_config
        bot.q_learning.q_table = profile.q_table
        bot.statistics = profile.statistics
        self.bots.append(bot)

    # def setup_new_profile(self):
    #     profile_name = input("Enter a name for the new profile: ")
    #     q_learning_config = QLearningConfig()
    #     reward_config = RewardConfig()
    #     tools_config = BotToolsConfig()
    #     q_learning_config.customize_q_learning()
    #     reward_config.customize_reward_modifiers()
    #     profile = BotProfile(profile_name, q_learning_config, reward_config, tools_config, {}, BotStatistics())
    #     self.profile_manager.save_profile(profile)
    #     self.setup_bots(profile)

    def setup_new_profile(self):
        profile_name = input("Enter a name for the new profile: ")
        #! Reward values are not being utilized. Instead the seems to be getting the original values from the RewardConfig class
        # Create and customize configurations
        q_learning_config = QLearningConfig()
        reward_config = RewardConfig()
        print("Final reward modifiers:")
        for key, value in reward_config.reward_modifiers.items():
            print(f"{key}: {value}")
        tools_config = BotToolsConfig()
        print("\n Tools Config:" + str(tools_config.__dict__), "\n")
        q_learning_config.customize_q_learning()
        reward_config.customize_reward_modifiers()
        tools_config.customize_tools()
        
        # Ensure the bot_type is set correctly
        bot_type = 'QLearningBot'  # Set to a valid bot type
    
        # Create a new profile with the valid bot_type
        profile = BotProfile(profile_name, bot_type, q_learning_config, reward_config, tools_config, {}, BotStatistics())
        
        # Save the new profile
        self.profile_manager.save_profile(profile)
        
        # Set up bots using the new profile
        self.setup_bots(profile)

    def setup_bots(self, profile):
        q_learning_config = profile.q_learning_config
        reward_config = profile.reward_config
        tools_config = profile.tools_config
        bot_statistics = profile.statistics
        reward_system = RewardSystem(self.maze, reward_config)
        q_learning_bot = QLearningBot(self.maze, q_learning_config, reward_system, tools_config, bot_statistics, profile_name=profile.name)
        q_learning_bot.q_learning.q_table = profile.q_table
        self.bots.append(q_learning_bot)

    def save_profiles(self):
        for bot in self.bots:
            profile = BotProfile(
                name = bot.profile_name,
                bot_type=type(bot).__name__,
                q_learning_config=bot.q_learning.q_learning_config,
                reward_config=bot.reward_system.reward_config,
                tools_config=bot.tools.tools_config,
                q_table=bot.q_learning.q_table,
                statistics=bot.statistics
            )
            self.profile_manager.save_profile(profile)


if __name__ == "__main__":
    game_env = GameEnvironment()
    print("Starting game........")
    game_env.game_loop()
    