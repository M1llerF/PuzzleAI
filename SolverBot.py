import numpy as np
from Pathfinding import Pathfinding
class BotConfig:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, num_actions=4):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.num_actions = num_actions

class BotStatistics:
    def __init__(self):
        self.total_steps = 0
        self.cumulative_reward_for_debugging = 0
        self.times_hit_wall = 0
        self.times_revisited_squares = 0
        self.non_repeating_steps_taken = 0
        self.visited_positions = {}
        self.last_visited = {}
    
    def reset(self):
        """ Reset statistics for a new episode """
        print(self.visited_positions)
        self.total_steps = 0
        self.cumulative_reward_for_debugging = 0
        self.times_hit_wall = 0
        self.times_revisited_squares = 0
        self.non_repeating_steps_taken = 0
        self.visited_positions.clear()
        self.last_visited.clear()
    
    def update_visited_positions(self, position):
        """ Update the visited positions """
        self.visited_positions[position] = self.visited_positions.get(position, 0) + 1

    def get_visited_positions(self):
        """ Get the visited positions """
        return self.visited_positions
    
    def update_last_visited(self, position, current_step):
        """ Update the last visited steps for a position """
        if position not in self.last_visited:
            self.last_visited[position] = []
        self.last_visited[position].append(current_step)
        # Keep only the last 5 visits
        self.last_visited[position] = self.last_visited[position][-5:]

    def get_last_visited(self,position):
        """ Get the last visited positions """
        return self.last_visited.get(position, [])

class SolverBot:
    def __init__(self, maze, q_learning, reward_system, config):
        self.maze = maze
        self.q_learning = q_learning
        self.reward_system = reward_system
        self.config = config
        self.statistics = BotStatistics()
        self.total_reward = 0
        self.position = maze.start
        self.state = self.calculate_state()
        self.optimal_path = Pathfinding.a_star_search(maze, maze.start, maze.end)
        self.optimal_length = len(self.optimal_path)
        self.reset_bot()
    
    def check_goal_in_sight(self, wall_distances):
        """Check if the goal is in sight based on wall distances"""
        return any(self.maze.end in [(self.position[0] + dx * distance, self.position[1] + dy * distance)
                   for (dx, dy), distance in zip([(-1, 0), (1, 0), (0, -1), (0, 1)], wall_distances.values())])

    def pos_to_state(self, position):
        """Convert position to a state index for simplicity in smaller mazes"""
        return (position[0], position[1])
    
    def calculate_state(self):
        """Calculate the state representation based on the current position and layout"""
        position_index = self.pos_to_state(self.position)
        wall_distances, goal_direction = self.detect_walls()
        visited = self.q_learning.visited_positions.get(self.position, 0)
        distance_to_goal = np.linalg.norm(np.array(self.position) - np.array(self.maze.end))
        return (position_index, tuple(wall_distances.values()), visited, distance_to_goal, goal_direction)
    
    #! BOT KEEPS TRYING TO MOVE INTO WALLS
    def detect_walls(self):
        """Detect the distance to walls in all directions"""
        directions = {
            'Up': (-1, 0),
            'Down': (1, 0),
            'Left': (0, -1),
            'Right': (0, 1),
        }
        wall_distances = {}
        goal_direction = None
        for direction, (dx, dy) in directions.items():
            distance = 0
            current_position = self.position
            # Check boundaries before moving in the direction
            while True:
                next_position = (current_position[0] + dx, current_position[1] + dy)
                # Make sure next_position is within the maze boundaries
                if 0 <= next_position[0] < self.maze.height and 0 <= next_position[1] < self.maze.width:
                    if next_position == self.maze.end:
                            goal_direction = direction
                            break # Goal is in sight, stop checking further
                    if self.maze.is_valid_position(next_position[0], next_position[1]):
                        current_position = next_position
                        distance += 1
                    else:
                        break  # Hit a wall or boundary, break the loop
                else:
                    break  # Out of bounds, break the loop
            wall_distances[direction] = distance
        return wall_distances, goal_direction
    
    def calculate_next_position(self, action):
        """Calculate the next position based on the current action"""
        direction_map = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}
        direction = direction_map[action]
        #print(self.position[0] + direction[0], self.position[1] + direction[1])
        return (self.position[0] + direction[0], self.position[1] + direction[1])

    def run_episode(self):
        #print("Running episode...")
        """Run one episode of the bot solving the maze."""
        self.maze.display_with_bot(self.position)  # Initial display
        step_limit = 3000 * self.optimal_length  # Define a reasonable step limit

        while self.position != self.maze.end:
            reward = 0
            action = self.q_learning.choose_action(self.state)
            new_position = self.calculate_next_position(action)
            self.statistics.total_steps = self.statistics.times_revisited_squares + self.statistics.non_repeating_steps_taken
            current_step = self.statistics.total_steps
            # Update last visited for the current position with the current step count
            self.statistics.update_last_visited(self.position, current_step)
            #print(self.statistics.last_visited)

            if not self.maze.is_valid_position(new_position[0], new_position[1]):
                reward += -1000
                #print("Hit a wall!")
                self.statistics.times_hit_wall += 1
                new_state = self.calculate_state()
                self.q_learning.update_q_value(self.state, action, reward, new_state)
                self.total_reward += reward
                continue
            #print("Reward: ", reward)
            reward += self.reward_system.get_reward(new_position, self.optimal_path, self.optimal_length, self.statistics.get_visited_positions(), self.statistics.get_last_visited(self.position))

            #! Ugly:
            if(self.statistics.total_steps > step_limit):
                self.print("Step limit reached.")
                reward -= 1000
                self.total_reward += reward # Include penalty
                break
            
            self.total_reward += reward
            # print(f"Reward: {reward}")
            self.q_learning.visited_positions[self.position] = self.q_learning.visited_positions.get(self.position, 0) + 1
            self.statistics.update_visited_positions(self.position)
            new_state = self.calculate_state()
            self.q_learning.update_q_value(self.state, action, reward, new_state)

            self.position = new_position
            self.state = new_state
            self.maze.display_with_bot(self.position) # Optional display
        print("Episode Summary: ", self.statistics.total_steps, self.total_reward) 
        self.q_learning.save_q_table()
        self.save_heatmap_data()

        # ! Make this a optional feature
        with open('code/NonCodeFiles/SimulationRewards.txt', 'a') as f:
            f.write(f"{self.total_reward}\n")

        if self.statistics.total_steps > step_limit:
            self.statistics.total_steps = 0
            self.reset_bot()

    def reset_bot(self):
        """Reset the bot's position and state"""
        #print("Resetting bot...")
        self.position = self.maze.start
        self.statistics.reset()
        self.total_reward = 0
        self.state = self.calculate_state()
        self.q_learning.reset()

    def save_heatmap_data(self):
        """Save the heatmap data to a file."""
        #print("Saving heatmap data...")
        heatmap_data = self.statistics.get_visited_positions()
        
        # Read existing data
        existing_data = {}
        try:
            with open('code/NonCodeFiles/HeatmapData.txt', 'r') as f:
                for line in f:
                    x, y, count = map(int, line.strip().split(','))
                    existing_data[(x, y)] = count
        except FileNotFoundError:
            # If the file doesn't exist, we can skip reading existing data
            pass
        
        # Update existing data with new data
        for position, count in heatmap_data.items():
            if position in existing_data:
                existing_data[position] += count
            else:
                existing_data[position] = count
        
        # Write the combined data back to the file
        with open('code/NonCodeFiles/HeatmapData.txt', 'w') as f:
            for position, count in existing_data.items():
                f.write(f"{position[0]},{position[1]},{count}\n")
        
       # print(f"Heatmap data saved successfully.")
