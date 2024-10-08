import json
import os
import pickle
from DisplayTools import DisplayTools
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import matplotlib.colors as mcolors
from BotConfigs import bot_configs


from matplotlib import pyplot as plt
import numpy as np

from GameEnvironment import GameEnvironment
from QLearningBot import QLearningConfig
from RewardSystem import RewardConfig
from BotStatistics import BotStatistics
from RewardGrapher import RewardGrapher
from VisualizationStrategy import QLearningBotVisualizationStrategy
from BotProfile import BotProfile

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

        for F in (ProfileManagementFrame, CreateEditProfileFrame, BotTrainingFrame, VisualizationFrame):
            page_name = F.__name__
            frame = F(parent=self.root, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Set the default frame, replacing OverviewFrame
        self.show_frame("ProfileManagementFrame")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "BotTrainingFrame":
            frame.clear_profile_selection()

    def show_profile_management(self):
        self.show_frame("ProfileManagementFrame")

    def show_create_edit_profile(self, profile=None):
        frame = self.frames["CreateEditProfileFrame"]
        frame.load_profile(profile)
        self.show_frame("CreateEditProfileFrame")

    def show_bot_training(self):
        self.show_frame("BotTrainingFrame")

    def show_visualizations(self):
        self.show_frame("VisualizationFrame")

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

        ttk.Button(self, text="Delete Profile", command=self.delete_profile).pack(pady=10)

    def load_profiles(self):
        DisplayTools.load_profiles(self.controller.game_env.profile_manager, self.profile_list)

    def create_new_profile(self):
        self.controller.show_create_edit_profile()

    def on_profile_double_click(self, event):
        selected_index = self.profile_list.curselection()
        if selected_index:
            profile_name = self.profile_list.get(selected_index)
            self.load_profile(profile_name)

    def load_profile(self, profile_name):
        # Load the profile from the profile manager
        profile = self.controller.game_env.profile_manager.load_profile(profile_name)

        # Navigate to the CreateEditProfileFrame and load the profile details there
        self.controller.show_create_edit_profile(profile)


    def delete_profile(self):
        DisplayTools.delete_profile(self.controller.game_env.profile_manager, self.profile_list)
        self.load_profiles()
        self.controller.frames["BotTrainingFrame"].load_profiles()
        self.controller.frames["VisualizationFrame"].load_profiles()

class CreateEditProfileFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.current_config_widgets = []
        self.param_vars = {}  # Store references to parameter StringVars
        self.reward_vars = {}  # Store references to reward StringVars

        ttk.Label(self, text="Create/Edit Profile", font=("TkDefaultFont", 20)).pack(pady=10, padx=10)

        ttk.Label(self, text="Profile Name:").pack()
        self.profile_name_entry = ttk.Entry(self)
        self.profile_name_entry.pack()

        ttk.Label(self, text="Bot Type:").pack()
        self.bot_type_entry = ttk.Combobox(self, values=list(bot_configs.keys()))
        self.bot_type_entry.pack()
        self.bot_type_entry.bind("<<ComboboxSelected>>", self.update_bot_config_ui)

        self.config_frame = ttk.Frame(self)
        self.config_frame.pack(pady=10)

        ttk.Button(self, text="Save", command=self.save_profile).pack(pady=10)
        ttk.Button(self, text="Cancel", command=self.cancel).pack(pady=10)
        
    def update_bot_config_ui(self, event=None):
        # Clear current config widgets
        for widget in self.current_config_widgets:
            widget.destroy()
        self.current_config_widgets.clear()
        self.param_vars.clear()
        self.reward_vars.clear()

        bot_type = self.bot_type_entry.get()

        if bot_type not in bot_configs:
            return

        config = bot_configs[bot_type]

        # Handle params
        if "params" in config:
            for param_name, param_key in config["params"].items():
                label = ttk.Label(self.config_frame, text=f"{param_name}:")
                label.pack()
                var = tk.StringVar()
                entry = ttk.Entry(self.config_frame, textvariable=var)
                entry.pack()
                self.current_config_widgets.extend([label, entry])
                self.param_vars[param_key] = var



        # Handle rewards
        if "rewards" in config:
            label = ttk.Label(self.config_frame, text="Reward Configuration:")
            label.pack()
            self.current_config_widgets.append(label)
            for reward_key, default_value in config["rewards"].items():
                reward_label = ttk.Label(self.config_frame, text=reward_key)
                reward_label.pack()
                var = tk.StringVar(value=default_value)
                reward_entry = ttk.Entry(self.config_frame, textvariable=var)
                reward_entry.pack()
                self.current_config_widgets.extend([reward_label, reward_entry])
                self.reward_vars[reward_key] = var


    def load_profile(self, profile=None):
        self.profile = profile
        if profile:
            self.profile_name_entry.delete(0, tk.END)
            self.profile_name_entry.insert(0, profile.name)
            self.bot_type_entry.set(profile.bot_type)
            self.update_bot_config_ui()

            if profile.config:
                for param_key, var in self.param_vars.items():
                    var.set(getattr(profile.config, param_key, ""))

            if profile.reward_config:
                for reward_key, var in self.reward_vars.items():
                    var.set(profile.reward_config.reward_modifiers.get(reward_key, ""))

    def save_profile(self):
        profile_name = self.profile_name_entry.get()
        bot_type = self.bot_type_entry.get()

        if bot_type not in bot_configs:
            messagebox.showerror("Error", f"Unknown bot type: {bot_type}")
            return

        config = bot_configs[bot_type]

        # Extract bot-specific parameters
        bot_params = {param_key: float(var.get()) for param_key, var in self.param_vars.items()}

        # Extract reward configuration
        rewards_config = {reward_key: float(var.get()) for reward_key, var in self.reward_vars.items()}

        # Create the appropriate configuration object
        if bot_type == "QLearningBot":
            bot_config = QLearningConfig(**bot_params)
        else:
            bot_config = None  # Replace with appropriate config class for other bot types

        reward_config_obj = RewardConfig()
        reward_config_obj.reward_modifiers.update(rewards_config)

        # Create a new BotProfile instance and save it
        profile = BotProfile(
            name=profile_name,
            bot_type=bot_type,
            config=bot_config,
            reward_config=reward_config_obj,
            statistics=BotStatistics(),  # Initialize with default statistics
            bot_specific_data={}  # Add any additional bot-specific data here
        )

        self.controller.game_env.setup_new_profile(profile_name, bot_type, bot_config, reward_config_obj)

        # Initialize the mazes.json file
        profile_dir = f"profiles/{profile_name}"
        os.makedirs(profile_dir, exist_ok=True)
        maze_data_path = f"{profile_dir}/mazes.json"
        initial_data = {
            "latest": {},
            "highest": {"reward": float('-inf')},
            "lowest": {"reward": float('inf')}
        }
        with open(maze_data_path, 'w') as f:
            json.dump(initial_data, f, indent=4)

        # Notify the user
        messagebox.showinfo("Profile Saved", "Profile has been saved.")

        # Update profile lists in other frames
        self.controller.frames["ProfileManagementFrame"].load_profiles()
        self.controller.frames["VisualizationFrame"].load_profiles()
        self.controller.frames["BotTrainingFrame"].load_profiles()

        self.controller.show_profile_management()

    def cancel(self):
        self.controller.show_profile_management()

class BotTrainingFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.visualization_window = None
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
        
        ttk.Button(self, text="Open Visualization", command=self.open_visualization).pack(pady=10)

        self.load_profiles()

    def clear_profile_selection(self):
        self.profile_select.set("")

    def load_profiles(self):
        profiles = self.controller.game_env.profile_manager.list_profiles()
        self.profile_select['values'] = profiles

    def start_training(self):
        selected_profile = self.profile_select.get()
        if not selected_profile:
            messagebox.showerror("Error", "No profile selected.")
            return


        profile = self.controller.game_env.profile_manager.load_profile(selected_profile)
        profile_index = self.controller.game_env.apply_profile(profile)

        rounds = self.rounds_entry.get()
        if not rounds.isdigit():
            messagebox.showerror("Error", "Number of rounds must be a positive integer.")
            return
        
        rounds = int(rounds)
        self.training_progress['maximum'] = rounds
        self.training_progress['value'] = 0
        self.log_output.insert(tk.END, f"Training started for {selected_profile} with {rounds} rounds...\n")

        training_thread = threading.Thread(target=self.run_training, args=(rounds, profile_index, selected_profile))
        training_thread.start()

    def run_training(self, rounds, profile_index, selected_profile):
        profile_dir = f"{self.controller.game_env.profile_manager.profile_directory}/{selected_profile}"
        for i in range(rounds):
            self.controller.game_env.game_loop(1, profile_index, profile_dir)
            self.controller.root.after(0, self.update_progress, i + 1, rounds)

    def update_progress(self, completed_rounds, total_rounds):
        self.training_progress['value'] = completed_rounds
        self.log_output.insert(tk.END, f"Completed round {completed_rounds}/{total_rounds}\n")
        self.log_output.see(tk.END)  # Scroll to the end of the log output
        if completed_rounds == total_rounds:
            self.log_output.insert(tk.END, "Training completed.\n")
            self.log_output.see(tk.END)  # Scroll to the end of the log output


    def open_visualization(self):
        selected_profile = self.profile_select.get()
        if not selected_profile:
            messagebox.showerror("Error", "No profile selected.")
            return
        
        profile = self.controller.game_env.profile_manager.load_profile(selected_profile)
        profile_index = self.controller.game_env.apply_profile(profile)
        

        if self.visualization_window and self.visualization_window.winfo_exists():
            self.visualization_window.focus()
        else:
            self.visualization_window = VisualizationWindow(self.controller.root, self.controller.game_env, selected_profile, profile_index)
class VisualizationWindow(tk.Toplevel):
    def __init__(self, parent, game_env, profile_name, profile_index):
        super().__init__(parent)
        self.game_env = game_env
        self.profile_name = profile_name
        self.profile_index = profile_index
        self.title("Maze Visualization")
        self.geometry("600x600")

        self.canvas = tk.Canvas(self, width=500, height=500, bg="white")
        self.canvas.pack(pady=20)

        self.after_id = None
        self.visualize = True
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.update_visualization()

    def update_visualization(self):
        if not self.visualize:
            return


        self.canvas.delete("all")
        bot = self.game_env.bots[self.profile_index]  # Assuming single bot for now
        bot_position = bot.position
        self.display_with_bot_and_heatmap(bot_position, bot.statistics.get_visited_positions())
        self.after_id = self.after(100, self.update_visualization)

    def display_with_bot(self, bot_position):
        """ Display the maze with the bot's current position highlighted. """
        maze = self.game_env.maze
        cell_width = self.canvas.winfo_width() / maze.width
        cell_height = self.canvas.winfo_height() / maze.height

        for y in range(maze.height):
            for x in range(maze.width):
                if maze.grid[y][x] == 1:
                    self.canvas.create_rectangle(x * cell_width, y * cell_height,
                                                 (x + 1) * cell_width, (y + 1) * cell_height,
                                                 fill="black")

        start = maze.get_start()
        end = maze.end

        self.canvas.create_rectangle(start[1] * cell_width, start[0] * cell_height,
                                     (start[1] + 1) * cell_width, (start[0] + 1) * cell_height,
                                     fill="blue")

        self.canvas.create_rectangle(end[1] * cell_width, end[0] * cell_height,
                                     (end[1] + 1) * cell_width, (end[0] + 1) * cell_height,
                                     fill="green")

        self.canvas.create_oval(bot_position[1] * cell_width, bot_position[0] * cell_height,
                                (bot_position[1] + 1) * cell_width, (bot_position[0] + 1) * cell_height,
                                fill="red")

    def display_with_bot_and_heatmap(self, bot_position, visited_positions):
        """ Display the maze with the bot's current position highlighted and heatmap overlay. """
        maze = self.game_env.maze
        cell_width = self.canvas.winfo_width() / maze.width
        cell_height = self.canvas.winfo_height() / maze.height

        heatmap = np.zeros((maze.height, maze.width))
        for (x, y), count in visited_positions.items():
            heatmap[x, y] = count

        max_heat = heatmap.max() if heatmap.max() > 0 else 1  # Avoid division by zero
        cmap = plt.cm.Reds

        for y in range(maze.height):
            for x in range(maze.width):
                if maze.grid[y][x] == 1:
                    self.canvas.create_rectangle(x * cell_width, y * cell_height,
                                                 (x + 1) * cell_width, (y + 1) * cell_height,
                                                 fill="black")
                else:
                    heat_value = heatmap[y, x] / max_heat
                    if heat_value > 0:
                        color = mcolors.to_hex(cmap(heat_value))
                        self.canvas.create_rectangle(x * cell_width, y * cell_height,
                                                     (x + 1) * cell_width, (y + 1) * cell_height,
                                                     fill=color, outline=color)

        start = maze.get_start()
        end = maze.end

        self.canvas.create_rectangle(start[1] * cell_width, start[0] * cell_height,
                                     (start[1] + 1) * cell_width, (start[0] + 1) * cell_height,
                                     fill="blue")

        self.canvas.create_rectangle(end[1] * cell_width, end[0] * cell_height,
                                     (end[1] + 1) * cell_width, (end[0] + 1) * cell_height,
                                     fill="green")

        self.canvas.create_oval(bot_position[1] * cell_width, bot_position[0] * cell_height,
                                (bot_position[1] + 1) * cell_width, (bot_position[0] + 1) * cell_height,
                                fill="red")
        
    def on_close(self):
        self.visualize = False
        if self.after_id is not None:
            self.after_cancel(self.after_id)
        self.destroy()

class VisualizationFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.visualization_strategies = {
            'QLearningBot': QLearningBotVisualizationStrategy(),
            # Add other bot types and their strategies here
        }
        self.canvas_agg = None # Store the reference to the canvas object
        
        ttk.Label(self, text="Visualizations", font=("TkDefaultFont", 20)).pack(pady=10, padx=10)
        self.canvas = tk.Canvas(self, height=600, width=1000)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        ttk.Label(self.scrollable_frame, text="Select Profile:").pack()
        self.profile_select = ttk.Combobox(self.scrollable_frame)
        self.profile_select.pack()

        ttk.Button(self.scrollable_frame, text="Load Profile", command=self.load_profile).pack(pady=10)
        self.heatmap_frame = tk.Frame(self.scrollable_frame)
        self.heatmap_frame.pack(pady=10)
        ttk.Label(self.heatmap_frame, text="Latest Maze").grid(row=0, column=0, pady=10)
        self.heatmap_canvas_latest = tk.Canvas(self.heatmap_frame, width=300, height=300, bg="white")
        self.heatmap_canvas_latest.grid(row=1, column=0, padx=5)
        ttk.Label(self.heatmap_frame, text="Highest Reward Maze").grid(row=0, column=1, pady=10)
        self.heatmap_canvas_highest = tk.Canvas(self.heatmap_frame, width=300, height=300, bg="white")
        self.heatmap_canvas_highest.grid(row=1, column=1, padx=5)
        ttk.Label(self.heatmap_frame, text="Lowest Reward Maze").grid(row=0, column=2, pady=10)
        self.heatmap_canvas_lowest = tk.Canvas(self.heatmap_frame, width=300, height=300, bg="white")
        self.heatmap_canvas_lowest.grid(row=1, column=2, padx=5)
        ttk.Label(self.scrollable_frame, text="Reward Graph Visualization:").pack(pady=10)
        self.reward_canvas = tk.Canvas(self.scrollable_frame, width=800, height=400)
        self.reward_canvas.pack(pady=10)
        ttk.Label(self.scrollable_frame, text="Q-Table Visualization:").pack(pady=10)
        self.qtable_output = tk.Text(self.scrollable_frame, height=10, width=50)
        self.qtable_output.pack(pady=10)
        self.qtable_scrollbar = ttk.Scrollbar(self.scrollable_frame, command=self.qtable_output.yview)
        self.qtable_scrollbar.pack(side="right", fill="y")
        self.qtable_output.config(yscrollcommand=self.qtable_scrollbar.set)
        ttk.Label(self.scrollable_frame, text="Statistics:").pack(pady=10)
        self.statistics_output = tk.Text(self.scrollable_frame, height=5, width=50)
        self.statistics_output.pack(pady=10)
        self.load_profiles()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def load_profiles(self):
        profiles = self.controller.game_env.profile_manager.list_profiles()
        self.profile_select['values'] = profiles

    def load_profile(self):
        selected_profile = self.profile_select.get()
        if not selected_profile:
            messagebox.showerror("Error", "No profile selected.")
            return

        profile = self.controller.game_env.profile_manager.load_profile(selected_profile)
        profile_index = self.controller.game_env.apply_profile(profile)
        bot = self.controller.game_env.bots[profile_index]

        strategy = self.visualization_strategies.get(profile.bot_type)
        if strategy:
            strategy.visualize(self, bot, profile_index)

    def display_heatmap(self, canvas, maze, start, end, heatmap_data):
        canvas.delete("all")
        if maze is None:
            return

        maze_width = len(maze[0])
        maze_height = len(maze)
        cell_width = canvas.winfo_width() / maze_width
        cell_height = canvas.winfo_height() / maze_height

        heatmap = np.zeros((maze_height, maze_width))
        for (x, y), count in heatmap_data.items():
            heatmap[x, y] = count

        max_heat = heatmap.max() if heatmap.max() > 0 else 1
        cmap = plt.cm.Reds

        for y in range(maze_height):
            for x in range(maze_width):
                if maze[y][x] == 1:
                    canvas.create_rectangle(x * cell_width, y * cell_height, (x + 1) * cell_width, (y + 1) * cell_height, fill="black")
                else:
                    heat_value = heatmap[y, x] / max_heat
                    if heat_value > 0:
                        color = mcolors.to_hex(cmap(heat_value))
                        canvas.create_rectangle(x * cell_width, y * cell_height, (x + 1) * cell_width, (y + 1) * cell_height, fill=color, outline=color)

        canvas.create_rectangle(start[1] * cell_width, start[0] * cell_height, (start[1] + 1) * cell_width, (start[0] + 1) * cell_height, fill="blue")
        canvas.create_rectangle(end[1] * cell_width, end[0] * cell_height, (end[1] + 1) * cell_width, (end[0] + 1) * cell_height, fill="green")

    def display_qtable(self, bot, profile_index):
        top_values = self.get_top_q_values(bot, profile_index)
        self.qtable_output.delete("1.0", tk.END)
        self.qtable_output.insert(tk.END, "Top Q-Table Values:\n")
        for i, (q_value, (state, actions)) in enumerate(top_values):
            position, surrounding, step_count, distance_to_goal, _ = state
            best_action_index = np.argmax(actions)
            best_action = self.get_action_label(best_action_index)
            best_q_value = q_value
            self.qtable_output.insert(tk.END, f"Rank {i+1}:\n")
            self.qtable_output.insert(tk.END, f"  Current Position: {position}\n")
            self.qtable_output.insert(tk.END, f"  Surrounding: {surrounding}\n")
            self.qtable_output.insert(tk.END, f"  Step Count: {step_count}\n")
            self.qtable_output.insert(tk.END, f"  Distance to Goal: {distance_to_goal}\n")
            self.qtable_output.insert(tk.END, f"  Best Action: {best_action}\n")
            self.qtable_output.insert(tk.END, f"  Best Q-value: {best_q_value}\n\n")

    def display_statistics(self, bot, profile_index):
        statistics = bot.statistics
        self.statistics_output.delete("1.0", tk.END)
        profile_pkl_path = f"profiles/{bot.profile_name}/profile.pkl"
        with open(profile_pkl_path, 'rb') as file:
            profile_data = pickle.load(file)
        self.statistics_output.insert(tk.END, f"Total Steps: {profile_data.get('total_steps', 0)}\n")
        self.statistics_output.insert(tk.END, f"Non-Repeating Steps: {profile_data.get('non_repeating_steps_taken', 0)}\n")
        self.statistics_output.insert(tk.END, f"Times Revisited Squares: {profile_data.get('times_revisited_squares', 0)}\n")
        self.statistics_output.insert(tk.END, f"Times Bot Hit Wall: {profile_data.get('times_hit_wall', 0)}\n")

    def display_reward_graph(self, bot):
        if self.canvas_agg:
            self.canvas_agg.get_tk_widget().destroy()
        reward_filenames = [f'profiles/{bot.profile_name}/SimulationRewards.txt']
        grapher = RewardGrapher(reward_filenames)
        self.canvas_agg = grapher.run(self.reward_canvas)

    def get_top_q_values(self, bot, profile_index, n=10):
        q_table_items = bot.q_learning.q_table.items()
        top_items = []
        for item in q_table_items:
            q_value = np.max(item[1])
            if len(top_items) < n:
                top_items.append((q_value, item))
                top_items.sort(reverse=True, key=lambda x: x[0])
            else:
                if q_value > top_items[-1][0]:
                    top_items[-1] = (q_value, item)
                    top_items.sort(reverse=True, key=lambda x: x[0])
        return top_items

    def get_action_label(self, action_index):
        action_labels = ["Up", "Down", "Left", "Right"]
        return action_labels[action_index]