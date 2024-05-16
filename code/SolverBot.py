import os
import pickle
import numpy as np

class SolverBot:
    def __init__(self, maze, learning_rate=0.1, discount_factor=0.9):
        self.maze = maze
        self.lr = learning_rate
        self.gamma = discount_factor
        self.num_actions = 4
        self.visited_positions = {}
        self.q_table = {}
        self.position = maze.start
        self.state = self.calculate_state()
        self.total_steps = 0
        self.cumulative_reward = 0

        #self.last_action = -1  # Initialize with no last action

    def pos_to_state(self, position):
        """ Convert position to a state index for simplicity in smaller mazes"""
        return position[0] * self.maze.width + position[1]
    
    def calculate_state(self):
        position_index = self.pos_to_state(self.position)
        wall_distances = self.detect_walls()
        visited = self.visited_positions.get(position_index, 0)
        return (position_index, tuple(wall_distances.values()), visited)
    
    def detect_walls(self):
        directions = {
            'Up': (-1, 0),
            'Down': (1, 0),
            'Left': (0, -1),
            'Right': (0, 1),
        }
        wall_distances = {}
        for direction, (dx, dy) in directions.items():
            distance = 0
            current_position = self.position
            # Check boundaries before moving in the direction
            while True:
                next_position = (current_position[0] + dx, current_position[1] + dy)
                # Make sure next_position is within the maze boundaries
                if 0 <= next_position[0] < self.maze.height and 0 <= next_position[1] < self.maze.width:
                    if self.maze.is_valid_position(next_position[0], next_position[1]):
                        current_position = next_position
                        distance += 1
                    else:
                        break  # Hit a wall or boundary, break the loop
                else:
                    break  # Out of bounds, break the loop
            wall_distances[direction] = distance
        return wall_distances

    def get_reward(self, new_position):
        """ Calculate the reward for moving to a new position."""
        if new_position == self.maze.end:
            return 1000
        if not self.maze.is_valid_position(*new_position):
            return -10
        if new_position in self.visited_positions:
            return -5
        return -1

    def update_q_value(self, action, reward, new_state):
        if self.state not in self.q_table:
            self.q_table[self.state] = np.zeros(self.num_actions)
        if new_state not in self.q_table:
            self.q_table[new_state] = np.zeros(self.num_actions)

        old_value = self.q_table[self.state][action]
        future_optimal_value = np.max(self.q_table[new_state])
        new_value = old_value + self.lr * (reward + self.gamma * future_optimal_value - old_value)
        self.q_table[self.state][action] = new_value
    
    def choose_action(self):
        if self.state not in self.q_table:
            self.q_table[self.state] = np.zeros(self.num_actions)
        
        if np.random.rand() < max(0.01, 0.1 - 0.001 * self.total_steps):
            return np.random.randint(self.num_actions)
        return np.argmax(self.q_table[self.state])

    # def choose_action(self):
    #     """Choose the next action to take based on the current state and Q-table"""
    #     self.total_steps += 1
    #     if np.random.rand() < 0.1:  # Increased exploration temporarily
    #         action = np.random.randint(self.num_actions)
    #     else:
    #         current_q_values = self.q_table[self.state]
    #         adjusted_q_values = current_q_values - 0.01 * self.visited_positions.get(self.position, 0)
    #         action = np.argmax(adjusted_q_values)
    #     return action
    
    def calculate_next_position(self, action):
        """Calculate the next position based on the current action."""
        direction_map = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}
        direction = direction_map[action]
        return (self.position[0] + direction[0], self.position[1] + direction[1])

    def run_episode(self):
        """Run one episode of the bot solving the maze."""
        #self.maze.display_with_bot(self.position)  # Initial display
        self.cumulative_reward = 0
        while self.position != self.maze.end:
            action = self.choose_action()
            new_position = self.calculate_next_position(action)
            if not self.maze.is_valid_position(new_position[0], new_position[1]):
                #print("Invalid move attempted.")
                continue
            reward = self.get_reward(new_position)
            self.cumulative_reward += reward
            self.visited_positions[self.position] = self.visited_positions.get(self.position, 0) + 1
            new_state = self.calculate_state()
            self.update_q_value(action, reward, new_state)
            self.position = new_position
            self.state = new_state

            #self.maze.display_with_bot(self.position)
        
        self.save_q_table()
        print(self.total_steps, "steps taken to reach the goal. Reward is", self.cumulative_reward)
        print("Episode completed. Q-table saved.")

    def save_q_table(self):
        # Adapt this method to handle dictionary saving if necessary
        with open('q_table.pkl', 'wb') as f:
            pickle.dump(self.q_table, f)
    
    def load_q_table(self):
        try:
            with open('q_table.pkl', 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}

    def reset_bot(self):
        """Reset the bot's position and state."""
        self.position = self.maze.start
        self.state = self.calculate_state()
        self.visited_positions.clear()
