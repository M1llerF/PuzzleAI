import tkinter as tk
from tkinter import ttk
from BotFactory import BotFactory
from QLearningBot import QLearningConfig
from RewardSystem import RewardConfig
from BotTools import BotToolsConfig
from BotStatistics import BotStatistics
from BotProfile import BotProfile, ProfileManager
from Maze import Maze

class BotProfileApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Create New Bot Profile")
        
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.maze = Maze(10, 10)  # Assuming a 10x10 maze for initialization
        self.bot_factory = BotFactory(self.maze)
        self.profile_manager = ProfileManager('profiles')
        
        self.create_profile_screen()
    
    def create_profile_screen(self):
        ttk.Label(self.main_frame, text="Profile Name:").grid(row=0, column=0, sticky=tk.W)
        self.profile_name_entry = ttk.Entry(self.main_frame, width=25)
        self.profile_name_entry.grid(row=0, column=1, sticky=tk.W)

        ttk.Label(self.main_frame, text="Bot Type:").grid(row=1, column=0, sticky=tk.W)
        self.bot_type_combo = ttk.Combobox(self.main_frame, values=["QLearningBot"])
        self.bot_type_combo.grid(row=1, column=1, sticky=tk.W)

        ttk.Button(self.main_frame, text="Next", command=self.customize_q_learning).grid(row=2, column=1, sticky=tk.W)
    
    def customize_q_learning(self):
        self.profile_name = self.profile_name_entry.get()
        self.bot_type = self.bot_type_combo.get()
        
        if self.bot_type == 'QLearningBot':
            self.config = QLearningConfig()
        else:
            raise ValueError(f"Unknown bot type: {self.bot_type}")

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.main_frame, text="Learning Rate:").grid(row=0, column=0, sticky=tk.W)
        self.learning_rate_entry = ttk.Entry(self.main_frame, width=25)
        self.learning_rate_entry.insert(0, str(self.config.learning_rate))
        self.learning_rate_entry.grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(self.main_frame, text="Discount Factor:").grid(row=1, column=0, sticky=tk.W)
        self.discount_factor_entry = ttk.Entry(self.main_frame, width=25)
        self.discount_factor_entry.insert(0, str(self.config.discount_factor))
        self.discount_factor_entry.grid(row=1, column=1, sticky=tk.W)

        ttk.Button(self.main_frame, text="Next", command=self.customize_tools).grid(row=2, column=1, sticky=tk.W)
    
    def customize_tools(self):
        self.config.learning_rate = float(self.learning_rate_entry.get())
        self.config.discount_factor = float(self.discount_factor_entry.get())
        
        self.tools_config = BotToolsConfig()

        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        ttk.Label(self.main_frame, text="Tools Configuration:").grid(row=0, column=0, sticky=tk.W)
        
        self.tools_vars = {}
        row = 1
        for tool, tool_code in self.tools_config.tools.items():
            var = tk.BooleanVar(value=True)
            self.tools_vars[tool] = var
            ttk.Checkbutton(self.main_frame, text=tool, variable=var).grid(row=row, column=1, sticky=tk.W)
            row += 1

        ttk.Button(self.main_frame, text="Next", command=self.customize_rewards).grid(row=row, column=1, sticky=tk.W)

    def customize_rewards(self):
        self.tools_config.tools = {tool: tool_code for tool, tool_code in self.tools_config.tools.items() if self.tools_vars[tool].get()}
        
        self.reward_config = RewardConfig()

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.main_frame, text="Reward Configuration:").grid(row=0, column=0, sticky=tk.W)
        
        self.rewards_vars = {}
        row = 1
        for reward, value in self.reward_config.reward_modifiers.items():
            var = tk.StringVar(value=value)
            self.rewards_vars[reward] = var
            ttk.Label(self.main_frame, text=reward).grid(row=row, column=0, sticky=tk.W)
            ttk.Entry(self.main_frame, textvariable=var, width=25).grid(row=row, column=1, sticky=tk.W)
            row += 1
        
        ttk.Button(self.main_frame, text="Save Profile", command=self.save_profile).grid(row=row, column=1, sticky=tk.W)

    def save_profile(self):
        print("Saving profile...")
        profile_name = self.profile_name
        bot_type = self.bot_type
        learning_rate = float(self.learning_rate_entry.get())
        discount_factor = float(self.discount_factor_entry.get())

        self.config.learning_rate = learning_rate
        self.config.discount_factor = discount_factor

        self.reward_config.reward_modifiers = {reward: float(var.get()) for reward, var in self.rewards_vars.items()}
        
        profile = BotProfile(
            name=profile_name,
            bot_type=bot_type,
            config=self.config,
            reward_config=self.reward_config,
            tools_config=self.tools_config,
            statistics=BotStatistics(),
            bot_specific_data={}
        )
        
        self.profile_manager.save_profile(profile)
        print("Profile saved successfully!")
        print(f"Profile Name: {profile.name}")
        print(f"Bot Type: {profile.bot_type}")
        print(f"Config: {profile.config.__dict__}")
        print(f"Reward Config: {profile.reward_config.reward_modifiers}")
        print(f"Tools Config: {profile.tools_config.tools}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BotProfileApp(root)
    root.mainloop()
