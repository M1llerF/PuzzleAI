import pickle

from QLearningBot import QLearningConfig
from RewardSystem import RewardConfig
from BotTools import BotToolsConfig
from BotStatistics import BotStatistics



class BotProfile:
    def __init__(self, bot_type, q_learning_config, reward_config, tools_config, q_table, statistics):
        self.bot_type = bot_type
        self.q_learning_config = q_learning_config
        self.reward_config = reward_config
        self.tools_config = tools_config
        self.q_table = q_table
        self.statistics = statistics

    def to_dict(self):
        """Convert the profile to a dictionary."""
        return {
            "bot_type": self.bot_type,
            "q_learning_config": self.q_learning_config.__dict__,
            "reward_config": self.reward_config.__dict__,
            "tools_config": self.tools_config.tools,
            "q_table": self.q_table,
            "statistics": self.statistics.__dict__
        }
    
    @staticmethod
    def from_dict(data):
        q_learning_config = data['q_learning_config']
        if isinstance(q_learning_config, dict):
            q_learning_config = QLearningConfig(**q_learning_config)

        reward_config = data['reward_config']
        if isinstance(reward_config, dict):
            reward_config = RewardConfig(**reward_config)

        tools_config_data = data['tools_config']
        tools_config = BotToolsConfig()
        if isinstance(tools_config_data, dict):
            tools_config.tools.update(tools_config_data)
        
        statistics = data['statistics']
        if isinstance(statistics, dict):
            statistics = BotStatistics()
            statistics.__dict__.update(data['statistics'])

        
        print("Statistics data:", data['statistics'])  # Debugging print

        # statistics = BotStatistics()
        # statistics.__dict__.update(data['statistics'])

        return BotProfile(
            data['bot_type'],
            q_learning_config,
            reward_config,
            tools_config,
            data['q_table'],
            statistics
        )

class ProfileManager:
    def __init__(self, profile_directory):
        self.profile_directory = profile_directory

    def save_profile(self, profile):
        """Save a profile to a pickle file."""
        print("SAVE PROFILE CALLED")
        filename = f"{self.profile_directory}/{profile.bot_type}.pkl"
        with open(filename, 'wb') as f:
            pickle.dump(profile.to_dict(), f)

    def load_profile(self, profile_name):
        """Load a profile from a pickle file."""
        print("LOAD PROFILE CALLED")
        filename = f"{self.profile_directory}/{profile_name}.pkl"
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        return BotProfile.from_dict(data)

    def list_profiles(self):
        """List all available profiles."""
        import os
        return [f.replace('.pkl', '') for f in os.listdir(self.profile_directory) if f.endswith('.pkl')]