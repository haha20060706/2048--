# records_window.py
import tkinter as tk
from tkinter import ttk
from utils import center_window


class RecordsWindow:
    """个人记录窗口"""

    def __init__(self, user_manager, username, theme_manager, current_theme):
        self.user_manager = user_manager
        self.username = username
        self.theme_manager = theme_manager
        self.current_theme = current_theme
        self.window = tk.Toplevel()
        self.window.title("我的游戏记录")

        theme = self.theme_manager.get_theme(current_theme)
        self.window.configure(bg=theme['bg'])

        center_window(self.window, 580, 500)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        theme = self.theme_manager.get_theme(self.current_theme)

        tk.Label(self.window, text="📋 我的游戏记录", font=("Arial", 20, "bold"),
                 bg=theme['bg'], fg=theme['title_color']).pack(pady=20)

        records = self.user_manager.get_user_records(self.username)
        total_score = sum(r['score'] for r in records) if records else 0
        avg_score = total_score // len(records) if records else 0

        stats_frame = tk.Frame(self.window, bg=theme['info_bg'], relief=tk.RAISED)
        stats_frame.pack(pady=10, padx=20, fill='x')

        stats_text = f"📊 总游戏次数: {len(records)}  |  🎯 平均得分: {avg_score}"
        tk.Label(stats_frame, text=stats_text, font=("Arial", 11),
                 bg=theme['info_bg'], fg=theme['text_color'], pady=8).pack()

        columns = ('得分', '最大数字', '步数', '游戏时间')
        self.tree = ttk.Treeview(self.window, columns=columns, show='headings', height=12)

        col_widths = [100, 100, 80, 250]
        for col, width in zip(columns, col_widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor='center')

        self.tree.pack(pady=20, padx=20, fill='both', expand=True)

        scrollbar = ttk.Scrollbar(self.window, orient='vertical', command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=scrollbar.set)

        close_btn = tk.Button(self.window, text="关闭", font=("Arial", 10),
                              bg=theme['button_primary'], fg='white', padx=20, pady=5,
                              command=self.window.destroy)
        close_btn.pack(pady=10)

    def load_data(self):
        records = self.user_manager.get_user_records(self.username)
        for record in records[::-1]:
            self.tree.insert('', 'end', values=(record['score'], record['max_number'],
                                                record['steps'], record['time']))