import ttkbootstrap as ttk
import tkinter as tk
from enum import Enum
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from gui.colors import * 
import threading
from PIL import Image, ImageTk
from tkinter import font

import sys
import os

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for both development and PyInstaller. """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

quackhacks_path = resource_path("assets/quackhacks.png")
refresh_path = resource_path("assets/refresh2.png")


class App(ttk.Window):
    """
    Main window 

    """
    def __init__(self, controller):
        super().__init__(themename="darkly")

        # Controller holds model data 
        self.controller = controller 
        self.geometry("1000x800")
        self.title("QuackStats")
        # Makes sure app closes even if there are other threads running 
        self.protocol("WM_DELETE_WINDOW", self._on_close)


        self._setup_menu()

        container = ttk.Frame(self)  
        container.pack(side = "top", fill = "both", expand = True) 
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # For page managment
        self.frames = {}
        for F in (HomePage, AddRepos, StatsFrame):  
            frame = F(container, self.controller)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew") 

        self._show_frame(HomePage)

    def _on_close(self): 
        self.quit()

    def _show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()  

    def _setup_menu(self): 
        toolbar = ttk.Frame(self)
        toolbar.pack(side="top", fill="x")

        menu_btn = ttk.Menubutton(toolbar, text="Menu", width=10, bootstyle="secondary")
        menu_btn.pack(side='left', padx=0, pady=(0, 15))  # Adds space below with (top, bottom) padding

        menu = tk.Menu(menu_btn, tearoff=0)
        menu.add_command(label="Home", command=lambda: self._show_frame(HomePage))
        menu.add_command(label="Add Repos", command=lambda: self._show_frame(AddRepos))
        menu.add_command(label="Repo Statistics", command=lambda: self._show_frame(StatsFrame))

        # Color the options 
        for index in range(menu.index("end") + 1):
            menu.entryconfig(index, 
                             font=("Helvetica", 12), 
                             background="#232323", 
                             foreground="#d1d1d1",
                             activebackground="#00BC8C", 
                             activeforeground="#000000")

        menu_btn["menu"] = menu

class HomePage(ttk.Frame): 
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        img = Image.open(quackhacks_path)
        img = img.resize((600, 400), Image.Resampling.LANCZOS)  # Adjust size as needed
        self.image = ImageTk.PhotoImage(img)


        img_label = ttk.Label(self, image=self.image)
        img_label.place(relx=0.5, rely=0.2, anchor="center")

        desc_label = ttk.Label(self, text="QuackStats for QuackHacks: Version 1.0", font=DESC_FONT, foreground=TEXT_COLOR)
        desc_label.place(relx=0.5, rely=0.35, anchor="center")



class AddRepos(ttk.Frame):
    """
    Page for adding and removing repos from the repos in use list 
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        add_link_frame = ttk.Frame(self, padding=(20, 10))
        add_link_frame.pack(fill="x", pady=(0, 30))

        ttk.Label(add_link_frame, text="Add Github Repository Link", font=SUB_FONT, foreground=TEXT_COLOR).grid(row=0, column=0, sticky="w", pady=(0, 10))

        # To enter in the repo link 
        entry_list_font = font.Font(size=14)
        self.entry = ttk.Entry(add_link_frame, width=40, font=entry_list_font)
        self.entry.grid(row=1, column=0, sticky="ew", padx=(0, 10))
        self.submit_button = ttk.Button(
            add_link_frame, text="Submit", bootstyle="success", command=self._on_link_submit
        )
        self.submit_button.grid(row=1, column=1)
        add_link_frame.columnconfigure(0, weight=1)  

        # To list the repos in use 
        repos_frame = ttk.Frame(self, padding=(20, 10))
        repos_frame.pack(fill="both", expand=True)
        ttk.Label(repos_frame, text="Repositories In Use:", font=SUB_FONT, foreground=TEXT_COLOR).pack(anchor="w", pady=(0, 10))
        listbox_frame = ttk.Frame(repos_frame)
        listbox_frame.pack(fill="both", expand=True)

        self.listbox = tk.Listbox(listbox_frame, height=15, width=80, selectmode=tk.SINGLE, font=entry_list_font)
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        # To remove a repo from use 
        remove_button = ttk.Button(repos_frame, text="Remove Selected", command=self.remove_item, bootstyle="danger")
        remove_button.pack(anchor="e", pady=10)

    def _on_link_submit(self):
        item = self.entry.get().strip()
        if item:
            self.controller.add_link(item)
            self.entry.delete(0, tk.END)
            self.listbox.insert(tk.END, item)

    def remove_item(self):
        try:
            selected_index = self.listbox.curselection()[0]
            deleted_item = self.listbox.get(selected_index)
            self.controller.remove_link(deleted_item)
            self.listbox.delete(selected_index)
        except IndexError:
            pass  # No item selected





class StatsFrame(ttk.Frame): 
    """
    Displays repo stats via matplotlib

    """
    class CurrentStats(Enum): 
        # To know what to display when data is refreshed 
        REPO_LOC = 1 
        REPO_COMMITS = 2 
        USER_COMMITS = 3
        NONE = 4

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.current_stat = StatsFrame.CurrentStats.NONE

        top_frame = ttk.Frame(self)
        # top_frame.pack(fill="x")   
        top_frame.pack()   


        # Refersh image 
        self.angle = 0  
        self.is_spinning = False
        self.original_img = Image.open(refresh_path)
        self.icon_size = (20, 20)
        self.original_img = self.original_img.resize(self.icon_size, Image.Resampling.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(self.original_img)


        self.refresh_button = ttk.Button(
            top_frame, 
            image=self.tk_img,
            command=lambda: self._start_refresh_stats(self.refresh_button),
            bootstyle="secondary",
        )
        self.refresh_button.grid(row=0, column=2, sticky="e", padx=(0, 10), pady=(0, 0))

        # Selects a different chart to display 
        stats_menu_btn = ttk.Menubutton(
            top_frame, 
            text="Select Stats", 
            width=10, 
            bootstyle="secondary"
        )
        stats_menu_btn.grid(row=0, column=1, sticky="e", padx=(0, 10), pady=(0, 0))

        stats_menu = tk.Menu(stats_menu_btn, tearoff=0)
        stats_menu.add_command(label="User Commits", command=self._display_user_commits)
        stats_menu.add_command(label="Repo Commits", command=self._display_repo_commits)
        stats_menu.add_command(label="Repo LOC", command=self._display_repo_loc)

        stats_menu_btn["menu"] = stats_menu
        for index in range(stats_menu.index("end") + 1):
            stats_menu.entryconfig(index, 
                             font=("Helvetica", 12), 
                             background="#232323", 
                             foreground="#d1d1d1",
                             activebackground="#00BC8C", 
                             activeforeground="#000000")


        spacer = ttk.Label(top_frame)
        spacer.grid(row=0, column=0, sticky="ew")
        top_frame.grid_columnconfigure(0, weight=1)

        # Charts 
        self.plot_frame = ttk.Frame(self)
        self.plot_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.fig, self.ax = plt.subplots()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.fig.patch.set_facecolor(BACKGROUND_COLOR)
        self.ax.set_facecolor(BACKGROUND_COLOR)


    def toggle_spin(self):
        self.is_spinning = not self.is_spinning
        if self.is_spinning:
            self.spin_icon()

    def spin_icon(self):
        if self.is_spinning:
            self.angle = (self.angle + 10) % 360
            rotated_img = self.original_img.rotate(self.angle)
            self.tk_img = ImageTk.PhotoImage(rotated_img)
            self.refresh_button.config(image=self.tk_img)
            self.after(50, self.spin_icon)  

    def _start_refresh_stats(self, button): 
        self.toggle_spin()
        button.config(state="disabled")
        threading.Thread(target=self._fetch_repo_stats, args=(button,), daemon=True).start()
        
    def _fetch_repo_stats(self, button): 
        self.controller.refresh_repo_stats()
        self.after(0, lambda: self._on_stats_refreshed(button))

    def _on_stats_refreshed(self, button): 
        if self.current_stat == StatsFrame.CurrentStats.REPO_COMMITS: 
            self._display_repo_commits()
        elif self.current_stat == StatsFrame.CurrentStats.REPO_LOC: 
            self._display_repo_loc()
        elif self.current_stat == StatsFrame.CurrentStats.USER_COMMITS: 
            self._display_user_commits()
        self.toggle_spin()
        button.config(state="normal")


    def _display_repo_loc(self): 
        self.current_stat = StatsFrame.CurrentStats.REPO_LOC
        repo_names = [repo.name for repo in self.controller.get_repo_stats()]
        repo_locs = [repo.lines_of_code for repo in self.controller.get_repo_stats()]
        self._update_bar_graph("Repo Lines of Code", "Repos", "Commits", repo_names, repo_locs, "#53e2ee")

    def _display_repo_commits(self): 
        self.current_stat = StatsFrame.CurrentStats.REPO_COMMITS
        repo_names = [repo.name for repo in self.controller.get_repo_stats()]
        repo_commits = [repo.commits for repo in self.controller.get_repo_stats()]
        self._update_bar_graph("Repo Commits", "Repos", "Commits", repo_names, repo_commits, "#439429")

    def _display_user_commits(self): 
        self.current_stat = StatsFrame.CurrentStats.USER_COMMITS
        user_names = []
        user_commits = []
        for repo in self.controller.get_repo_stats(): 
            user_names += repo.user_commits.keys()
            user_commits += repo.user_commits.values()

        self._update_bar_graph("User Commits", "Users", "Commits", user_names, user_commits, "#007acc")


    def _update_bar_graph(self, title: str, x_axis: str, y_axis: str, x_data: list, y_data: list, color:str):

        self.ax.clear()
        self.ax.bar(x_data, y_data, color=color)
        
        self.ax.set_title(title, color=TEXT_COLOR, fontsize=16)
        self.ax.set_xlabel(x_axis, color=TEXT_COLOR, fontsize=14)
        self.ax.set_ylabel(y_axis, color=TEXT_COLOR, fontsize=14)
        
        self.ax.tick_params(axis='both', colors=TEXT_COLOR, labelsize=12)  
        
        for label in self.ax.get_xticklabels() + self.ax.get_yticklabels():
            label.set_fontsize(12)
            label.set_color(TEXT_COLOR)

        self.canvas.draw()

















