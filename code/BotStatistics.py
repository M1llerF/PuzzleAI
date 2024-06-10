class BotStatistics:
    def __init__(self):
        self.total_steps = 0
        self.cumulative_reward_for_debugging = 0
        self.times_hit_wall = 0
        self.times_revisited_squares = 0
        self.non_repeating_steps_taken = 0
        self.visited_positions = {}
        self.last_visited_positions = []

    def reset(self):
        """Reset statistics for a new episode."""
        self.total_steps = 0
        self.cumulative_reward_for_debugging = 0
        self.times_hit_wall = 0
        self.times_revisited_squares = 0
        self.non_repeating_steps_taken = 0
        self.visited_positions.clear()
        self.last_visited_positions.clear()

    def update_visited_positions(self, position):
        """Update the visited positions."""
        self.visited_positions[position] = self.visited_positions.get(position, 0) + 1
        print(f"Updated visited_positions: {self.visited_positions}")  # Debug print


    def get_visited_positions(self):
        """Get the visited positions."""
        print(f"Returning visited_positions: {self.visited_positions}")  # Debug print
        return self.visited_positions

    def update_last_visited(self, position):
        """Update the last visited positions."""
        if len(self.last_visited_positions) >= 5:
            self.last_visited_positions.pop(0)
        if position not in self.last_visited_positions:
            self.last_visited_positions.append(position)

    def get_last_visited(self):
        """Get the last visited positions."""
        return self.last_visited_positions
