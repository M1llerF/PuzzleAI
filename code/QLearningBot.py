import os
import pickle
import hashlib
import tempfile
import numpy as np
from typing import Any, Dict, Tuple

from BotStatistics import BotStatistics
from BaseBot import BaseBot
from BotTools import BotTools

class QLearningConfig:
    def __init__(self, learning_rate: float = 0.1, discount_factor: float = 0.9):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

class QLearning:
    def __init__(self, q_learning_config: QLearningConfig):
        """Initialize Q-learning algorithm with the given configuration."""
        self.lr = q_learning_config.learning_rate
        self.gamma = q_learning_config.discount_factor
        self.num_actions = 4
        self.q_table: Dict[Any, np.ndarray] = {}
        self.initial_exploration_rate = 1.0
        self.min_exploration_rate = 0.1
        self.exploration_decay_rate = 0.001

    def update_q_value(self, state: Any, action: int, reward: float, new_state: Any) -> None:
        """ Update Q-value for the given state-action pair."""
        state_key = self.state_to_key(state)
        new_state_key = self.state_to_key(new_state)

        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.num_actions)
        if new_state_key not in self.q_table:
            self.q_table[new_state_key] = np.zeros(self.num_actions)

        old_value = self.q_table[state_key][action]
        future_optimal_value = np.max(self.q_table[new_state_key])
        new_value = old_value + self.lr * (reward + self.gamma * future_optimal_value - old_value)
        self.q_table[state_key][action] = new_value
    
    def choose_action(self, state: Any) -> int:
        """ Choose an action based on the exploration-exploitation trade-off."""
        state_key = self.state_to_key(state)

        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.num_actions) 
        
        exploration_rate = max(
            self.min_exploration_rate, self.initial_exploration_rate - self.exploration_decay_rate * BotStatistics().non_repeating_steps_taken
        )
        if np.random.rand() < exploration_rate:
            return np.random.randint(self.num_actions)
        return np.argmax(self.q_table[state_key])
    
    @staticmethod
    def get_file_checksum(file_path: str) -> str:
        """Calculate the checksum of a file."""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f: 
            for block in iter(lambda: f.read(4096), b""): 
                sha256.update(block)
        return sha256.hexdigest()
    
    def save_q_table(self, profile_name):
        """Save the Q-table to a file atomically."""
        profile_dir = f"profiles/{profile_name}"
        os.makedirs(profile_dir, exist_ok=True)
        q_table_path = f"{profile_dir}/q_table.pkl"

        with tempfile.NamedTemporaryFile(delete=False, dir=profile_dir) as tmp_file:
            pickle.dump(self.q_table, tmp_file)
            temp_name = tmp_file.name
        os.replace(temp_name, q_table_path)

        # Save the checksum ("fingerprint") of the Q-table file
        checksum = self.get_file_checksum(q_table_path)
        with open(f"{profile_dir}/q_table.checksum", 'w') as f:
            f.write(checksum)

    def load_q_table(self, profile_name: str) -> None:
        """Load the Q-table from a file."""
        profile_dir = f"profiles/{profile_name}"
        q_table_path = f"{profile_dir}/q_table.pkl"
        q_table_path_no_ext = f"{profile_dir}/q_table"
        try:
            # Check if the checksum file exists
            checksum_path = f"{q_table_path_no_ext}.checksum"
            if os.path.exists(checksum_path):
                with open(checksum_path, 'r') as f:
                    saved_checksum = f.read()
                
                current_checksum = self.get_file_checksum(q_table_path)
                if saved_checksum != current_checksum:
                    raise ValueError("File checksum does not match.")
            else:
                print("Checksum does not match or was not found at file not found at:", checksum_path)

            with open(q_table_path, 'rb') as f:
                self.q_table = pickle.load(f)
        except FileNotFoundError:
            print("FileNotFoundError: Q-table file not found.")
        except ValueError as ve:
            print("ValueError: ", ve)
        except EOFError:
            print("Q-table file is incomplete or corrupted.")

    @staticmethod
    def state_to_key(state: Any) -> Tuple:
        """Convert the state to a hashable key for the Q-table."""
        position_index, wall_distances, visited, distance_to_goal, goal_direction = state
        return position_index, wall_distances, visited, distance_to_goal, goal_direction


class QLearningBot(BaseBot):
    def __init__(self, maze, config, reward_system, statistics, profile_name):
        """
        Initialize the Q-learning bot.

        :param maze: The maze object.
        :param config: Q-learning configuration.
        :param reward_system: Reward system for evaluating actions.
        :param statistics: Instance of BotStatistics for tracking statistics.
        :param profile_name: Name of the profile for saving/loading data.
        """
        super().__init__(maze, statistics, config)
        self.q_learning = QLearning(config)
        self.tools = BotTools(maze)
        self.reward_system = reward_system
        self.profile_name = profile_name
        self.total_reward = 0
        self.position = maze.get_start()
        self.state = self.calculate_state()
        self.q_learning.load_q_table(profile_name)  # Load Q-table when initializing

        maze_data_path = f"profiles/{profile_name}/mazes.json"
        maze_data = self.statistics.load_all_maze_data(maze_data_path)

        self.highest_reward = maze_data["highest"].get("reward", float('-inf'))
        self.lowest_reward = maze_data["lowest"].get("reward", float('inf'))

    def get_bot_specific_data(self):
        """Retrieve bot-specific data."""
        return {'q_table': self.q_learning.q_table}
    
    def initialize_specific_data(self, data):
        """Initialize bot-specific data."""
        self.q_learning.q_table = data.get('q_table', {})
        self.q_learning.load_q_table(self.profile_name) # Load the Q-table from a file

    def calculate_state(self):
        """Calculate the state based on the position"""
        position_index = self.tools.pos_to_state(self.position)
        wall_distances, goal_direction = self.tools.detect_walls(self.position)
        visited = self.statistics.get_visited_positions()
        distance_to_goal = self.tools.get_distance_to_goal(self.position)
        return (position_index, wall_distances, tuple(visited), distance_to_goal, goal_direction)
    
    def run_episode(self):
        """Run a single episode of Q-learning."""
        step_limit = 1000 * self.tools.get_optimal_path_info(self.maze.start, self.maze.end, output='length')
        steps = 0
        times_hit_wall = 0

        while self.position != self.maze.end:
            reward = 0
            action = self.q_learning.choose_action(self.state)
            new_position = self.tools.calculate_next_position(self.position, action)
            self.statistics.total_steps = self.statistics.times_revisited_squares + self.statistics.non_repeating_steps_taken

            if not self.maze.is_valid_position(self.profile_name, new_position[0], new_position[1]):
                reward += self.reward_system.get_reward(new_position, self.tools.get_optimal_path_info(self.position, self.maze.end), self.tools.get_optimal_path_info(self.position, self.maze.end, output='length'), self.statistics.get_visited_positions())
                new_state = self.calculate_state()
                self.q_learning.update_q_value(self.state, action, reward, new_state)
                self.total_reward += reward
                times_hit_wall += 1
                continue

            self.statistics.update_last_visited(self.position)
            self.statistics.update_visited_positions(self.position)
            reward += self.reward_system.get_reward(new_position, self.tools.get_optimal_path_info(self.position, self.maze.end), self.tools.get_optimal_path_info(self.position, self.maze.end, output='length'), self.statistics.get_visited_positions())

            if new_position in self.statistics.get_visited_positions():
                self.statistics.times_revisited_squares += 1
            else:
                self.statistics.non_repeating_steps_taken += 1
            
            if self.statistics.total_steps > step_limit:
                print("Step limit reached: ", self.statistics.total_steps)
                reward += -1000
                new_state = self.calculate_state()
                self.q_learning.update_q_value(self.state, action, reward, new_state)
                self.total_reward += reward
                break

            self.total_reward += reward
            self.statistics.visited_positions[self.position] = self.statistics.visited_positions.get(self.position, 0) + 1
            new_state = self.calculate_state()
            self.q_learning.update_q_value(self.state, action, reward, new_state)


            self.position = new_position
            self.state = new_state
            steps += 1

            if steps > step_limit:
                print("Potential infinite loop detected. Breaking out.")
                break

            heatmap_data = self.statistics.get_visited_positions()
            
            profile_dir = f"profiles/{self.profile_name}"
            os.makedirs(profile_dir, exist_ok=True)
            simulation_rewards_path = f"{profile_dir}/SimulationRewards.txt"
            
            if self.statistics.total_steps > step_limit:
                print("Step limit reached: ", self.statistics.total_steps, ". Resetting bot.")
                self.statistics.total_steps = 0
                self.q_learning.save_q_table(self.profile_name)  # Save Q-table after each episode

                self.reset_bot()

        heatmap_data = self.statistics.get_visited_positions()
        self.statistics.save_all_maze_data(self.profile_name, self.maze, heatmap_data, self.total_reward)
        self.statistics.update_steps_in_profile(self.profile_name, heatmap_data)
        self.statistics.update_times_hit_wall(self.profile_name, times_hit_wall)
        with open(simulation_rewards_path, 'a') as f:
            f.write(f"{self.total_reward}\n")
        
        self.q_learning.save_q_table(self.profile_name)  # Save Q-table after each episode

    def reset_bot(self):
        """Reset the bot's position, statistics, and Q-learning data."""
        self.position = self.maze.start
        self.statistics.reset()
        self.total_reward = 0
        self.state = self.calculate_state()
