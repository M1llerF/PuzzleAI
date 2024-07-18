from BotFactory import BotFactory
from Maze import Maze
from RewardSystem import RewardConfig
from BotStatistics import BotStatistics
from BotProfile import BotProfile, ProfileManager
from typing import Any, List, Optional

class GameEnvironment:
    def __init__(self, width: int = 10, height: int = 10, profile_directory: str = 'profiles'):
        """
        Initialize the GameEnvironment with a maze, bot factory, and profile manager.

        :param width: Width of the maze.
        :param height: Height of the maze.
        :param profile_directory: Directory where profiles are stored.
        """
        self.maze = Maze(width, height)
        self.bot_factory = BotFactory(self.maze)
        self.profile_manager = ProfileManager(profile_directory)
        self.bots: List = []
        self.register_bots()

    def register_bots(self):
        """
        Register available bots with the bot factory.
        """
        from QLearningBot import QLearningBot  # Ensure QLearningBot is imported only when needed
        self.bot_factory.register_bot('QLearningBot', QLearningBot)
        # Register other bots as needed
        # self.bot_factory.register_bot('AnotherBot', AnotherBot)
        
    def setup_new_profile(self, profile_name: str, bot_type: str, config, reward_config):
        """
        Set up a new bot profile and save it.

        :param profile_name: Name of the profile.
        :param bot_type: Type of the bot.
        :param config: Configuration for the bot.
        :param reward_config: Reward configuration for the bot.
        """
        profile = BotProfile(profile_name, bot_type, config, reward_config, BotStatistics(), {})
        self.profile_manager.save_profile(profile)
        self.setup_bots(profile.bot_type, profile.name, config, reward_config, profile.statistics, profile.bot_specific_data)

    def game_loop(self, rounds: int, bot_index: int, visualize: bool = False, visualization_window: Optional[Any] = None):
        """
        Run the game loop for a specified number of rounds.

        :param rounds: Number of rounds to run.
        :param bot_index: Index of the bot to run.
        :param visualize: Whether to visualize the game.
        :param visualization_window: Visualization window object.
        """
        bot = self.bots[bot_index]
        for _ in range(rounds):
            bot.run_episode()
            self.reset_environment(bot_index)
            if visualize and visualization_window:
                visualization_window.update_visualization()

    def reset_environment(self, bot_index: int):
        """
        Reset the environment for the specified bot.

        :param bot_index: Index of the bot to reset.
        """
        self.maze.setup_simple_maze()
        for bot in self.bots:
            if bot == self.bots[bot_index]:
                bot.reset_bot()

    def load_profile(self, profile_name: str):
        """
        Load a bot profile from the profile manager.

        :param profile_name: Name of the profile to load.
        """
        profile = self.profile_manager.load_profile(profile_name)
        self.apply_profile(profile)

    def apply_profile(self, profile) -> int:
        """
        Apply a loaded profile to the environment.

        :param profile: The bot profile to apply.
        :return: The index of the bot.
        """
        # Check if a bot with the same profile name already exists
        bot_index = next((i for i, bot in enumerate(self.bots) if bot.profile_name == profile.name), -1)
        if bot_index == -1:
            # If the bot does not exist, create a new one and append it
            bot = self.bot_factory.create_bot(
                profile.bot_type,
                profile.name,
                profile.config,
                profile.reward_config,
                profile.statistics,
                profile.bot_specific_data
            )
            self.bots.append(bot)
            bot_index = len(self.bots) - 1
        else:
            bot = self.bots[bot_index]
            bot.config = profile.config
            bot.reward_config = profile.reward_config
            bot.statistics = profile.statistics
            bot.bot_specific_data = profile.bot_specific_data

        return bot_index

    def setup_bots(self, bot_type: str, bot_name: str, config, reward_config, statistics, bot_specific_data):
        """
        Set up bots and add them to the environment.

        :param bot_type: Type of the bot.
        :param bot_name: Name of the bot.
        :param config: Configuration for the bot.
        :param reward_config: Reward configuration for the bot.
        :param statistics: Statistics object for the bot.
        :param bot_specific_data: Specific data for the bot.
        """
        self.bots.append(self.bot_factory.create_bot(bot_type, bot_name, config, reward_config, statistics, bot_specific_data))

    def save_profiles(self):
        """
        Save all bot profiles to the profile manager.
        """
        for bot in self.bots:
            profile = BotProfile(
                name = bot.profile_name,
                bot_type=type(bot).__name__,
                config=bot.config,
                reward_config=bot.reward_system.reward_config,
                bot_specific_data=bot.get_bot_specific_data(),
                statistics=bot.statistics
            )
            self.profile_manager.save_profile(profile)
