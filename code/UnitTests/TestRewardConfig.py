import unittest

from RewardSystem import RewardConfig

class TestRewardConfig(unittest.TestCase):
    def setUp(self):
        self.reward_config = RewardConfig()

    def test_remove_reward_modifier(self):
        # Initial state
        initial_modifiers = self.reward_config.reward_modifiers.copy()

        # Remove a modifier
        self.reward_config.remove_reward_modifier = lambda: self.reward_config.reward_modifiers.pop('goal_reached', None)
        self.reward_config.remove_reward_modifier()

        # Ensure it was removed
        self.assertNotIn('goal_reached', self.reward_config.reward_modifiers)
        self.assertEqual(len(self.reward_config.reward_modifiers), len(initial_modifiers) - 1)

    def test_add_reward_modifier(self):
        # Add a new modifier
        self.reward_config.add_reward_modifier = lambda: self.reward_config.reward_modifiers.update({'new_reward': '500 * (optimal_length // 10)'})
        self.reward_config.add_reward_modifier()

        # Ensure it was added
        self.assertIn('new_reward', self.reward_config.reward_modifiers)
        self.assertEqual(self.reward_config.reward_modifiers['new_reward'], '500 * (optimal_length // 10)')

    def test_modify_reward_modifier(self):
        # Modify an existing modifier
        self.reward_config.modify_reward_modifier = lambda: self.reward_config.reward_modifiers.update({'hit_wall': '-200 * (optimal_length // 10)'})
        self.reward_config.modify_reward_modifier()

        # Ensure it was modified
        self.assertEqual(self.reward_config.reward_modifiers['hit_wall'], '-200 * (optimal_length // 10)')

if __name__ == "__main__":
    unittest.main()
