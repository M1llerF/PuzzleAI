import numpy as np

class SolverBot:
    def __init__(self, maze, learning_rate=0.1, discount_factor=0.9):
        self.maze = maze
        self.lr = learning_rate
        self.gamma = discount_factor
        self.num_actions = 4  # Up, Down, Left, Right
        self.q_table = np.zeros((maze.height * maze.width, self.num_actions, self.num_actions))
        self.position = maze.start
        self.state = self.pos_to_state(self.position)
        self.last_action = -1  # Initialize with no last action
    
    def pos_to_state(self, position):
        """ Convert a (x, y) position to a state index. """
        return position[0] * self.maze.width + position[1]
    
    def get_reward(self, new_position):
        if new_position == self.maze.goal:
            return 100
        elif not self.maze.is_valid_position(new_position[0], new_position[1]):
            return -10 # Penalty for hitting a wall
        else:
            return -0.1 # Small penalty to encourage shortest path
    
    def update_q_value(self, old_state, last_action, action, reward, new_state):
        if last_action == -1: # Handle the first move where there is no last action
            return
        
        old_value = self.q_table[old_state, last_action, action]
        future_optimal_value = np.max(self.q_table[new_state])
        new_value = old_value + self.lr * (reward + self.gamma * future_optimal_value - old_value)
        self.q_table[old_state, last_action, action] = new_value

    def choose_action(self):
        wall_distances = self.detect_walls()  # Use wall distances in decision-making
        adjusted_scores = self.q_table[self.state, self.last_action] + np.array([wall_distances['Up'], wall_distances['Down'], wall_distances['Left'], wall_distances['Right']])
        
        if np.random.rand() < 0.1: # 10% of the time, choose a random action
            return np.random.randint(self.num_actions)
        return np.argmax(adjusted_scores)  # Exploit based on adjusted Q table scores
    
    def calculate_next_position(self, action):
        """ Calculate next position based on current position and action taken. """
        direction_map = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}
        direction = direction_map[action]
        return (self.position[0] + direction[0], self.position[1] + direction[1])

    def run_episode(self):
        self.position = self.maze.start
        self.state = self.pos_to_state(self.position)
        self.last_action = -1  # Reset last action at the start of each episode

        while self.position != self.maze.goal:
            action = self.choose_action()
            new_position = self.calculate_next_position(action)

            if not self.maze.is_valid_position(new_position[0], new_position[1]):
                continue  # Ignore this action if it leads to an invalid position

            reward = self.get_reward(new_position)
            new_state = self.pos_to_state(new_position)
            self.update_q_value(self.state, self.last_action, action, reward, new_state)

            self.last_action = action
            self.state = new_state
            self.position = new_position    
  

    # Bots Eyes
    def detect_walls(self):
        """ Detect walls around the current position and return them. """
        directions = {
            'Up': (-1, 0),
            'Down': (1, 0),
            'Left': (0, -1),
            'Right': (0, 1),
        }
        wall_distances = {}

        for direction in directions:
            steps = 0
            current_position = self.position
            while True:
                next_position = (current_position[0] + directions[direction][0], current_position[1] + directions[direction][1])
                if not self.maze.is_valid_position(next_position[0], next_position[1]):
                    break
                current_position = next_position
                steps += 1
            wall_distances[direction] = steps

        return wall_distances
