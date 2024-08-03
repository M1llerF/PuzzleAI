from abc import ABC, abstractmethod
from typing import Any

from BotStatistics import BotStatistics

class VisualizationStrategy(ABC):
    @abstractmethod
    def visualize(self, frame: Any, bot: Any, profile_index: int):
        pass

class QLearningBotVisualizationStrategy(VisualizationStrategy):
    def visualize(self, frame, bot, profile_index):
        selected_profile = frame.profile_select.get()
        maze_data_path = f"profiles/{selected_profile}/mazes.json"
        
        # Ensure the maze data is loaded correctly
        bot_statistics = BotStatistics()
        maze_data = bot_statistics.load_all_maze_data(maze_data_path)

        # Check if maze_data contains the required keys
        if "latest" in maze_data and "highest" in maze_data and "lowest" in maze_data:
            # Update bot's maze_data
            bot.maze_data = maze_data
            
            # Display heatmaps
            frame.display_heatmap(frame.heatmap_canvas_latest, maze_data["latest"].get("maze"), maze_data["latest"].get("start"), maze_data["latest"].get("end"), maze_data["latest"].get("heatmap_data"))
            frame.display_heatmap(frame.heatmap_canvas_highest, maze_data["highest"].get("maze"), maze_data["highest"].get("start"), maze_data["highest"].get("end"), maze_data["highest"].get("heatmap_data"))
            frame.display_heatmap(frame.heatmap_canvas_lowest, maze_data["lowest"].get("maze"), maze_data["lowest"].get("start"), maze_data["lowest"].get("end"), maze_data["lowest"].get("heatmap_data"))
        else:
            print("Missing required keys in maze_data")

        frame.display_qtable(bot, profile_index)
        frame.display_statistics(bot, profile_index)
        frame.display_reward_graph(bot)


