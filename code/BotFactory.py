# from QLearningBot import QLearningBot, QLearningConfig
# from BotStatistics import BotStatistics
# from RewardSystem import RewardConfig, RewardSystem
# from BotTools import BotToolsConfig

# class BotFactory:
#     def __init__(self, maze):
#         self.maze = maze
    
#     def create_bot(self, bot_type):
#         bot_statistics = BotStatistics()
#         reward_config = RewardConfig()
#         q_learning_config = QLearningConfig(learning_rate=0.1, discount_factor=0.9)
#         reward_system = RewardSystem(self.maze, reward_config)
#         reward_system.reward_config.test_print("From BotFactory")
#         tool_config = BotToolsConfig()

#         if bot_type == 'QLearningBot':
#             return QLearningBot(self.maze, q_learning_config, reward_system, tool_config, bot_statistics)
#         # Add more bot types here
#         else:
#             raise ValueError(f"Unknown bot type: {bot_type}")
from RewardSystem import RewardConfig, RewardSystem
from QLearningBot import QLearningBot, QLearningConfig
from BotTools import BotToolsConfig
from BotStatistics import BotStatistics
from BaseBot import BaseBot

class BotFactory:
    def __init__(self, maze):
        self.maze = maze

    def create_bot(self, bot_type, profile_name):
        if bot_type == "QLearningBot":
            q_learning_config = QLearningConfig()
            reward_config = RewardConfig()
            tool_config = BotToolsConfig()
            bot_statistics = BotStatistics()
            reward_system = RewardSystem(self.maze, reward_config)
            
            return QLearningBot(self.maze, q_learning_config, reward_system, tool_config, bot_statistics, profile_name)
        raise ValueError(f"Unknown bot type: {bot_type}")

