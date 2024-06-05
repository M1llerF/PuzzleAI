import tkinter as tk
from tkinter import ttk, messagebox

class MazeAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze AI Experiment")
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

    def show_create_edit_profile(self):
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

    def load_profiles(self):
        # This method should load the profile names from the backend and populate the listbox
        profiles = ["Profile 1", "Profile 2", "Profile 3"]  # Replace with actual backend call
        for profile in profiles:
            self.profile_list.insert(tk.END, profile)

    def create_new_profile(self):
        self.controller.show_create_edit_profile()

class CreateEditProfileFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        ttk.Label(self, text="Create/Edit Profile", font=("TkDefaultFont", 20)).pack(pady=10, padx=10)

        ttk.Label(self, text="Profile Name:").pack()
        self.profile_name_entry = ttk.Entry(self)
        self.profile_name_entry.pack()

        ttk.Label(self, text="Q-Learning Configuration:").pack()
        ttk.Label(self, text="Learning Rate:").pack()
        self.learning_rate_entry = ttk.Entry(self)
        self.learning_rate_entry.pack()
        ttk.Label(self, text="Discount Factor:").pack()
        self.discount_factor_entry = ttk.Entry(self)
        self.discount_factor_entry.pack()

        ttk.Label(self, text="Reward System:").pack()
        ttk.Label(self, text="Goal Reward:").pack()
        self.goal_reward_entry = ttk.Entry(self)
        self.goal_reward_entry.pack()
        ttk.Label(self, text="Wall Penalty:").pack()
        self.wall_penalty_entry = ttk.Entry(self)
        self.wall_penalty_entry.pack()

        ttk.Label(self, text="Tools Configuration:").pack()
        ttk.Label(self, text="Optimal Path:").pack()
        self.optimal_path_entry = ttk.Entry(self)
        self.optimal_path_entry.pack()
        ttk.Label(self, text="Detect Walls:").pack()
        self.detect_walls_entry = ttk.Entry(self)
        self.detect_walls_entry.pack()

        ttk.Button(self, text="Save", command=self.save_profile).pack(pady=10)
        ttk.Button(self, text="Cancel", command=self.cancel).pack(pady=10)

    def save_profile(self):
        # Save profile logic
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

        ttk.Button(self, text="Start Training", command=self.start_training).pack(pady=10)
        self.training_progress = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self.training_progress.pack(pady=10)
        self.log_output = tk.Text(self, height=10, width=50)
        self.log_output.pack(pady=10)

    def start_training(self):
        # Start training logic
        self.training_progress.start()
        self.log_output.insert(tk.END, "Training started...\n")

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
