import json
import os
import pickle
from typing import Dict, Any, Tuple, Union


class BotStatistics:
    def __init__(self):
        """Initialize statistics and visited positions."""
        self.total_steps: int = 0
        self.times_hit_wall: int = 0
        self.times_revisited_squares: int = 0
        self.non_repeating_steps_taken: int = 0
        self.visited_positions: Dict[Tuple[int, int], int] = {}
        self.last_visited_positions: list[Tuple[int, int]] = []


    def reset(self):
        """Reset statistics for a new episode."""
        self.total_steps = 0
        self.times_hit_wall = 0
        self.times_revisited_squares = 0
        self.non_repeating_steps_taken = 0
        self.visited_positions.clear()
        self.last_visited_positions.clear()
    
    @staticmethod
    def _ensure_dir_exists(dir_path: str) -> None:
        """Ensure that the directory for a file exists, creating it if necessary."""
        os.makedirs(dir_path, exist_ok=True)
    
    def _get_file_path(self, profile_name: str, file_name: str, extension: str) -> str:
        """Contruct the file path for a given profile and file name."""
        profile_dir = f"profiles/{profile_name}"
        self._ensure_dir_exists(profile_dir)
        return f"{profile_dir}/{file_name}.{extension}"
    
    def _read_file(self, file_path: str, file_type: str = 'json') -> Union[Dict[str, Any], None]:
        """Read data from a file (JSON or Pickle)."""
        try:
            with open(file_path, 'r' if file_type == 'json' else 'rb') as f:
                return json.load(f) if file_type == 'json' else pickle.load(f)
        except (FileNotFoundError, json.JSONDecodeError, pickle.UnpicklingError):
            return None

    def _write_file(self, file_path: str, data: Any, file_type: str = 'json') -> None:
        """Write data to a file (JSON or Pickle)."""
        try:
            with open(file_path, 'w' if file_type == 'json' else 'wb') as f:
                json.dump(data, f, indent=4) if file_type == 'json' else pickle.dump(data, f)
        except (OSError, IOError) as e:
            print(f"Error writing to {file_type} file {file_path}: {e}")

    def get_json_data(self, profile_name: str, file_name: str) -> Dict[str, Any]:
        """Retrieve data from a JSON file for a given profile."""
        return self._read_file(self._get_file_path(profile_name, file_name, 'json')) or "No data found"

    def dump_json_data(self, profile_name: str, file_name: str, data: Dict[str, Any]) -> None:
        """Save data to a JSON file for a given profile."""
        self._write_file(self._get_file_path(profile_name, file_name, 'json'), data)

    def get_steps_from_heatmap(self, profile_name: str, heatmap_data: Dict[Tuple[int, int], int]) -> Tuple[int, int, int]:
        """Calculate total, repeated, and unique steps from heatmap data."""
        data = self.get_json_data(profile_name, "mazes")
        if data == "No data found":
            return 0, 0, 0

        heatmap_data = data["latest"]["heatmap_data"]

        # Number of different coordinates visited
        unique_steps = len(heatmap_data)
        total_steps = sum(heatmap_data.values())
        repeated_steps = total_steps - unique_steps

        return total_steps, repeated_steps, unique_steps

    def update_steps_in_profile(self, profile_name: str, heatmap_data: Dict[Tuple[int, int], int]) -> None:
        """Update the profile with steps information from heatmap data."""
        total_steps, repeated_steps, unique_steps = self.get_steps_from_heatmap(profile_name, heatmap_data)
        profile_data = self._read_file(self._get_file_path(profile_name, "profile", 'pkl'), 'pickle') or {}

        profile_data['non_repeating_steps_taken'] = profile_data.get('non_repeating_steps_taken', 0) + unique_steps
        profile_data['total_steps'] = profile_data.get('total_steps', 0) + total_steps
        profile_data['times_revisited_squares'] = profile_data.get('times_revisited_squares', 0) + repeated_steps

        self._write_file(self._get_file_path(profile_name, "profile", 'pkl'), profile_data, 'pickle')

    def update_times_hit_wall(self, profile_name, times_hit_wall=1):
        """Increment the count of times the bot has hit a wall in the profile data."""
        profile_data = self._read_file(self._get_file_path(profile_name, "profile", 'pkl'), 'pickle') or {}
        profile_data['times_hit_wall'] = profile_data.get('times_hit_wall', 0) + times_hit_wall
        self._write_file(self._get_file_path(profile_name, "profile", 'pkl'), profile_data, 'pickle')

    def save_all_maze_data(self, profile_name, maze, heatmap_data, reward):
        """Save the latest, highest reward, and lowest reward mazes to a JSON file."""
        data = self.get_json_data(profile_name, "mazes")
        if data == "No data found":
            data = {
                "latest": {},
                "highest": {"reward": float('-inf')},
                "lowest": {"reward": float('inf')}
            }

        heatmap_data_str_keys = {str(k): v for k, v in heatmap_data.items()}

        data["latest"] = {
            "maze": maze.grid,
            "start": maze.get_start(),
            "end": maze.end,
            "heatmap_data": heatmap_data_str_keys,
            "reward": reward
        }

        if reward > data["highest"]["reward"]:
            data["highest"] = {
                "maze": maze.grid,
                "start": maze.get_start(),
                "end": maze.end,
                "heatmap_data": heatmap_data_str_keys,
                "reward": reward
            }

        if reward < data["lowest"]["reward"]:
            data["lowest"] = {
                "maze": maze.grid,
                "start": maze.get_start(),
                "end": maze.end,
                "heatmap_data": heatmap_data_str_keys,
                "reward": reward
            }

        self.dump_json_data(profile_name, "mazes", data)

    def load_all_maze_data(self, file_path):
        data = self._read_file(file_path, 'json')
        if data:
            for key in ['latest', 'highest', 'lowest']:
                if "heatmap_data" in data[key]:
                    data[key]["heatmap_data"] = {eval(k): v for k, v in data[key]["heatmap_data"].items()}
        else:
            data = {
                "latest": {},
                "highest": {"reward": float('-inf')},
                "lowest": {"reward": float('inf')}
            }
        return data

    def update_visited_positions(self, position):
        """Update the count of times a position has been visited."""
        self.visited_positions[position] = self.visited_positions.get(position, 0) + 1

    def get_visited_positions(self):
        """Retrieve the dictionary of visited positions."""
        return self.visited_positions

    def update_last_visited(self, position):
        """Update the list of the last visited positions."""
        if len(self.last_visited_positions) >= 5:
            self.last_visited_positions.pop(0)
        if position not in self.last_visited_positions:
            self.last_visited_positions.append(position)

    def get_last_visited(self):
        """Retrieve the list of the last visited positions."""
        return self.last_visited_positions
