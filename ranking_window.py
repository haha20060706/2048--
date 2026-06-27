# ranking_window.py
import tkinter as tk
from tkinter import ttk
from utils import center_window


class RankingWindow:
    """排行榜窗口"""

    def __init__(self, user_manager, theme_manager, current_theme):
        self.user_manager = user_manager
        self.theme_manager = theme_manager
        self.current_theme = current_theme
        self.window = tk.Toplevel()
        self.window.title("排行榜")

        theme = self.theme_manager.get_theme(current_theme)
        self.window.configure(bg=theme['bg'])

        center_window(self.window, 500, 550)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        theme = self.theme_manager.get_theme(self.current_theme)

        title_frame = tk.Frame(self.window, bg=theme['bg'])
        title_frame.pack(pady=20)

        tk.Label(title_frame, text="🏆", font=("Arial", 30),
                 bg=theme['bg']).pack(side=tk.LEFT)
        tk.Label(title_frame, text="排行榜", font=("Arial", 24, "bold"),
                 bg=theme['bg'], fg=theme['title_color']).pack(side=tk.LEFT)

        columns = ('排名', '昵称', '最高分', '最大数字', '游戏次数')
        self.tree = ttk.Treeview(self.window, columns=columns, show='headings', height=15)

        col_widths = [80, 120, 100, 100, 100]
        for col, width in zip(columns, col_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor='center')

        style = ttk.Style()
        style.theme_use('clam')

        self.tree.pack(pady=20, padx=20, fill='both', expand=True)

        scrollbar = ttk.Scrollbar(self.window, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        close_btn = tk.Button(self.window, text="关闭", font=("Arial", 10),
                              bg=theme['button_primary'], fg='white', padx=20, pady=5,
                              command=self.window.destroy)
        close_btn.pack(pady=10)

    def load_data(self):
        ranking = self.user_manager.get_ranking()
        for idx, player in enumerate(ranking, 1):
            if idx == 1:
                values = (f"🥇 {idx}", player['nickname'], player['best_score'],
                          player['max_number'], player['total_games'])
            elif idx == 2:
                values = (f"🥈 {idx}", player['nickname'], player['best_score'],
                          player['max_number'], player['total_games'])
            elif idx == 3:
                values = (f"🥉 {idx}", player['nickname'], player['best_score'],
                          player['max_number'], player['total_games'])
            else:
                values = (idx, player['nickname'], player['best_score'],
                          player['max_number'], player['total_games'])
            self.tree.insert('', 'end', values=values)