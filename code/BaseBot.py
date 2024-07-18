class BaseBot:
    def __init__(self, maze, statistics, config=None):
        """
        Initialize the base bot.

        :param maze: The maze object that the bot will navigate.
        :param statistics: An instance of BotStatistics to track the bot's performance.
        :param config: Optional configuration for specific algorithms (e.g., Q-learning config).
        """
        self.maze = maze
        self.statistics = statistics
        self.config = config
    
    def reset(self):
        """Reset the bot's state and statistics. Should be implemented by subclasses."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    def calculate_state(self):
        """Calculate the current state of the bot. Should be implemented by subclasses."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    def run_episode(self):
        """Run a single episode of the bot's operation. Should be implemented by subclasses."""
        raise NotImplementedError("This method should be implemented by subclasses.")
