
from typing import Any, Dict, Tuple
from BotTools import BotTools

from typing import Dict

class RewardConfig:
    def __init__(self, **kwargs):
        """
        Initialize the RewardConfig with default values or provided keyword arguments.
        """
        self.goal_reward: int = kwargs.get('goal_reward', 1000)
        self.wall_penalty: int = kwargs.get('wall_penalty', -100)
        self.revisit_penalty_optimal: int = kwargs.get('revisit_penalty_optimal', -10)
        self.revisit_penalty_non_optimal: int = kwargs.get('revisit_penalty_non_optimal', -15)
        self.step_penalty: int = kwargs.get('step_penalty', -1)
        self.goal_in_sight_reward: int = kwargs.get('goal_in_sight_reward', 50)
        self.reward_modifiers: Dict[str, str] = kwargs.get('reward_modifiers', {
            'goal_reached': '1000',
            'hit_wall': '-100',
            'revisit_optimal_path': '-10',
            'revisit_non_optimal_path': '-15',
            'move_in_optimal_path': '5',
            'see_goal_new_location': '50',
            'see_goal_revisit': '5',
            'per_move_penalty': '-1'
        })

    def update_from_dict(self, config_dict):
        """
        Update the attributes of RewardConfig from a dictionary.
        """
        for key, value in config_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
                # Also update the corresponding reward modifier if applicable
                if key in self.reward_modifiers:
                    self.reward_modifiers[key] = str(value)
class RewardSystem:
    def __init__(self, maze, reward_config):
        self.maze = maze
        self.reward_config = reward_config
        self.cumulative_reward = 0
        self.times_hit_wall = 0
        self.times_revisited_square = 0
        self.non_repeating_steps_taken = 0
    
    def evaluate_expression(self, expression: str, **kwargs: Any) -> int:
        """
        Safely evaluate a mathematical expression with the given context.
        
        :param expression: The mathematical expression to evaluate.
        :param kwargs: The context for the expression.
        :return: The result of the evaluation.
        """
        try:
            return eval(expression, {}, kwargs)
        except Exception as e:
            print(f"Error evaluating expression '{expression}': {e}")
            return 0

    def get_reward(self, new_position: Tuple[int, int], optimal_path: list, optimal_length: int, visited_positions: Dict[Tuple[int, int], int]) -> int:
        """
        Calculate the reward for moving to a new position.
        
        :param new_position: The new position of the bot.
        :param optimal_path: The optimal path to the goal.
        :param optimal_length: The length of the optimal path.
        :param visited_positions: The dictionary of visited positions.
        :return: The calculated reward.
        """
        reward = 0

        context = {
            'optimal_length': optimal_length,
            'visited_positions': visited_positions,
            'optimal_path': optimal_path,
            'new_position': new_position
        }

        bot_tools = BotTools(self.maze)
        optimal_length = bot_tools.get_optimal_path_info(self.maze.start, self.maze.end, 'length')
        for key, expr in self.reward_config.reward_modifiers.items():
            multiplied_expr = str(int(expr) * optimal_length/100)

            if key == 'goal_reached' and new_position == self.maze.end:
                reward += self.evaluate_expression(multiplied_expr, **context)
            elif key == 'hit_wall' and not self.maze.is_valid_position(None, *new_position):
                reward += self.evaluate_expression(multiplied_expr, **context)
            elif key == 'revisit_optimal_path' and new_position in visited_positions and new_position in optimal_path:
                reward += self.evaluate_expression(multiplied_expr, **context)
            elif key == 'revisit_non_optimal_path' and new_position in visited_positions and new_position not in optimal_path:
                reward += self.evaluate_expression(multiplied_expr, **context)
            elif key == 'move_in_optimal_path' and new_position in optimal_path:
                reward += self.evaluate_expression(multiplied_expr, **context)
            elif key == 'see_goal_new_location' and bot_tools.check_goal_in_sight(new_position) and new_position not in visited_positions:
                reward += self.evaluate_expression(multiplied_expr, **context)
            elif key == 'see_goal_revisit' and bot_tools.check_goal_in_sight(new_position) and new_position in visited_positions:
                reward += self.evaluate_expression(multiplied_expr, **context)
            elif key == 'per_move_penalty':
                reward += self.evaluate_expression(multiplied_expr, **context)
        
        return reward

    def update_rewards(self, reward: int) -> None:
        """
        Update cumulative rewards and other statistics.
        
        :param reward: The reward to update.
        """
        self.cumulative_reward += reward
        if reward == self.evaluate_expression(self.reward_config.get_modifier('hit_wall')):
            self.times_hit_wall += 1
        elif reward == self.evaluate_expression(self.reward_config.get_modifier('revisit_non_optimal_path')):
            self.times_revisited_square += 1
        else:
            self.non_repeating_steps_taken += 1

    def reset_rewards(self) -> None:
        """
        Reset rewards and other statistics at the start of each episode.
        """
        self.cumulative_reward = 0
        self.times_hit_wall = 0
        self.times_revisited_square = 0
        self.non_repeating_steps_taken = 0
