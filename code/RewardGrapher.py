import matplotlib.pyplot as plt

class RewardGrapher:
    def __init__(self, filename='code/NonCodeFiles/SimulationRewards.txt'):
        self.filename = filename
    
    def read_rewards(self):
        with open(self.filename, 'r') as f:
            rewards = [float(line.strip()) for line in f]
        return rewards
    
    def plot_rewards(self, rewards):
        plt.figure(figsize=(10, 5))
        plt.plot(rewards, label='Rewards per Episode')
        plt.xlabel('Episode')
        plt.ylabel('Cumulative Reward')
        plt.title('Rewards over Episodes')
        plt.legend()
        plt.show()

    def run(self):
        rewards = self.read_rewards()
        self.plot_rewards(rewards)

# Example usage:
grapher = RewardGrapher()
grapher.run()
