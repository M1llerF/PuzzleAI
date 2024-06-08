from BaseConfig import BaseConfig

class QLearningConfig(BaseConfig):
    def __init__(self, learning_rate=0.1, discount_factor=0.9):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

    def customize(self):
        self.learning_rate = float(input("Enter learning rate (default 0.1): ") or 0.1)
        self.discount_factor = float(input("Enter discount factor (default 0.9): ") or 0.9)
