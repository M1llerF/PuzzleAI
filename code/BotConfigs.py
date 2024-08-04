# bot_configs.py

class QLearningConfig:
    def __init__(self, learning_rate=0.1, discount_factor=0.9):
        """
        Initialize Q-learning configuration with default learning rate and discount factor.
        """
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

    def customize(self):
        """
        Customize Q-learning parameters via user input.
        Prompts the user to enter new values for learning rate and discount factor.
        If the user input is invalid or left blank, the default values are used.
        """
        self.learning_rate = self._get_float_input("Enter learning rate (default 0.1): ", self.learning_rate)
        self.discount_factor = self._get_float_input("Enter discount factor (default 0.9): ", self.discount_factor)

    @staticmethod
    def _get_float_input(prompt, default):
        """
        Helper method to get a float input from the user.
        If the input is invalid or left blank, the default value is returned.

        :param prompt: The prompt message for input.
        :param default: The default value to return if input is invalid or blank.
        :return: The user input as a float or the default value.
        """
        try:
            return float(input(prompt) or default)
        except ValueError:
            print(f"Invalid input. Using default value {default}.")
            return default

# Define configurations for different bot types
bot_configs = {
    "QLearningBot": {
        "class": QLearningConfig,
        "params": {
            "Learning Rate": "learning_rate",
            "Discount Factor": "discount_factor"
        },
        "rewards": {
            'goal_reached': 1000,
            'hit_wall': -100,
            'revisit_optimal_path': -10,
            'revisit_non_optimal_path': -15,
            'move_in_optimal_path': 5,
            'see_goal_new_location': 50,
            'see_goal_revisit': 5,
            'per_move_penalty': -1
        }
    },
    # Additional bot types can be added here in the future
}
