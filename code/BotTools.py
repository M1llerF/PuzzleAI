from Pathfinding import Pathfinding
import numpy as np

class BotToolsConfig:
    def __init__(self):
        self.tools = {
            'optimal_path': 'Pathfinding.a_star_search(maze, maze.start, maze.end)',
            'optimal_length': 'len(Pathfinding.a_star_search(maze, maze.start, maze.end))',
            'detect_walls': 'self.detect_walls()'
        }

    def customize_tools(self):
        while True:
            print("Current tools configuration:")
            for key, value in self.tools.items():
                print(f"{key}: {value}")
            action = input("Do you want to add, remove, or modify a tool? (add/remove/modify/exit): ").strip().lower()
            if action == "add":
                self.add_tool()
            elif action == "remove":
                self.remove_tool()
            elif action == "modify":
                self.modify_tool()
            elif action == "exit":
                break
            else:
                print("Invalid action. Please enter add, remove, modify, or exit.")

    def add_tool(self):
        key = input("Enter the tool identifier (e.g., 'new_tool'): ").strip()
        value = input(f"Enter the tool function (e.g., 'self.new_tool_function()'): ").strip()
        if key and value:
            self.tools[key] = value
        else:
            print("Invalid input. Tool not added.")

    def remove_tool(self):
        key = input("Enter the tool identifier to remove: ").strip()
        if key in self.tools:
            self.tools[key] = '0'
        else:
            print("Invalid identifier. Tool not removed.")

    def modify_tool(self):
        key = input("Enter the tool identifier to modify: ").strip()
        if key in self.tools:
            value = input(f"Enter the new tool function (current: {self.tools[key]}): ").strip()
            if value:
                self.tools[key] = value
        else:
            print("Invalid identifier. Tool not modified.")

    def get_tool(self, tool_name):
        return self.tools.get(tool_name)


class BotTools:
    def __init__(self, maze, tools_config):
        self.maze = maze
        self.tools_config = tools_config
    
    def get_tool(self, tool_name):
        tool_code = self.tools_config.get_tool(tool_name)
        if tool_code:
            return eval(tool_code, {'self': self, 'maze': self.maze, 'Pathfinding': Pathfinding})
        return None
    
    """Class provides general tools to bots."""
    def check_goal_in_sight(self, position, wall_distances):
        """Check if the goal is in sight based on wall distances"""
        return any(self.maze.end in [(position[0] + dx * distance, position[1] + dy * distance)
                    for (dx, dy), distance in zip([(-1, 0), (1, 0), (0, -1), (0, 1)], wall_distances.values())])
    
    def pos_to_state(self, position):
        """Convert position to a state index for simplicity in smaller mazes"""
        #print("(From BotTools.py, BotTools, post_to_state(...)): position = (", position[0], ", ", position[1], ")")
        return (position[0], position[1])
    
    def is_valid_position(self, position):
        """Check if the position is valid in the maze"""
        return self.maze.is_valid_position(position[0], position[1])

    def detect_walls(self, position):
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
            current_position = position
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
    
    def get_distance_to_goal(self, position):
        """Get the distance to the goal"""
        return np.linalg.norm(np.array(position) - np.array(self.maze.end))
    
    def calculate_next_position(self, position, action):
        """Calculate the next position based on the current action"""
        direction_map = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}
        direction = direction_map[action]
        return (position[0] + direction[0], position[1] + direction[1])
    
    def get_optimal_path_info(self, start, end, output='path'):
        """Get optimal path or length from start to end based on the output parameter"""
        optimal_path = Pathfinding.a_star_search(self.maze, start, end)
        optimal_length = len(optimal_path)
        if output == 'path':
            return optimal_path
        elif output == 'length':
            return optimal_length
        else:
            raise ValueError("Output parameter must be 'path' or 'length'")
        