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
    def check_goal_in_sight(self, position, max_distance):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            for distance in range(1, max_distance + 1):
                new_position = (position[0] + dx * distance, position[1] + dy * distance)
                if self.maze.is_valid_position(new_position[0], new_position[1]):
                    if new_position == self.maze.end:
                        return 1 # True
                else:
                    break
        return 0 # False
    
    def pos_to_state(self, position):
        """Convert position to a state index for simplicity in smaller mazes"""
        return (position[0], position[1])
    
    def is_valid_position(self, position):
        """Check if the position is valid in the maze"""
        return self.maze.is_valid_position(position[0], position[1])


    def detect_walls(self, position):
        """Detect the distance to walls in all directions and check for the goal direction"""
        directions = {
            'Up': (-1, 0),
            'Down': (1, 0),
            'Left': (0, -1),
            'Right': (0, 1),
        }

        wall_distances_list = []  # Initialize distances for all directions
        goal_direction_list = []  # Initialize goal directions to 0 (False)

        maze_height = self.maze.height
        maze_width = self.maze.width
        maze_end = self.maze.end
        is_valid_position = self.maze.is_valid_position

        for direction, (dx, dy) in directions.items():
            distance = 0
            goal = 0
            current_position = position

            # Check boundaries before moving in the direction
            while True:
                next_position = (current_position[0] + dx, current_position[1] + dy)

                # Make sure next_position is within the maze boundaries
                if 0 <= next_position[0] < maze_height and 0 <= next_position[1] < maze_width:
                    if next_position == maze_end:
                        goal = 1  # Goal is in sight in this direction
                        break  # Goal is in sight, stop checking further
                    if is_valid_position(next_position[0], next_position[1]):
                        current_position = next_position
                        distance += 1
                    else:
                        break  # Hit a wall or boundary, break the loop
                else:
                    break  # Out of bounds, break the loop

            wall_distances_list.append(distance)
            goal_direction_list.append(goal)

        wall_distances = tuple(wall_distances_list)
        goal_direction = tuple(goal_direction_list)

        return wall_distances, goal_direction

    # def detect_walls(self, position):
    #     """Detect the distance to walls in all directions and check for the goal direction"""
    #     directions = {
    #         'Up': (-1, 0),
    #         'Down': (1, 0),
    #         'Left': (0, -1),
    #         'Right': (0, 1),
    #     }

    #     wall_distances = [0] * len(directions)  # Initialize distances for all directions
    #     goal_direction = [0] * len(directions)  # Initialize goal directions to 0 (False)
    #     direction_keys = list(directions.keys())

    #     for idx, (direction, (dx, dy)) in enumerate(directions.items()):
    #         distance = 0
    #         current_position = position

    #         # Check boundaries before moving in the direction
    #         while True:
    #             next_position = (current_position[0] + dx, current_position[1] + dy)

    #             # Make sure next_position is within the maze boundaries
    #             if 0 <= next_position[0] < self.maze.height and 0 <= next_position[1] < self.maze.width:
    #                 if next_position == self.maze.end:
    #                     goal_direction[idx] = 1  # Goal is in sight in this direction
    #                     break  # Goal is in sight, stop checking further
    #                 if self.maze.is_valid_position(next_position[0], next_position[1]):
    #                     current_position = next_position
    #                     distance += 1
    #                 else:
    #                     break  # Hit a wall or boundary, break the loop
    #             else:
    #                 break  # Out of bounds, break the loop

    #         wall_distances[idx] = distance

    #     return wall_distances, goal_direction
    
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
        