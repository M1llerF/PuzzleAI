import matplotlib.pyplot as plt
import numpy as np
class RewardGrapher:
    def __init__(self, filename='code/NonCodeFiles/SimulationRewards.txt'):
        self.filename = filename
    
    def read_rewards(self):
        with open(self.filename, 'r') as f:
            rewards = [float(line.strip()) for line in f]
        return rewards
    
    def calculate_slope(self, rewards):
        episodes = np.arange(len(rewards))
        slope, intercept = np.polyfit(episodes, rewards, 1)
        return slope, intercept

    def plot_rewards(self, rewards, slope, intercept):
        episodes = np.arange(len(rewards))
        plt.figure(figsize=(10, 5))
        plt.plot(rewards, label='Rewards per Episode')
        plt.plot(episodes, slope * episodes + intercept, label=f'Fit Line (slope={slope:.2f})', linestyle='--')
        plt.xlabel('Episode')
        plt.ylabel('Cumulative Reward')
        plt.title('Rewards over Episodes')
        plt.legend()
        plt.show()

    def run(self):
        rewards = self.read_rewards()
        slope, intercept = self.calculate_slope(rewards)
        self.plot_rewards(rewards, slope, intercept)

# Example usage:
grapher = RewardGrapher()
grapher.run()
