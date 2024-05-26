from RewardSystem import RewardSystem, RewardConfig
from BotTools import BotTools
# TODO Determine whether we want to add statistics to this? If not, how will we get statistics??
class BaseBot:
    def __init__(self, maze, q_learning_config, reward_system, tool_config): #! TODO Should add statistics to this
        self.maze = maze
        self.q_learning_config = q_learning_config
        self.reward_system = reward_system
        self.tool_config = tool_config
    
    def reset(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def calculate_state(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def run_episode(self):
        raise NotImplementedError("This method should be implemented by subclasses.")
