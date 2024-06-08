from BotStatistics import BotStatistics
from BaseBot import BaseBot
from BotTools import BotTools
import pickle as pickle
import numpy as np

class QLearningConfig:
    def __init__(self, learning_rate=0.1, discount_factor=0.9):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

    def customize_q_learning(self):
        print("Customize your Q-learning settings:")
        self.learning_rate = float(input(f"Learning rate (current: {self.learning_rate}): ") or self.learning_rate)
        self.discount_factor = float(input(f"Discount factor (current: {self.discount_factor}): ") or self.discount_factor)


class QLearning:
    def __init__(self, q_learning_config):
        self.lr = q_learning_config.learning_rate
        self.gamma = q_learning_config.discount_factor
        self.num_actions = 4
        self.visited_positions = {}
        self.q_table = {}
        self.initial_exploration_rate = 1.0
        self.min_exploration_rate = 0.1
        self.exploration_decay_rate = 0.001
        self.q_learning_config = q_learning_config

    
    def update_q_value(self, state, action, reward, new_state):
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
    
    def choose_action(self, state):
        """ Choose an action based on the exploration-exploitation trade-off."""
        state_key = self.state_to_key(state)

        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.num_actions) 
        
        exploration_rate = max(self.min_exploration_rate, self.initial_exploration_rate - self.exploration_decay_rate * BotStatistics().non_repeating_steps_taken)
        if np.random.rand() < exploration_rate:
            return np.random.randint(self.num_actions)
        return np.argmax(self.q_table[state_key])
    
    def save_q_table(self):
        print("Saving Q-table...")
        """Save the Q-table to a file."""
        with open('code/NonCodeFiles/q_table.pkl', 'wb') as f:
            pickle.dump(self.q_table, f)
    
    def load_q_table(self):
        """Load the Q-table from a file."""
        try:
            with open('code/NonCodeFiles/q_table.pkl', 'rb') as f:
                self.q_table = pickle.load(f)
        except FileNotFoundError:
            return {}
    
    def reset(self):
        """Reset the Q-learning statistics"""
        self.visited_positions.clear()

    def state_to_key(self, state):
        """Convert the state to a hashable key for the Q-table."""
        position_index, wall_distances, visited, distance_to_goal, goal_direction = state
        return (position_index, wall_distances, visited, distance_to_goal, goal_direction)


class QLearningBot(BaseBot):
    def __init__(self, maze, config, reward_system, tool_config, statistics, profile_name):
        super().__init__(maze, config, reward_system, tool_config) # Debugging comment: This is passing the reward_system to BaseBot correctly
        # print(f"q_learning_config type (@ QLearningBot __init__): {type(q_learning_config)}")  # Debugging print
        # print(q_learning_config.learning_rate, q_learning_config.discount_factor)
        self.q_learning = QLearning(config) # Pass the config object
        self.tools = BotTools(maze, self.tool_config)
        self.statistics = statistics
        self.profile_name = profile_name
        self.total_reward = 0
        self.position = maze.get_start()
        self.state = self.calculate_state()
    
    def get_bot_specific_data(self):
        return {'q_table': self.q_learning.q_table}
    
    def initialize_specific_data(self, data):
        self.q_learning.q_table = data.get['q_table', {}]
from BotStatistics import BotStatistics
from BaseBot import BaseBot
from BotTools import BotTools
import pickle as pickle
import numpy as np

class QLearningConfig:
    def __init__(self, learning_rate=0.1, discount_factor=0.9):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

    def customize_q_learning(self):
        print("Customize your Q-learning settings:")
        self.learning_rate = float(input(f"Learning rate (current: {self.learning_rate}): ") or self.learning_rate)
        self.discount_factor = float(input(f"Discount factor (current: {self.discount_factor}): ") or self.discount_factor)


class QLearning:
    def __init__(self, q_learning_config):
        self.lr = q_learning_config.learning_rate
        self.gamma = q_learning_config.discount_factor
        self.num_actions = 4
        self.visited_positions = {}
        self.q_table = {}
        self.initial_exploration_rate = 1.0
        self.min_exploration_rate = 0.1
        self.exploration_decay_rate = 0.001
        self.q_learning_config = q_learning_config

    
    def update_q_value(self, state, action, reward, new_state):
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
    
    def choose_action(self, state):
        """ Choose an action based on the exploration-exploitation trade-off."""
        state_key = self.state_to_key(state)

        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.num_actions) 
        
        exploration_rate = max(self.min_exploration_rate, self.initial_exploration_rate - self.exploration_decay_rate * BotStatistics().non_repeating_steps_taken)
        if np.random.rand() < exploration_rate:
            return np.random.randint(self.num_actions)
        return np.argmax(self.q_table[state_key])
    
    def save_q_table(self):
        print("Saving Q-table...")
        """Save the Q-table to a file."""
        with open('code/NonCodeFiles/q_table.pkl', 'wb') as f:
            pickle.dump(self.q_table, f)
    
    def load_q_table(self):
        """Load the Q-table from a file."""
        try:
            with open('code/NonCodeFiles/q_table.pkl', 'rb') as f:
                self.q_table = pickle.load(f)
        except FileNotFoundError:
            return {}
    
    def reset(self):
        """Reset the Q-learning statistics"""
        self.visited_positions.clear()

    def state_to_key(self, state):
        """Convert the state to a hashable key for the Q-table."""
        position_index, wall_distances, visited, distance_to_goal, goal_direction = state
        return (position_index, wall_distances, visited, distance_to_goal, goal_direction)


class QLearningBot(BaseBot):
    def __init__(self, maze, config, reward_system, tool_config, statistics, profile_name):
        super().__init__(maze, config, reward_system, tool_config) # Debugging comment: This is passing the reward_system to BaseBot correctly
        # print(f"q_learning_config type (@ QLearningBot __init__): {type(q_learning_config)}")  # Debugging print
        # print(q_learning_config.learning_rate, q_learning_config.discount_factor)
        self.q_learning = QLearning(config) # Pass the config object
        self.tools = BotTools(maze, self.tool_config)
        self.statistics = statistics
        self.profile_name = profile_name
        self.total_reward = 0
        self.position = maze.get_start()
        self.state = self.calculate_state()
    
    def get_bot_specific_data(self):
        return {'q_table': self.q_learning.q_table}
    
    def initialize_specific_data(self, data):
        self.q_learning.q_table = data.get('q_table', {})


    def calculate_state(self):
        """Calculate the state based on the position"""
        position_index = self.tools.pos_to_state(self.position)
        wall_distances, goal_direction = self.tools.detect_walls(self.position)
        visited = self.q_learning.visited_positions.get(self.position, 0)
        distance_to_goal = self.tools.get_distance_to_goal(self.position)
        return (position_index, tuple(wall_distances.values()), visited, distance_to_goal, goal_direction)
    
    def run_episode(self):
        print("(From QLearningBot.py, QLearningBot(...), run_episodee(...)): Starting episode")
        #self.maze.display_with_bot(self.position)  # Initial display

        step_limit = 1000 * self.tools.get_optimal_path_info(self.maze.start, self.maze.end, output='length')
        steps = 0

        while self.position != self.maze.end:
            reward = 0
            action = self.q_learning.choose_action(self.state)
            new_position = self.tools.calculate_next_position(self.position, action)
            self.statistics.total_steps = self.statistics.times_revisited_squares + self.statistics.non_repeating_steps_taken

            #print(f"Step: {steps}, Position: {self.position}, Action: {action}, New Position: {new_position}")

            if not self.maze.is_valid_position(new_position[0], new_position[1]):
                # Could be messing up*
                reward += self.reward_system.get_reward(new_position, self.tools.get_optimal_path_info(self.position, self.maze.end), self.tools.get_optimal_path_info(self.position, self.maze.end, output='length'), self.statistics.get_visited_positions())
                new_state = self.calculate_state()
                self.q_learning.update_q_value(self.state, action, reward, new_state)
                self.total_reward += reward
                #print(f"Hit wall, Reward: {reward}, Total Reward: {self.total_reward}")
                continue

            self.statistics.update_last_visited(self.position)
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
            self.q_learning.visited_positions[self.position] = self.q_learning.visited_positions.get(self.position, 0) + 1

            self.position = new_position
            self.state = self.calculate_state()
            steps += 1

            if steps > step_limit:
                print("Potential infinite loop detected. Breaking out.")
                break
            #* Would be optimal for reward writing to be handled by BotStatistics instead.
            with open('code/NonCodeFiles/SimulationRewards.txt', 'a') as f:
                f.write(f"{self.total_reward}\n")
            
            if self.statistics.total_steps > step_limit:
                print("Step limit reached: ", self.statistics.total_steps, ". Resetting bot.")
                self.statistics.total_steps = 0
                self.reset_bot()
            
            #self.maze.display_with_bot(self.position) # Optional display

            
    def reset_bot(self):
        self.position = self.maze.start
        self.statistics.reset()
        self.total_reward = 0
        self.state = self.calculate_state()
        self.q_learning.reset()
    
    #* Would be optimal for this to be in BotStatisitcs.
    def save_heatmap_data(self):
        """Save the heatmap data to a file."""
        heatmap_data = self.statistics.get_visited_positions()

        existing_data = {}
        try:
            with open('code/NonCodeFiles/HeatmapData.txt', 'r') as f:
                for line in f:
                    x, y, count = map(int, line.strip().split(','))
                    existing_data[(x, y)] = count
        except FileNotFoundError:
            pass

        for position, count in heatmap_data.items():
            if position in existing_data:
                existing_data[position] += count
            else:
                existing_data[position] = count

        with open('code/NonCodeFiles/HeatmapData.txt', 'w') as f:
            for position, count in existing_data.items():
                f.write(f"{position[0]},{position[1]},{count}\n")


    def calculate_state(self):
        """Calculate the state based on the position"""
        position_index = self.tools.pos_to_state(self.position)
        wall_distances, goal_direction = self.tools.detect_walls(self.position)
        visited = self.q_learning.visited_positions.get(self.position, 0)
        distance_to_goal = self.tools.get_distance_to_goal(self.position)
        return (position_index, tuple(wall_distances.values()), visited, distance_to_goal, goal_direction)
    
    def run_episode(self):
        print("(From QLearningBot.py, QLearningBot(...), run_episodee(...)): Starting episode")
        #self.maze.display_with_bot(self.position)  # Initial display

        step_limit = 1000 * self.tools.get_optimal_path_info(self.maze.start, self.maze.end, output='length')
        steps = 0

        while self.position != self.maze.end:
            reward = 0
            action = self.q_learning.choose_action(self.state)
            new_position = self.tools.calculate_next_position(self.position, action)
            self.statistics.total_steps = self.statistics.times_revisited_squares + self.statistics.non_repeating_steps_taken

            #print(f"Step: {steps}, Position: {self.position}, Action: {action}, New Position: {new_position}")

            if not self.maze.is_valid_position(new_position[0], new_position[1]):
                # Could be messing up*
                reward += self.reward_system.get_reward(new_position, self.tools.get_optimal_path_info(self.position, self.maze.end), self.tools.get_optimal_path_info(self.position, self.maze.end, output='length'), self.statistics.get_visited_positions())
                new_state = self.calculate_state()
                self.q_learning.update_q_value(self.state, action, reward, new_state)
                self.total_reward += reward
                #print(f"Hit wall, Reward: {reward}, Total Reward: {self.total_reward}")
                continue

            self.statistics.update_last_visited(self.position)
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
            self.q_learning.visited_positions[self.position] = self.q_learning.visited_positions.get(self.position, 0) + 1

            self.position = new_position
            self.state = self.calculate_state()
            steps += 1

            if steps > step_limit:
                print("Potential infinite loop detected. Breaking out.")
                break
            #* Would be optimal for reward writing to be handled by BotStatistics instead.
            with open('code/NonCodeFiles/SimulationRewards.txt', 'a') as f:
                f.write(f"{self.total_reward}\n")
            
            if self.statistics.total_steps > step_limit:
                print("Step limit reached: ", self.statistics.total_steps, ". Resetting bot.")
                self.statistics.total_steps = 0
                self.reset_bot()
            
            #self.maze.display_with_bot(self.position) # Optional display

            
    def reset_bot(self):
        self.position = self.maze.start
        self.statistics.reset()
        self.total_reward = 0
        self.state = self.calculate_state()
        self.q_learning.reset()
    
    #* Would be optimal for this to be in BotStatisitcs.
    def save_heatmap_data(self):
        """Save the heatmap data to a file."""
        heatmap_data = self.statistics.get_visited_positions()

        existing_data = {}
        try:
            with open('code/NonCodeFiles/HeatmapData.txt', 'r') as f:
                for line in f:
                    x, y, count = map(int, line.strip().split(','))
                    existing_data[(x, y)] = count
        except FileNotFoundError:
            pass

        for position, count in heatmap_data.items():
            if position in existing_data:
                existing_data[position] += count
            else:
                existing_data[position] = count

        with open('code/NonCodeFiles/HeatmapData.txt', 'w') as f:
            for position, count in existing_data.items():
                f.write(f"{position[0]},{position[1]},{count}\n")

