import os
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
        """Save a profile to a pickle file and create necessary files."""
        print("SAVE PROFILE CALLED")
        profile_dir = f"{self.profile_directory}/{profile.name}"
        os.makedirs(profile_dir, exist_ok=True)
        filename = f"{profile_dir}/profile.pkl"
        
        # Save the profile data
        with open(filename, 'wb') as f:
            pickle.dump(profile.to_dict(), f)
        
        # Create empty Q-table file if it doesn't exist
        q_table_file = f"{profile_dir}/q_table.pkl"
        if not os.path.exists(q_table_file):
            with open(q_table_file, 'wb') as f:
                pickle.dump({}, f)
        
        # Create empty reward data file if it doesn't exist
        reward_file = f"{profile_dir}/SimulationRewards.txt"
        if not os.path.exists(reward_file):
            with open(reward_file, 'w') as f:
                f.write("")  # Write an empty string to create the file

        # Create empty heatmap data file if it doesn't exist
        heatmap_file = f"{profile_dir}/HeatmapData.txt"
        if not os.path.exists(heatmap_file):
            with open(heatmap_file, 'w') as f:
                f.write("")  # Write an empty string to create the file


    def load_profile(self, profile_name):
        """Load a profile from a pickle file."""
        print("LOAD PROFILE CALLED")
        profile_dir = f"{self.profile_directory}/{profile_name}"
        filename = f"{profile_dir}/profile.pkl"
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        return BotProfile.from_dict(data)
    
    def list_profiles(self):
        """List all available profiles."""
        return [d for d in os.listdir(self.profile_directory) if os.path.isdir(os.path.join(self.profile_directory, d))]
