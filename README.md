# Maze AI Experiment

This project is a Maze AI Experiment that serves as an introduction to AI and reinforcement learning. The application allows users to create, edit, and manage bot profiles that navigate through a maze using different AI strategies, such as Q-Learning. It includes features for training bots, visualizing their learning progress, and customizing their parameters and reward configurations.

## Getting Started

### Prerequisites

- Python 3.6+
- Required Python packages (see `requirements.txt`)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/maze-ai-experiment.git
   cd maze-ai-experiment
   ```

2. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**

   ```bash
   python main.py
   ```

## Features

- **Profile Management:** Create, edit, and delete profiles for different bots.
- **Bot Training:** Train bots with customizable parameters and reward configurations.
- **Visualizations:** Visualize the bot's learning progress, including reward graphs and heatmaps of visited maze areas.
- **Customization:** Adjust learning rate, discount factor, and rewards for various bot behaviors.

## Project Structure

- `MazeAIApp.py`: Main application file that handles the GUI and navigation.
- `BotProfile.py`: Defines the structure and management of bot profiles.
- `GameEnvironment.py`: Contains the environment setup and game loop logic.
- `QLearningBot.py`: Defines the Q-Learning bot and its configurations.
- `RewardSystem.py`: Manages the reward configurations for different bot actions.
- `VisualizationStrategy.py`: Strategies for visualizing different aspects of bot training.
- `BotConfigs.py`: Stores bot configuration mappings.
- `DisplayTools.py`: Utility functions for displaying profiles and other data.

## Customization

### Bot Configurations

The bot configurations, including learning rates, discount factors, and rewards, can be customized through the `Create/Edit Profile` interface. Each bot type has specific parameters and rewards that can be adjusted.

### Visualization

The `Visualization` frame provides various visual representations of the bot's learning process. This includes reward graphs, Q-table displays, and heatmaps showing areas visited by the bot.

## Usage

1. **Create a Profile:** Navigate to `Profile Management` and create a new profile.
2. **Set Parameters:** Customize the bot's parameters and reward configurations.
3. **Train the Bot:** Go to `Bot Training` and select the profile to start training.
4. **Visualize Progress:** Check the `Visualizations` section to see how the bot is learning.

## Notes

This project is the my first introduction to AI and serves as a learning experience in reinforcement learning and AI-driven applications.
