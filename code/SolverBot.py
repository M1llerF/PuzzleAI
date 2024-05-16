import os
import numpy as np

class SolverBot:
    def __init__(self, maze, learning_rate=0.1, discount_factor=0.9):
        self.number_of_steps = 0
        self.maze = maze
        self.lr = learning_rate
        self.gamma = discount_factor
        self.num_actions = 4  # Up, Down, Left, Right
        self.q_table = self.load_q_table() #np.zeros((maze.height * maze.width, self.num_actions, self.num_actions))
        self.position = maze.start
        self.state = self.pos_to_state(self.position)
        self.last_action = -1  # Initialize with no last action
    
    def reset_bot(self):
        self.number_of_steps = 0
        self.position = self.maze.start
        self.state = self.pos_to_state(self.position)
        self.last_action = -1 # Reset last action to no action

    def pos_to_state(self, position):
        return position[0] * self.maze.width + position[1]
    
    def get_reward(self, new_position):
        if new_position == self.maze.end:
            return 1000
        elif not self.maze.is_valid_position(new_position[0], new_position[1]):
            return -5
        else:
            return -1
    
    def update_q_value(self, old_state, last_action, action, reward, new_state):
        if last_action == -1:
            return
        old_value = self.q_table[old_state, last_action, action]
        future_optimal_value = np.max(self.q_table[new_state])
        new_value = old_value + self.lr * (reward + self.gamma * future_optimal_value - old_value)
        self.q_table[old_state, last_action, action] = new_value

    def choose_action(self):
        self.number_of_steps += 1
        wall_distances = self.detect_walls()
        #print("Wall distances:", wall_distances)
        # adjusted_scores = self.q_table[self.state, self.last_action] + np.array([
        #     wall_distances['Up'],
        #     wall_distances['Down'],
        #     wall_distances['Left'],
        #     wall_distances['Right']
        # ])
        adjusted_scores = np.array([
            wall_distances['Up'],
            wall_distances['Down'],
            wall_distances['Left'],
            wall_distances['Right']
        ])
        
        if np.random.rand() < 0.1: # Exploration part
            action = np.random.randint(self.num_actions)
        else:
            action = np.argmax(adjusted_scores)

        #print("Chosen action:", action)
        return action
    def calculate_next_position(self, action):
        direction_map = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}
        direction = direction_map[action]
        new_position = (self.position[0] + direction[0], self.position[1] + direction[1])
        if 0 <= new_position[0] < self.maze.height and 0 <= new_position[1] < self.maze.width:
            if self.maze.is_valid_position(new_position[0], new_position[1]):
                return new_position
        return self.position  # Return current position if new position is not valid

    def run_episode(self):
        print("SolverBot starting at position:", self.position)
        self.position = self.maze.start
        self.state = self.pos_to_state(self.position)
        self.last_action = -1

        self.maze.display_with_bot(self.position)  # Initial display

        while self.position != self.maze.end:
            action = self.choose_action()
            #print(f"Chosen action: {action} from position {self.position}")
            new_position = self.calculate_next_position(action)
            #print(f"Moving to new position: {new_position}")

            if not self.maze.is_valid_position(new_position[0], new_position[1]):
                #print("Invalid move attempted.")
                continue

            reward = self.get_reward(new_position)
            new_state = self.pos_to_state(new_position)
            self.update_q_value(self.state, self.last_action, action, reward, new_state)

            self.position = new_position
            self.state = new_state
            self.last_action = action

            self.maze.display_with_bot(self.position)

            if self.position == self.maze.end:
                print("Goal reached!")
                print("Number of steps taken:", self.number_of_steps)
                break
        
        self.save_q_table()

    def detect_walls(self):
        directions = {
            'Up': (-1, 0),
            'Down': (1, 0),
            'Left': (0, -1),
            'Right': (0, 1),
        }
        wall_distances = {}
        for direction, (dx, dy) in directions.items():
            steps = 0
            current_position = self.position
            # Check boundaries before moving in the direction
            while True:
                next_position = (current_position[0] + dx, current_position[1] + dy)
                # Make sure next_position is within the maze boundaries
                if 0 <= next_position[0] < self.maze.height and 0 <= next_position[1] < self.maze.width:
                    if self.maze.is_valid_position(next_position[0], next_position[1]):
                        current_position = next_position
                        steps += 1
                    else:
                        break  # Hit a wall or boundary, break the loop
                else:
                    break  # Out of bounds, break the loop
            wall_distances[direction] = steps
        return wall_distances

    def save_q_table(self):
        try:
            np.save('code/q_table.npy', self.q_table)
            print("Q-table successfully saved.")
        except Exception as e:
            print("Failed to save Q-table:", e)
    
    def load_q_table(self):
        q_table_path = 'code/q_table.npy'
        try:
            if os.path.exists(q_table_path):
                return np.load(q_table_path, allow_pickle=True)  # Allowing pickle
            else:
                print("Q-table file not found, initializing new Q-table...")
        except Exception as e:
            print("Error loading Q-table:", e)
        
        return np.zeros((self.maze.height * self.maze.width, self.num_actions), dtype=np.float32)

    