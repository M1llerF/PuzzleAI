import os
import pickle

from QLearningBot import QLearningConfig
from RewardSystem import RewardConfig
from BotStatistics import BotStatistics



class BotProfile:
    def __init__(self, name, bot_type, config, reward_config, statistics, bot_specific_data):
        """
        Initialize the BotProfile with the provided parameters.

        :param name: The name of the bot profile.
        :param bot_type: The type of the bot.
        :param config: The configuration object for the bot.
        :param reward_config: The reward configuration object for the bot.
        :param statistics: The statistics object tracking the bot's performance.
        :param bot_specific_data: Additional data specific to the bot.
        """
        self.name = name
        self.bot_type = bot_type
        self.config = config
        self.reward_config = reward_config
        self.statistics = statistics
        self.bot_specific_data = bot_specific_data

    def to_dict(self):
        """
        Convert the profile to a dictionary.

        :return: A dictionary representation of the profile.
        """
        return {
            "name": self.name,
            "bot_type": self.bot_type,
            "config": self.config.__dict__,
            "reward_config": self.reward_config.__dict__,
            "statistics": self.statistics.__dict__,
            "bot_specific_data": self.bot_specific_data

        }
    
    @staticmethod
    def from_dict(data):
        """
        Create a BotProfile instance from a dictionary.

        :param data: A dictionary containing the profile data.
        :return: A BotProfile instance.
        """        
        config_mapping = {
            'QLearningBot': QLearningConfig,
            # Add other bot types and their config classes here
        }
        config_class = config_mapping[data['bot_type']]#globals()[data['bot_type'] + "Config"]
        config = config_class(**data['config'])
        statistics = data['statistics']
        bot_specific_data = data['bot_specific_data']


        reward_config = data['reward_config']
        if isinstance(reward_config, dict):
            reward_config = RewardConfig(**reward_config)
        
        if isinstance(statistics, dict):
            statistics = BotStatistics()
            statistics.__dict__.update(data['statistics'])

        return BotProfile(
            name=data['name'],
            bot_type=data['bot_type'],
            config=config,
            reward_config=reward_config,
            statistics=statistics,
            bot_specific_data=bot_specific_data
        )

class ProfileManager:
    def __init__(self, profile_directory):
        """
        Initialize the ProfileManager with a directory for storing profiles.

        :param profile_directory: The directory where profiles are stored.
        """
        self.profile_directory = profile_directory

    def save_profile(self, profile):
        """
        Save a profile to a pickle file and create necessary files.

        :param profile: The BotProfile instance to save.
        """
        profile_dir = f"{self.profile_directory}/{profile.name}"
        os.makedirs(profile_dir, exist_ok=True)
        filename = f"{profile_dir}/profile.pkl"
        
        with open(filename, 'wb') as f:
            pickle.dump(profile.to_dict(), f)

        self._create_empty_file(os.path.join(profile_dir, "q_table.pkl"))
        self._create_empty_file(os.path.join(profile_dir, "SimulationRewards.txt"))
        self._create_empty_file(os.path.join(profile_dir, "HeatmapData.txt"))


    def load_profile(self, profile_name):
        """
        Load a profile from a pickle file.

        :param profile_name: The name of the profile to load.
        :return: A BotProfile instance.
        """
        profile_dir = f"{self.profile_directory}/{profile_name}"
        filename = f"{profile_dir}/profile.pkl"

        with open(filename, 'rb') as f:
            data = pickle.load(f)
        return BotProfile.from_dict(data)
    
    def list_profiles(self):
        """
        List all available profiles.

        :return: A list of profile names.
        """
        return [d for d in os.listdir(self.profile_directory) if os.path.isdir(os.path.join(self.profile_directory, d))]

    @staticmethod
    def _create_empty_file(filepath):
        """
        Create an empty file if it doesn't exist.

        :param filepath: The path to the file to create.
        """
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                f.write("")  # Write an empty string to create the file
