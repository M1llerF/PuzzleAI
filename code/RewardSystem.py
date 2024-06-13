
class RewardConfig:
    def __init__(self, **kwargs):
        self.goal_reward = kwargs.get('goal_reward', 1000)
        self.wall_penalty = kwargs.get('wall_penalty', -100)
        self.revisit_penalty_optimal = kwargs.get('revisit_penalty_optimal', -10)
        self.revisit_penalty_non_optimal = kwargs.get('revisit_penalty_non_optimal', -15)
        self.step_penalty = kwargs.get('step_penalty', -1)
        self.goal_in_sight_reward = kwargs.get('goal_in_sight_reward', 50)
        self.reward_modifiers = kwargs.get('reward_modifiers', {
            'goal_reached': '1000 * (optimal_length // 10)',
            'hit_wall': '-100 * (optimal_length // 10)',
            'revisit_optimal_path': '-10 * (optimal_length // 10)',
            'revisit_non_optimal_path': '-15 * (optimal_length // 10)',
            'move_in_optimal_path': '5 * (optimal_length // 10)',
            'see_goal_new_location': '50',
            'see_goal_revisit': '5',
            'per_move_penalty': '-1 * (optimal_length // 100)'
        })

    def customize_reward_modifiers(self):
        while True:
            print("Current reward modifiers:")
            for key, value in self.reward_modifiers.items():
                print(f"{key}: {value}")
            action = input("Do you want to add, remove, or modify a reward? (add/remove/modify/exit): ").strip().lower()
            if action == "add":
                self.add_reward_modifier()
            elif action == "remove":
                self.remove_reward_modifier()
            elif action == "modify":
                self.modify_reward_modifier()
            elif action == "exit":
                break
            else:
                print("Invalid action. Please enter add, remove, modify, or exit.")

    def add_reward_modifier(self):
        key = input("Enter the reward identifier (e.g., 'new_reward'): ").strip()
        value = input(f"Enter the reward formula (e.g., '500 * (optimal_length // 10)'): ").strip()
        if key and value:
            self.reward_modifiers[key] = value
        else:
            print("Invalid input. Reward not added.")

    def remove_reward_modifier(self):
        key = input("Enter the reward identifier to remove: ").strip()
        if key in self.reward_modifiers:
            self.reward_modifiers[key] = '0'
        else:
            print("Invalid identifier. Reward not removed.")

    def modify_reward_modifier(self):
        key = input("Enter the reward identifier to modify: ").strip()
        if key in self.reward_modifiers:
            value = input(f"Enter the new reward formula (current: {self.reward_modifiers[key]}): ").strip()
            if value:
                self.reward_modifiers[key] = value
        else:
            print("Invalid identifier. Reward not modified.")

    def get_modifier(self, action):
        return self.reward_modifiers.get(action, '0')  # Default to no modifier
    
    def test_print(self, printStatement):
        print("Reward Config Test Print: ", printStatement)

class RewardSystem:
    def __init__(self, maze, reward_config):
        self.maze = maze
        self.reward_config = reward_config
        self.cumulative_reward = 0
        self.times_hit_wall = 0
        self.times_revisited_square = 0
        self.non_repeating_steps_taken = 0
    
    def evaluate_expression(self, expression, **kwargs):
        try:
            return eval(expression, {}, kwargs)
        except Exception as e:
            print(f"Error evaluating expression '{expression}': {e}")
            return 0

    def get_reward(self, new_position, optimal_path, optimal_length, visited_positions):
        """Calculate the reward for moving to a new position."""
        reward = 0

        context = {
            'optimal_length': optimal_length,
            'visited_positions': visited_positions,
            'optimal_path': optimal_path,
            'new_position': new_position
        }

        for key, expr in self.reward_config.reward_modifiers.items():
            if key == 'goal_reached' and new_position == self.maze.end:
                reward += self.evaluate_expression(expr, **context)
            elif key == 'hit_wall' and not self.maze.is_valid_position(*new_position):
                reward += self.evaluate_expression(expr, **context)
            elif key == 'revisit_optimal_path' and new_position in visited_positions and new_position in optimal_path:
                reward += self.evaluate_expression(expr, **context)
            elif key == 'revisit_non_optimal_path' and new_position in visited_positions and new_position not in optimal_path:
                reward += self.evaluate_expression(expr, **context)
            elif key == 'move_in_optimal_path' and new_position in optimal_path:
                reward += self.evaluate_expression(expr, **context)
            elif key == 'see_goal_new_location' and self.is_goal_in_sight(new_position) and new_position not in visited_positions:
                reward += self.evaluate_expression(expr, **context)
            elif key == 'see_goal_revisit' and self.is_goal_in_sight(new_position) and new_position in visited_positions:
                reward += self.evaluate_expression(expr, **context)
            elif key == 'per_move_penalty':
                reward += self.evaluate_expression(expr, **context)
        
        #print(f"New Position: {new_position}, Total Reward: {reward}")  # Detailed debug statement
        return reward

    #? Should be in tools
    def is_goal_in_sight(self, position):
        """Check if the goal is in sight from the current position."""
        return self.maze.end in [(position[0] + dx, position[1] + dy) 
                                 for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]

    def update_rewards(self, reward):
        """Update cumulative rewards and other statistics."""
        self.cumulative_reward += reward
        if reward == self.evaluate_expression(self.reward_config.get_modifier('hit_wall')):
            self.times_hit_wall += 1
        elif reward == self.evaluate_expression(self.reward_config.get_modifier('revisit_non_optimal_path')):
            self.times_revisited_square += 1
        else:
            self.non_repeating_steps_taken += 1

    def reset_rewards(self):
        """Reset rewards and other statistics at the start of each episode."""
        self.cumulative_reward = 0
        self.times_hit_wall = 0
        self.times_revisited_square = 0
        self.non_repeating_steps_taken = 0
