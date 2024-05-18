import numpy as np
import pickle
from SolverBot import BotStatistics

class QLearning:
    def __init__(self, learning_rate=0.1, discount_factor=0.9):
        self.lr = learning_rate
        self.gamma = discount_factor
        self.num_actions = 4
        self.visited_positions = {}
        self.q_table = {}
    
    def update_q_value(self, state, action, reward, new_state):
        """ Update Q-value for the given state-action pair."""
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.num_actions)
        if new_state not in self.q_table:
            self.q_table[new_state] = np.zeros(self.num_actions)

        old_value = self.q_table[state][action]
        future_optimal_value = np.max(self.q_table[new_state])
        new_value = old_value + self.lr * (reward + self.gamma * future_optimal_value - old_value)
        self.q_table[state][action] = new_value
    
    def choose_action(self, state):
        """ Choose an action based on the exploration-exploitation trade-off."""
        if state not in self.q_table:
            self.q_table[state] = np.zeros(self.num_actions) 
        exploration_rate = max(0.1, 1.0 - 0.001 * BotStatistics().non_repeating_steps_taken)
        if np.random.rand() < exploration_rate:
            return np.random.randint(self.num_actions)
        return np.argmax(self.q_table[state])
    
    def save_q_table(self):
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

class RewardSystem:
    def __init__(self, maze):
        self.maze = maze
        self.cumulative_reward = 0
        self.times_hit_wall = 0
        self.times_revisited_square = 0
        self.non_repeating_steps_taken = 0
    
    def get_reward(self, new_position, optimal_path, optimal_length, visited_positions):
        """Calculate the reward for moving to a new position."""
        if new_position == self.maze.end: # Reached the goal
            return 1000 + optimal_length
        if not self.maze.is_valid_position(*new_position): # Hit a wall
            return -100 * (optimal_length // 10)
        if new_position in visited_positions: # Revisited a position
            return -10 * (optimal_length // 10)
        if new_position not in optimal_path: # Moved away from the optimal path
            return -20 * (optimal_length // 10)
        return -1 * (optimal_length // 100) # Small penalty for each move
    
    def update_rewards(self, reward):
        """Update cumulative rewards and other statistics."""
        #* Class assumes reward values
        self.cumulative_reward += reward
        if reward == -100:
            self.times_hit_wall += 1
        elif reward == -10:
            self.times_revisited_square += 1
        else:
            self.non_repeating_steps_taken += 1

    def reset_rewards(self):
        """Reset rewards and other statistics at the start of each episode."""
        self.cumulative_reward = 0
        self.times_hit_wall = 0
        self.times_revisited_square = 0
        self.non_repeating_steps_taken = 0