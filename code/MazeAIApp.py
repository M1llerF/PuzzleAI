import tkinter as tk
from tkinter import ttk, messagebox
import threading
from GameEnvironment import GameEnvironment
from QLearningBot import QLearningConfig
from RewardSystem import RewardConfig
from BotTools import BotToolsConfig

class MazeAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze AI Experiment")
        self.game_env = GameEnvironment()
        self.create_navigation_bar()
        self.create_main_frames()
        
    def create_navigation_bar(self):
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.nav_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Navigation", menu=self.nav_menu)
        self.nav_menu.add_command(label="Profile Management", command=self.show_profile_management)
        self.nav_menu.add_command(label="Bot Training", command=self.show_bot_training)
        self.nav_menu.add_command(label="Visualizations", command=self.show_visualizations)
        self.nav_menu.add_command(label="Exit", command=self.root.quit)

    def create_main_frames(self):
        self.frames = {}
        
        for F in (OverviewFrame, ProfileManagementFrame, CreateEditProfileFrame, BotTrainingFrame, VisualizationsFrame):
            page_name = F.__name__
            frame = F(parent=self.root, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("OverviewFrame")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def show_profile_management(self):
        self.show_frame("ProfileManagementFrame")

    def show_create_edit_profile(self, profile=None):
        frame = self.frames["CreateEditProfileFrame"]
        frame.load_profile(profile)
        self.show_frame("CreateEditProfileFrame")

    def show_bot_training(self):
        self.show_frame("BotTrainingFrame")

    def show_visualizations(self):
        self.show_frame("VisualizationsFrame")

class OverviewFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        ttk.Label(self, text="Overview", font=("TkDefaultFont", 20)).pack(pady=10, padx=10)
        ttk.Label(self, text="Recently Used Profiles").pack()
        ttk.Label(self, text="Quick Access to Bots").pack()

class ProfileManagementFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        ttk.Label(self, text="Profile Management", font=("TkDefaultFont", 20)).pack(pady=10, padx=10)
        ttk.Button(self, text="Create New Profile", command=self.create_new_profile).pack(pady=10)

        self.profile_list = tk.Listbox(self)
        self.profile_list.pack(pady=10)
        self.load_profiles()
        self.profile_list.bind("<Double-Button-1>", self.on_profile_double_click)

    def load_profiles(self):
        profiles = self.controller.game_env.profile_manager.list_profiles()
        self.profile_list.delete(0, tk.END)
        for profile in profiles:
            self.profile_list.insert(tk.END, profile)

    def create_new_profile(self):
        self.controller.show_create_edit_profile()
    
    def on_profile_double_click(self, event):
        selected_index = self.profile_list.curselection()
        if selected_index:
            profile_name = self.profile_list.get(selected_index)
            print(profile_name)
            self.load_profile(profile_name)

    def load_profile(self, profile_name):
        profile = self.controller.game_env.profile_manager.load_profile(profile_name)
        self.controller.game_env.apply_profile(profile)
        self.controller.show_create_edit_profile(profile)

class CreateEditProfileFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        ttk.Label(self, text="Create/Edit Profile", font=("TkDefaultFont", 20)).pack(pady=10, padx=10)

        ttk.Label(self, text="Profile Name:").pack()
        self.profile_name_entry = ttk.Entry(self)
        self.profile_name_entry.pack()

        ttk.Label(self, text="Bot Type:").pack()
        self.bot_type_entry = ttk.Combobox(self, values=["QLearningBot"])
        self.bot_type_entry.pack()

        ttk.Label(self, text="Learning Rate:").pack()
        self.learning_rate_entry = ttk.Entry(self)
        self.learning_rate_entry.pack()
        
        ttk.Label(self, text="Discount Factor:").pack()
        self.discount_factor_entry = ttk.Entry(self)
        self.discount_factor_entry.pack()

        ttk.Label(self, text="Tools Configuration:").pack()
        self.tools = {
            'optimal_path': tk.BooleanVar(value=True),
            'optimal_length': tk.BooleanVar(value=True),
            'detect_walls': tk.BooleanVar(value=True)
        }
        
        for tool, var in self.tools.items():
            ttk.Checkbutton(self, text=tool, variable=var).pack()

        ttk.Label(self, text="Reward Configuration:").pack()
        self.rewards = {
            'goal_reached': tk.StringVar(value="1000 * (optimal_length // 10)"),
            'hit_wall': tk.StringVar(value="-100 * (optimal_length // 10)"),
            'revisit_optimal_path': tk.StringVar(value="-10 * (optimal_length // 10)"),
            'revisit_non_optimal_path': tk.StringVar(value="-15 * (optimal_length // 10)"),
            'move_in_optimal_path': tk.StringVar(value="5 * (optimal_length // 10)"),
            'see_goal_new_location': tk.StringVar(value="50"),
            'see_goal_revisit': tk.StringVar(value="5"),
            'per_move_penalty': tk.StringVar(value="-1 * (optimal_length // 100)")
        }

        for reward, var in self.rewards.items():
            ttk.Label(self, text=reward).pack()
            ttk.Entry(self, textvariable=var).pack()

        ttk.Button(self, text="Save", command=self.save_profile).pack(pady=10)
        ttk.Button(self, text="Cancel", command=self.cancel).pack(pady=10)
    
    def load_profile(self, profile=None):
        self.profile = profile
        if profile:
            self.profile_name_entry.delete(0, tk.END)
            self.profile_name_entry.insert(0, profile.name)
            self.bot_type_entry.set(profile.bot_type)

            if profile.config:
                self.learning_rate_entry.delete(0, tk.END)
                self.learning_rate_entry.insert(0, profile.config.learning_rate)
                self.discount_factor_entry.delete(0, tk.END)
                self.discount_factor_entry.insert(0, profile.config.discount_factor)

            if profile.tools_config:
                for tool, var in self.tools.items():
                    var.set(profile.tools_config.tools.get(tool, False))

            if profile.reward_config:
                for reward, var in self.rewards.items():
                    var.set(profile.reward_config.reward_modifiers.get(reward, ""))

    def save_profile(self):
        profile_name = self.profile_name_entry.get()
        bot_type = self.bot_type_entry.get()
        learning_rate = self.learning_rate_entry.get()
        discount_factor = self.discount_factor_entry.get()
        tools_config = {tool: var.get() for tool, var in self.tools.items()}
        rewards_config = {reward: var.get() for reward, var in self.rewards.items()}

        if bot_type == "QLearningBot":
            config = QLearningConfig(float(learning_rate), float(discount_factor))
        else:
            messagebox.showerror("Error", f"Unknown bot type: {bot_type}")
            return

        tools_config_obj = BotToolsConfig()
        tools_config_obj.tools.update(tools_config)
        
        reward_config_obj = RewardConfig()
        reward_config_obj.reward_modifiers.update(rewards_config)
        
        self.controller.game_env.setup_new_profile(profile_name, bot_type, config, reward_config_obj, tools_config_obj)

        messagebox.showinfo("Profile Saved", "Profile has been saved.")
        self.controller.show_profile_management()

    def cancel(self):
        self.controller.show_profile_management()

class BotTrainingFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        ttk.Label(self, text="Bot Training", font=("TkDefaultFont", 20)).pack(pady=10, padx=10)

        ttk.Label(self, text="Select Profile:").pack()
        self.profile_select = ttk.Combobox(self)
        self.profile_select.pack()

        ttk.Label(self, text="Number of Rounds:").pack()
        self.rounds_entry = ttk.Entry(self)
        self.rounds_entry.pack()

        ttk.Button(self, text="Start Training", command=self.start_training).pack(pady=10)
        self.training_progress = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self.training_progress.pack(pady=10)
        self.log_output = tk.Text(self, height=10, width=50)
        self.log_output.pack(pady=10)

        self.load_profiles()

    def load_profiles(self):
        profiles = self.controller.game_env.profile_manager.list_profiles()
        self.profile_select['values'] = profiles

    def start_training(self):
        selected_profile = self.profile_select.get()
        if not selected_profile:
            messagebox.showerror("Error", "No profile selected.")
            return

        profiles = self.controller.game_env.profile_manager.list_profiles()
        profile = self.controller.game_env.profile_manager.load_profile(selected_profile)
        profile_index = profiles.index(selected_profile)
        self.controller.game_env.apply_profile(profile)

        rounds = self.rounds_entry.get()
        if not rounds.isdigit():
            messagebox.showerror("Error", "Number of rounds must be a positive integer.")
            return
        
        rounds = int(rounds)
        self.training_progress['maximum'] = rounds
        self.training_progress['value'] = 0
        self.log_output.insert(tk.END, f"Training started for {selected_profile} with {rounds} rounds...\n")

        training_thread = threading.Thread(target=self.run_training, args=(rounds, profile_index))
        training_thread.start()

    def run_training(self, rounds, profile_index):
        for i in range(rounds):
            self.controller.game_env.game_loop(1, profile_index, self.update_progress)
            self.controller.root.after(0, self.update_progress, i + 1, rounds)

    def update_progress(self, completed_rounds, total_rounds):
        self.training_progress['value'] = completed_rounds
        self.log_output.insert(tk.END, f"Completed round {completed_rounds}/{total_rounds}\n")
        if completed_rounds == total_rounds:
            self.log_output.insert(tk.END, "Training completed.\n")

class VisualizationsFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        ttk.Label(self, text="Visualizations", font=("TkDefaultFont", 20)).pack(pady=10, padx=10)

        ttk.Label(self, text="Select Profile:").pack()
        self.profile_select = ttk.Combobox(self)
        self.profile_select.pack()

        ttk.Label(self, text="Heatmap Visualization:").pack(pady=10)
        self.heatmap_canvas = tk.Canvas(self, width=500, height=500, bg="white")
        self.heatmap_canvas.pack(pady=10)

        ttk.Label(self, text="Q-Table Visualization:").pack(pady=10)
        self.qtable_output = tk.Text(self, height=10, width=50)
        self.qtable_output.pack(pady=10)

        ttk.Label(self, text="Statistics:").pack(pady=10)
        self.statistics_output = tk.Text(self, height=5, width=50)
        self.statistics_output.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeAIApp(root)
    root.mainloop()
