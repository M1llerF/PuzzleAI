import pickle

from QLearningBot import QLearningConfig
from RewardSystem import RewardConfig
from BotTools import BotToolsConfig
from BotStatistics import BotStatistics



class BotProfile:
    def __init__(self, name, bot_type, config, reward_config, tools_config, statistics, bot_specific_data):
        self.name = name
        self.bot_type = bot_type
        self.config = config
        self.reward_config = reward_config
        self.tools_config = tools_config
        self.statistics = statistics
        self.bot_specific_data = bot_specific_data

    def to_dict(self):
        """Convert the profile to a dictionary."""
        return {
            "name": self.name,
            "bot_type": self.bot_type,
            "config": self.config.__dict__,
            "reward_config": self.reward_config.__dict__,
            "tools_config": self.tools_config.tools,
            "statistics": self.statistics.__dict__,
            "bot_specific_data": self.bot_specific_data

        }
    
    @staticmethod
    def from_dict(data):
        config_mapping = {
            'QLearningBot': QLearningConfig,
            # Add other bot types and their config classes here
        }
        config_class = config_mapping[data['bot_type']]#globals()[data['bot_type'] + "Config"]
        config = config_class(**data['config'])
        tools_config_data = data['tools_config']
        statistics = data['statistics']
        bot_specific_data = data['bot_specific_data']


        reward_config = data['reward_config']
        if isinstance(reward_config, dict):
            reward_config = RewardConfig(**reward_config)

        tools_config_data = data['tools_config']
        tools_config = BotToolsConfig()
        if isinstance(tools_config_data, dict):
            tools_config.tools.update(tools_config_data)
        
        if isinstance(statistics, dict):
            statistics = BotStatistics()
            statistics.__dict__.update(data['statistics'])



        
        #print("Statistics data:", data['statistics'])  # Debugging print

        # statistics = BotStatistics()
        # statistics.__dict__.update(data['statistics'])

        return BotProfile(
            name=data['name'],
            bot_type=data['bot_type'],
            config=config,
            reward_config=reward_config,
            tools_config=tools_config,
            statistics=statistics,
            bot_specific_data=bot_specific_data
        )

class ProfileManager:
    def __init__(self, profile_directory):
        self.profile_directory = profile_directory

    def save_profile(self, profile):
        """Save a profile to a pickle file."""
        print("SAVE PROFILE CALLED")
        filename = f"{self.profile_directory}/{profile.name}.pkl"
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