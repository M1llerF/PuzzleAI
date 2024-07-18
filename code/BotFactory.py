from RewardSystem import RewardSystem

class BotFactory:
    def __init__(self, maze):
        """
        Initialize the BotFactory with a given maze.
        
        :param maze: The maze instance that the bots will navigate.
        """
        self.maze = maze
        self.bot_registry = {}

    def register_bot(self, bot_type, bot_class):
        """
        Register a new bot type with its corresponding class.

        :param bot_type: A string representing the type of the bot.
        :param bot_class: The class of the bot to be registered.
        """
        self.bot_registry[bot_type] = bot_class

    def create_bot(self, bot_type, profile_name, config, reward_config, statistics, bot_specific_data):
        """
        Create an instance of the specified bot type.

        :param bot_type: The type of bot to create.
        :param profile_name: The profile name for the bot.
        :param config: The configuration for the bot.
        :param reward_config: The reward configuration for the bot.
        :param statistics: The statistics instance to track the bot's performance.
        :param bot_specific_data: Specific data needed for the bot's initialization.

        :return: An instance of the specified bot.
        
        :raises ValueError: If the bot type is not registered.
        """
        if bot_type not in self.bot_registry:
            raise ValueError(f"Unknown bot type: {bot_type}")

        bot_class = self.bot_registry[bot_type]
        reward_system = RewardSystem(self.maze, reward_config)
        bot_instance = bot_class(self.maze, config, reward_system, statistics, profile_name=profile_name)
        
        if hasattr(bot_instance, 'initialize_specific_data'):
            bot_instance.initialize_specific_data(bot_specific_data)

        return bot_instance
