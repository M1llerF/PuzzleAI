import json
import os

class BotStatistics:
    def __init__(self):
        self.total_steps = 0
        self.cumulative_reward_for_debugging = 0
        self.times_hit_wall = 0
        self.times_revisited_squares = 0
        self.non_repeating_steps_taken = 0
        self.visited_positions = {}
        self.last_visited_positions = []

    def reset(self):
        """Reset statistics for a new episode."""
        self.total_steps = 0
        self.cumulative_reward_for_debugging = 0
        self.times_hit_wall = 0
        self.times_revisited_squares = 0
        self.non_repeating_steps_taken = 0
        self.visited_positions.clear()
        self.last_visited_positions.clear()
    
    def save_all_maze_data(self, profile_name, maze, heatmap_data, reward):
        """Save the latest, highest reward, and lowest reward mazes to a single file."""
        profile_dir = f"profiles/{profile_name}"
        os.makedirs(profile_dir, exist_ok=True)
        maze_data_path = f"{profile_dir}/mazes.json"

        try:
            with open(maze_data_path, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {
                "latest": {},
                "highest": {"reward": float('-inf')},
                "lowest": {"reward": float('inf')}
            }

        # Convert tuple keys to strings for JSON serialization
        heatmap_data_str_keys = {str(k): v for k, v in heatmap_data.items()}

        # Save latest maze
        data["latest"] = {
            "maze": maze.grid,
            "start": maze.get_start(),
            "end": maze.end,
            "heatmap_data": heatmap_data_str_keys,
            "reward": reward
        }

        # Save highest reward maze
        if reward > data["highest"]["reward"]:
            data["highest"] = {
                "maze": maze.grid,
                "start": maze.get_start(),
                "end": maze.end,
                "heatmap_data": heatmap_data_str_keys,
                "reward": reward
            }

        # Save lowest reward maze
        if reward < data["lowest"]["reward"]:
            data["lowest"] = {
                "maze": maze.grid,
                "start": maze.get_start(),
                "end": maze.end,
                "heatmap_data": heatmap_data_str_keys,
                "reward": reward
            }

        with open(maze_data_path, 'w') as f:
            json.dump(data, f, indent=4)

    def read_maze_and_heatmap(file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                for key in ['latest', 'highest', 'lowest']:
                    if "heatmap_data" in data[key]:
                        data[key]["heatmap_data"] = {eval(k): v for k, v in data[key]["heatmap_data"].items()}
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Maze data file {file_path} not found or is invalid.")
            return {
                "latest": {},
                "highest": {"reward": float('-inf')},
                "lowest": {"reward": float('inf')}
            }

    def load_all_maze_data(self, file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Maze data file {file_path} not found or is invalid.")
            return {
                "latest": {},
                "highest": {"reward": float('-inf')},
                "lowest": {"reward": float('inf')}
            }

        
    def update_visited_positions(self, position):
        """Update the visited positions."""
        self.visited_positions[position] = self.visited_positions.get(position, 0) + 1


    def get_visited_positions(self):
        """Get the visited positions."""
        return self.visited_positions

    def update_last_visited(self, position):
        """Update the last visited positions."""
        if len(self.last_visited_positions) >= 5:
            self.last_visited_positions.pop(0)
        if position not in self.last_visited_positions:
            self.last_visited_positions.append(position)

    def get_last_visited(self):
        """Get the last visited positions."""
        return self.last_visited_positions
