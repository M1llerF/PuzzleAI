from RewardSystem import RewardSystem

class BotFactory:
    def __init__(self, maze):
        self.maze = maze
        self.bot_registry = {}

    def register_bot(self, bot_type, bot_class):
        self.bot_registry[bot_type] = bot_class

    def create_bot(self, bot_type, profile_name, config, reward_config, tools_config, statistics, bot_specific_data):
        if bot_type not in self.bot_registry:
            raise ValueError(f"Unknown bot type: {bot_type}")

        bot_class = self.bot_registry[bot_type]
        reward_system = RewardSystem(self.maze, reward_config)
        bot_instance = bot_class(self.maze, config, reward_system, tools_config, statistics, profile_name=profile_name)
        
        if hasattr(bot_instance, 'initialize_specific_data'):
            bot_instance.initialize_specific_data(bot_specific_data)

        return bot_instance
