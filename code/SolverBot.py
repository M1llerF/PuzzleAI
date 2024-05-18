import pickle
import numpy as np
from Pathfinding import Pathfinding
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
        self.cumulative_reward_for_debugging = 0
        self.times_bot_hit_wall = 0
        self.times_bot_revisited_squares = 0
        self.non_repeating_steps_taken = 0
        self.exploration_rate = 0
        self.optimal_path = Pathfinding.a_star_search(maze, maze.start, maze.end)
        self.optimal_length = len(self.optimal_path)

        #self.last_action = -1  # Initialize with no last action

    def pos_to_state(self, position):
        """ Convert position to a state index for simplicity in smaller mazes"""
        return position[0] * self.maze.width + position[1]
    
    def calculate_state(self):
        position_index = self.pos_to_state(self.position)
        wall_distances = self.detect_walls()
        visited = self.visited_positions.get(position_index, 0)
        distance_to_goal = np.linalg.norm(np.array(self.position) - np.array(self.maze.end))
        return (position_index, tuple(wall_distances.values()), visited, distance_to_goal)
    
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
        optimal_length = self.optimal_length
        """ Calculate the reward for moving to a new position."""
        maze_size = self.maze.width * self.maze.height
        #print("Maze size:", maze_size)
        
        if new_position == self.maze.end:
            # Reward for reaching the goal, scaled by optimal path size
            self.cumulative_reward_for_debugging += 1000
            return 1000 + optimal_length # Was + maze_size
        if not self.maze.is_valid_position(*new_position):
            # Penalty for hitting a wall, scaled by optimal path size
            self.cumulative_reward_for_debugging += -100
            self.times_bot_hit_wall += 1
            return -100 * (optimal_length // 10)
        if new_position in self.visited_positions:
            # Penalty for revisiting a position, scaled by optimal path size
            self.cumulative_reward_for_debugging += -10
            self.times_bot_revisited_squares += 1
            return -10 * (optimal_length // 10)
        if new_position not in self.optimal_path:
            # Penalty for moving away from the optimal path, scaled by optimal path size
            return -20 * (optimal_length // 10)

        # Small penalty for each move, scaled by maze size
        self.cumulative_reward_for_debugging += -1
        self.non_repeating_steps_taken += 1
        return -1 * (optimal_length // 100)

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
        
        exploration_rate = max(0.1, 1.0 - 0.001 * self.total_steps)
        if np.random.rand() < max(0.1, 0.1 - 0.001 * self.total_steps):
            return np.random.randint(self.num_actions)
        return np.argmax(self.q_table[self.state])

    def calculate_next_position(self, action):
        """Calculate the next position based on the current action."""
        direction_map = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}
        direction = direction_map[action]
        return (self.position[0] + direction[0], self.position[1] + direction[1])

    def run_episode(self):
        """Run one episode of the bot solving the maze."""
        #self.maze.display_with_bot(self.position)  # Initial display
        self.cumulative_reward_for_debugging = 0  # Reset cumulative reward at the start of each episode
        self.times_hit_wall = 0
        self.times_revisited_square = 0
        self.non_repeated_steps = 0
        step_limit = 1000  # Define a reasonable step limit
        while self.position != self.maze.end:
            action = self.choose_action()
            new_position = self.calculate_next_position(action)
            self.total_steps = self.times_bot_revisited_squares + self.non_repeating_steps_taken
            if not self.maze.is_valid_position(new_position[0], new_position[1]):
                #print("Invalid move attempted.")
                continue
            reward = self.get_reward(new_position)
            if(self.total_steps > step_limit):
                reward -= 1000
                self.cumulative_reward_for_debugging += reward # Include penalty
                break
            
            #self.cumulative_reward_for_debugging += reward
            self.visited_positions[self.position] = self.visited_positions.get(self.position, 0) + 1
            new_state = self.calculate_state()
            self.update_q_value(action, reward, new_state)
            self.position = new_position
            self.state = new_state

            #self.maze.display_with_bot(self.position)
        if(self.total_steps > step_limit):
            print("Resetting Bot")
            self.total_steps = 0
            SolverBot.reset_bot(self)
        else:
            print("Saving Q-table. Total steps: ", self.total_steps, "Reward: ", self.cumulative_reward_for_debugging)
            # For debugging:
            #print("Times Bot Hit Wall: ", self.times_bot_hit_wall, "| Times Bot revisited a square: ", self.times_bot_revisited_squares, "| Amount of non-repeated steps taken: ", self.non_repeating_steps_taken)
            self.save_q_table()
        #print(self.total_steps, "steps taken to reach the goal. Reward is", self.cumulative_reward_for_debugging)
        #print("Episode completed. Q-table saved.")

        with open('rewards.txt', 'a') as f:
            f.write(f"{self.cumulative_reward_for_debugging}\n")

    def save_q_table(self):
        # Adapt this method to handle dictionary saving if necessary
        with open('code/NonCodeFiles/q_table.pkl', 'wb') as f:
            pickle.dump(self.q_table, f)
    
    def load_q_table(self):
        try:
            with open('code/NonCodeFiles/q_table.pkl', 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}

    def reset_bot(self):
        """Reset the bot's position and state."""
        self.position = self.maze.start
        self.state = self.calculate_state()
        self.visited_positions.clear()
        self.cumulative_reward_for_debugging = 0
        self.total_steps = 0
        self.times_bot_hit_wall = 0
        self.times_bot_revisited_squares = 0
        self.non_repeating_steps_taken = 0