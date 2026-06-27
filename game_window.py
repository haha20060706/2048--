# game_window.py
import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
from utils import center_window
from ranking_window import RankingWindow
from records_window import RecordsWindow


class GameWindow:
    """游戏主窗口 - 包含所有创新功能"""

    def __init__(self, user_manager, username, user_info):
        self.user_manager = user_manager
        self.username = username
        self.user_info = user_info or {'nickname': '游客', 'best_score': 0, 'max_number': 2}
        self.is_guest = username is None

        from theme_manager import ThemeManager
        self.theme_manager = ThemeManager()
        self.current_theme = 'light'

        self.board_size = 4
        self.history = []
        self.max_history = 30

        # ===== 游戏模式相关 =====
        self.game_mode = "classic"
        self.steps_limit = 50
        self.time_limit = 60
        self.time_remaining = 60
        self.steps_remaining = 50
        self.target_score = 1024
        self.timer_running = False
        self.timer_id = None

        self.window = tk.Tk()
        self.window.title(f"2048游戏 - {self.user_info['nickname']}")
        self.window.resizable(True, True)

        theme = self.theme_manager.get_theme(self.current_theme)
        self.window.configure(bg=theme['bg'])

        window_width = 580 + (self.board_size - 4) * 40
        window_height = 800 + (self.board_size - 4) * 40
        center_window(self.window, window_width, window_height)

        self.grid = [[0] * self.board_size for _ in range(self.board_size)]
        self.score = 0
        self.steps = 0
        self.max_number = 2
        self.game_over = False
        self.win_achieved = False

        self.colors = theme['colors']
        self.text_colors = theme['text_colors']

        self.create_widgets()
        self.init_game()
        self.window.mainloop()

    def create_widgets(self):
        theme = self.theme_manager.get_theme(self.current_theme)

        main_frame = tk.Frame(self.window, bg=theme['bg'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        top_frame = tk.Frame(main_frame, bg=theme['bg'])
        top_frame.pack(fill='x', pady=(0, 20))

        title = tk.Label(top_frame, text="2048", font=("Arial", 36, "bold"),
                         bg=theme['bg'], fg=theme['title_color'])
        title.pack(side=tk.LEFT)

        score_frame = tk.Frame(top_frame, bg='#bbada0', padx=15, pady=8, relief=tk.RAISED)
        score_frame.pack(side=tk.RIGHT)

        tk.Label(score_frame, text="SCORE", font=("Arial", 10),
                 bg='#bbada0', fg='#eee4da').pack()
        self.score_label = tk.Label(score_frame, text="0", font=("Arial", 22, "bold"),
                                    bg='#bbada0', fg='white')
        self.score_label.pack()

        mode_frame = tk.Frame(main_frame, bg=theme['bg'])
        mode_frame.pack(fill='x', pady=(0, 10))

        tk.Label(mode_frame, text="🎯 游戏模式:", font=("Arial", 10),
                 bg=theme['bg'], fg=theme['text_color']).pack(side=tk.LEFT, padx=5)

        self.mode_var = tk.StringVar(value="经典模式")
        mode_menu = ttk.Combobox(mode_frame, textvariable=self.mode_var,
                                 values=["经典模式", "步数限制", "时间限制"],
                                 state="readonly", width=12)
        mode_menu.pack(side=tk.LEFT, padx=5)
        mode_menu.bind('<<ComboboxSelected>>', self.change_game_mode)
        mode_menu.bind("<Up>", lambda e: "break")
        mode_menu.bind("<Down>", lambda e: "break")
        mode_menu.bind("<Key>", lambda e: "break")

        self.limit_frame = tk.Frame(main_frame, bg=theme['bg'])
        self.limit_frame.pack(fill='x', pady=(0, 10))

        self.steps_frame = tk.Frame(self.limit_frame, bg=theme['bg'])
        self.steps_frame.pack(side=tk.LEFT, padx=5)
        self.steps_frame.pack_forget()

        tk.Label(self.steps_frame, text="步数:", font=("Arial", 10),
                 bg=theme['bg'], fg=theme['text_color']).pack(side=tk.LEFT, padx=5)

        self.steps_var = tk.StringVar(value="50")
        steps_menu = ttk.Combobox(self.steps_frame, textvariable=self.steps_var,
                                  values=["30", "50", "80", "100"],
                                  state="readonly", width=8)
        steps_menu.pack(side=tk.LEFT, padx=5)
        steps_menu.bind("<<ComboboxSelected>>", self.update_steps_limit)
        steps_menu.bind("<Up>", lambda e: "break")
        steps_menu.bind("<Down>", lambda e: "break")
        steps_menu.bind("<Key>", lambda e: "break")

        self.time_frame = tk.Frame(self.limit_frame, bg=theme['bg'])
        self.time_frame.pack(side=tk.LEFT, padx=5)
        self.time_frame.pack_forget()

        tk.Label(self.time_frame, text="时间:", font=("Arial", 10),
                 bg=theme['bg'], fg=theme['text_color']).pack(side=tk.LEFT, padx=5)

        self.time_var = tk.StringVar(value="60")
        time_menu = ttk.Combobox(self.time_frame, textvariable=self.time_var,
                                 values=["30", "60", "90", "120"],
                                 state="readonly", width=8)
        time_menu.pack(side=tk.LEFT, padx=5)
        time_menu.bind("<<ComboboxSelected>>", self.update_time_limit)
        time_menu.bind("<Up>", lambda e: "break")
        time_menu.bind("<Down>", lambda e: "break")
        time_menu.bind("<Key>", lambda e: "break")

        tk.Label(self.limit_frame, text="目标分数:", font=("Arial", 10),
                 bg=theme['bg'], fg=theme['text_color']).pack(side=tk.LEFT, padx=5)

        self.target_var = tk.StringVar(value="1024")
        target_menu = ttk.Combobox(self.limit_frame, textvariable=self.target_var,
                                   values=["512", "1024", "2048", "4096"],
                                   state="readonly", width=8)
        target_menu.pack(side=tk.LEFT, padx=5)
        target_menu.bind("<<ComboboxSelected>>", self.update_target_score)
        target_menu.bind("<Up>", lambda e: "break")
        target_menu.bind("<Down>", lambda e: "break")
        target_menu.bind("<Key>", lambda e: "break")

        status_frame = tk.Frame(main_frame, bg=theme['info_bg'], relief=tk.RAISED, bd=1)
        status_frame.pack(fill='x', pady=(0, 10))

        self.status_label = tk.Label(status_frame, text="🎮 经典模式 - 无限挑战",
                                     font=("Arial", 10),
                                     bg=theme['info_bg'], fg=theme['text_color'], pady=5)
        self.status_label.pack()

        user_frame = tk.Frame(main_frame, bg=theme['info_bg'], relief=tk.RAISED, bd=1)
        user_frame.pack(fill='x', pady=(0, 10))

        info_text = f"👤 {self.user_info['nickname']}  |  🏆 最高分: {self.user_info['best_score']}  |  🔢 最大数字: {self.user_info['max_number']}"
        if self.is_guest:
            info_text = "👤 游客模式  |  数据不会保存"

        self.user_label = tk.Label(user_frame, text=info_text, font=("Arial", 10),
                                   bg=theme['info_bg'], fg=theme['text_color'], pady=5)
        self.user_label.pack()

        size_frame = tk.Frame(main_frame, bg=theme['bg'])
        size_frame.pack(fill='x', pady=(0, 10))

        tk.Label(size_frame, text="棋盘大小:", font=("Arial", 10),
                 bg=theme['bg'], fg=theme['text_color']).pack(side=tk.LEFT, padx=5)

        self.size_var = tk.StringVar(value=f"{self.board_size}×{self.board_size}")
        size_menu = ttk.Combobox(size_frame, textvariable=self.size_var,
                                 values=["4×4", "5×5", "6×6"],
                                 state="readonly", width=8)
        size_menu.pack(side=tk.LEFT, padx=5)
        size_menu.bind('<<ComboboxSelected>>', self.change_board_size)
        size_menu.bind("<Up>", lambda e: "break")
        size_menu.bind("<Down>", lambda e: "break")
        size_menu.bind("<Key>", lambda e: "break")

        canvas_size = 380 + (self.board_size - 4) * 30
        self.canvas = tk.Canvas(main_frame, width=canvas_size, height=canvas_size,
                                bg=theme['grid_bg'], highlightthickness=0)
        self.canvas.pack(pady=(0, 10))

        stats_frame = tk.Frame(main_frame, bg=theme['bg'])
        stats_frame.pack(fill='x', pady=(0, 10))

        self.steps_label = tk.Label(stats_frame, text="🚶 步数: 0", font=("Arial", 10),
                                    bg=theme['bg'], fg=theme['text_color'])
        self.steps_label.pack(side=tk.LEFT, padx=15)

        self.max_label = tk.Label(stats_frame, text="💎 最大数字: 2", font=("Arial", 10),
                                  bg=theme['bg'], fg=theme['text_color'])
        self.max_label.pack(side=tk.LEFT, padx=15)

        self.limit_label = tk.Label(stats_frame, text="", font=("Arial", 10),
                                    bg=theme['bg'], fg='#e94560')
        self.limit_label.pack(side=tk.LEFT, padx=15)

        button_frame = tk.Frame(main_frame, bg=theme['bg'])
        button_frame.pack(fill='x', pady=(0, 10))

        buttons = [
            ("🔄 新游戏", self.new_game, theme['button_primary']),
            ("↩️ 撤销", self.undo_move, '#6c5ce7'),
            ("💡 AI提示", self.show_ai_hint, '#00b894'),
            ("🏆 排行榜", self.show_ranking, theme['button_secondary']),
            ("📋 我的记录", self.show_records, theme['button_secondary']),
            ("🎨 主题", self.switch_theme, '#fd79a8'),
            ("🔓 切换账号", self.switch_account, '#bbada0')
        ]

        btn_frame = tk.Frame(button_frame, bg=theme['bg'])
        btn_frame.pack()

        row1_buttons = buttons[:4]
        row2_buttons = buttons[4:]

        for text, cmd, color in row1_buttons:
            btn = tk.Button(btn_frame, text=text, font=("Arial", 9, "bold"),
                            bg=color, fg='white', padx=8, pady=3,
                            relief=tk.RAISED, command=cmd)
            btn.pack(side=tk.LEFT, padx=2, pady=2)

        btn_frame2 = tk.Frame(button_frame, bg=theme['bg'])
        btn_frame2.pack(pady=(3, 0))

        for text, cmd, color in row2_buttons:
            btn = tk.Button(btn_frame2, text=text, font=("Arial", 9, "bold"),
                            bg=color, fg='white', padx=8, pady=3,
                            relief=tk.RAISED, command=cmd)
            btn.pack(side=tk.LEFT, padx=2, pady=2)

        help_frame = tk.Frame(main_frame, bg=theme['bg'])
        help_frame.pack(fill='x')

        help_text = "💡 方向键移动  |  Ctrl+Z 撤销  |  鼠标选择模式"
        help_label = tk.Label(help_frame, text=help_text, font=("Arial", 9),
                              bg=theme['bg'], fg='#bbada0')
        help_label.pack()

        self.window.bind("<Key>", self.on_key_press)
        self.window.bind("<Control-z>", lambda e: self.undo_move())

        self.window.focus_set()
        self.canvas.bind("<Button-1>", lambda e: self.window.focus_set())

    # ===== 游戏模式相关方法 =====
    def change_game_mode(self, event=None):
        mode = self.mode_var.get()
        self.steps_frame.pack_forget()
        self.time_frame.pack_forget()

        if mode == "经典模式":
            self.game_mode = "classic"
            self.status_label.config(text="🎮 经典模式 - 无限挑战")
            self.limit_label.config(text="")
            self.steps_remaining = None
            self.time_remaining = None
            if self.timer_running:
                self.stop_timer()
        elif mode == "步数限制":
            self.game_mode = "steps"
            self.steps_frame.pack(side=tk.LEFT, padx=5)
            self.update_steps_limit()
            self.status_label.config(text=f"🚶 步数限制 - 目标 {self.target_score} 分")
            if self.timer_running:
                self.stop_timer()
        elif mode == "时间限制":
            self.game_mode = "time"
            self.time_frame.pack(side=tk.LEFT, padx=5)
            self.update_time_limit()
            self.status_label.config(text=f"⏱️ 时间限制 - 目标 {self.target_score} 分")
        self.new_game()

    def update_steps_limit(self, event=None):
        self.steps_limit = int(self.steps_var.get())
        self.steps_remaining = self.steps_limit
        self.status_label.config(text=f"🚶 步数限制 - {self.steps_limit}步内达到 {self.target_score} 分")
        if self.game_mode == "steps":
            self.limit_label.config(text=f"🚶 剩余步数: {self.steps_remaining}")

    def update_time_limit(self, event=None):
        self.time_limit = int(self.time_var.get())
        self.time_remaining = self.time_limit
        self.status_label.config(text=f"⏱️ 时间限制 - {self.time_limit}秒内达到 {self.target_score} 分")
        if self.game_mode == "time":
            self.limit_label.config(text=f"⏱️ 剩余时间: {self.time_remaining}s")

    def update_target_score(self, event=None):
        self.target_score = int(self.target_var.get())
        mode = self.mode_var.get()
        if mode == "步数限制":
            self.status_label.config(text=f"🚶 步数限制 - {self.steps_limit}步内达到 {self.target_score} 分")
        elif mode == "时间限制":
            self.status_label.config(text=f"⏱️ 时间限制 - {self.time_limit}秒内达到 {self.target_score} 分")

    def start_timer(self):
        if self.timer_running:
            return
        self.timer_running = True
        self.update_timer()

    def stop_timer(self):
        self.timer_running = False
        if self.timer_id:
            self.window.after_cancel(self.timer_id)
            self.timer_id = None

    def update_timer(self):
        if not self.timer_running or self.game_over:
            return
        self.time_remaining -= 1
        self.limit_label.config(text=f"⏱️ 剩余时间: {self.time_remaining}s")
        if self.time_remaining <= 0:
            self.time_remaining = 0
            self.limit_label.config(text="⏱️ 时间到！")
            self.game_over = True
            self.timer_running = False
            self.save_result()
            messagebox.showinfo("时间到",
                                f"⏱️ 时间到！\n\n"
                                f"📊 得分: {self.score}\n"
                                f"🎯 目标分数: {self.target_score}\n"
                                f"💎 最大数字: {self.max_number}\n\n"
                                f"{'🎉 达成目标！' if self.score >= self.target_score else '😅 未达成目标，继续加油！'}")
            return
        if self.score >= self.target_score:
            self.game_over = True
            self.timer_running = False
            self.save_result()
            messagebox.showinfo("🎉 恭喜！",
                                f"🎉 达成目标！\n\n"
                                f"📊 得分: {self.score}\n"
                                f"🎯 目标分数: {self.target_score}\n"
                                f"⏱️ 用时: {self.time_limit - self.time_remaining} 秒\n"
                                f"💎 最大数字: {self.max_number}")
            return
        self.timer_id = self.window.after(1000, self.update_timer)

    def check_game_limits(self):
        if self.game_mode == "steps":
            self.steps_remaining -= 1
            self.limit_label.config(text=f"🚶 剩余步数: {self.steps_remaining}")
            if self.score >= self.target_score:
                self.game_over = True
                self.save_result()
                messagebox.showinfo("🎉 恭喜！",
                                    f"🎉 达成目标！\n\n"
                                    f"📊 得分: {self.score}\n"
                                    f"🎯 目标分数: {self.target_score}\n"
                                    f"🚶 使用步数: {self.steps}\n"
                                    f"💎 最大数字: {self.max_number}")
                return True
            if self.steps_remaining <= 0:
                self.game_over = True
                self.save_result()
                messagebox.showinfo("步数用完",
                                    f"🚶 步数已用完！\n\n"
                                    f"📊 得分: {self.score}\n"
                                    f"🎯 目标分数: {self.target_score}\n"
                                    f"💎 最大数字: {self.max_number}\n\n"
                                    f"{'🎉 达成目标！' if self.score >= self.target_score else '😅 未达成目标，继续加油！'}")
                return True
        elif self.game_mode == "time":
            if self.score >= self.target_score:
                self.game_over = True
                self.stop_timer()
                self.save_result()
                messagebox.showinfo("🎉 恭喜！",
                                    f"🎉 达成目标！\n\n"
                                    f"📊 得分: {self.score}\n"
                                    f"🎯 目标分数: {self.target_score}\n"
                                    f"⏱️ 用时: {self.time_limit - self.time_remaining} 秒\n"
                                    f"💎 最大数字: {self.max_number}")
                return True
        return False

    def init_game(self):
        self.grid = [[0] * self.board_size for _ in range(self.board_size)]
        self.score = 0
        self.steps = 0
        self.max_number = 2
        self.game_over = False
        self.win_achieved = False
        self.history = []

        if self.game_mode == "steps":
            self.steps_remaining = self.steps_limit
            self.limit_label.config(text=f"🚶 剩余步数: {self.steps_remaining}")
        elif self.game_mode == "time":
            self.time_remaining = self.time_limit
            self.limit_label.config(text=f"⏱️ 剩余时间: {self.time_remaining}s")
            self.stop_timer()
            self.start_timer()
        else:
            self.limit_label.config(text="")

        initial_count = 2 if self.board_size <= 4 else 3
        for _ in range(initial_count):
            self.add_new_number()
        self.draw_grid()
        self.update_stats()

    def add_new_number(self):
        empty_cells = [(i, j) for i in range(self.board_size) for j in range(self.board_size)
                       if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def draw_grid(self):
        self.canvas.delete("all")
        theme = self.theme_manager.get_theme(self.current_theme)
        self.colors = theme['colors']
        self.text_colors = theme['text_colors']

        canvas_size = 380 + (self.board_size - 4) * 30
        margin = 15 + (self.board_size - 4) * 2
        cell_size = (canvas_size - margin * 2) / self.board_size
        gap = 5

        for i in range(self.board_size):
            for j in range(self.board_size):
                x1 = margin + j * (cell_size + gap)
                y1 = margin + i * (cell_size + gap)
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                value = self.grid[i][j]
                color = self.colors.get(value, "#edc22e")

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color,
                                             outline=color, width=0)

                if value != 0:
                    if value >= 1000:
                        font_size = int(18 - (self.board_size - 4) * 2)
                    elif value >= 100:
                        font_size = int(22 - (self.board_size - 4) * 2)
                    else:
                        font_size = int(28 - (self.board_size - 4) * 2)

                    text_color = self.text_colors['dark'] if value <= 4 else self.text_colors['light']
                    self.canvas.create_text(x1 + cell_size / 2, y1 + cell_size / 2,
                                            text=str(value),
                                            font=("Arial", max(12, font_size), "bold"),
                                            fill=text_color)

    def update_stats(self):
        theme = self.theme_manager.get_theme(self.current_theme)
        self.score_label.config(text=str(self.score))
        self.steps_label.config(text=f"🚶 步数: {self.steps}")
        self.max_label.config(text=f"💎 最大数字: {self.max_number}")
        self.window.configure(bg=theme['bg'])

    def on_key_press(self, event):
        if self.game_over:
            return
        key = event.keysym
        if event.widget != self.window:
            self.window.focus_set()
            return
        if key in ["Up", "Down", "Left", "Right"]:
            self.move(key)

    def move(self, direction):
        self.save_state()
        old_grid = [row[:] for row in self.grid]

        if direction == "Left":
            self.move_left()
        elif direction == "Right":
            self.move_right()
        elif direction == "Up":
            self.move_up()
        elif direction == "Down":
            self.move_down()

        if old_grid != self.grid:
            self.steps += 1
            self.add_new_number()
            self.draw_grid()
            self.update_stats()

            current_max = max(max(row) for row in self.grid)
            if current_max > self.max_number:
                self.max_number = current_max
                self.max_label.config(text=f"💎 最大数字: {self.max_number}", fg='#f67c5f')
                self.window.after(500, lambda: self.max_label.config(fg='#776e65'))

            if not self.win_achieved and current_max >= 2048:
                self.win_achieved = True
                messagebox.showinfo("🎉 恭喜！", "你达成了2048！继续挑战更高分数吧！")

            if not self.game_over:
                if self.check_game_limits():
                    return

            if self.is_game_over():
                self.game_over = True
                self.save_result()
                result = messagebox.askyesno("游戏结束",
                                             f"游戏结束！\n\n📊 得分: {self.score}\n🚶 步数: {self.steps}\n💎 最大数字: {self.max_number}\n\n是否重新开始？")
                if result:
                    self.new_game()
        else:
            if self.history:
                self.history.pop()

    def save_state(self):
        state = {
            'grid': [row[:] for row in self.grid],
            'score': self.score,
            'steps': self.steps,
            'max_number': self.max_number
        }
        self.history.append(state)
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def undo_move(self):
        if not self.history:
            messagebox.showinfo("提示", "没有可撤销的操作")
            return
        if self.game_over:
            messagebox.showinfo("提示", "游戏已结束，无法撤销")
            return
        state = self.history.pop()
        self.grid = state['grid']
        self.score = state['score']
        self.steps = state['steps']
        self.max_number = state['max_number']
        self.game_over = False
        self.draw_grid()
        self.update_stats()
        theme = self.theme_manager.get_theme(self.current_theme)
        self.window.configure(bg=theme['bg'])

    # ===== AI提示 =====
    def evaluate_board(self, grid):
        score = 0
        size = len(grid)

        empty_count = sum(1 for i in range(size) for j in range(size) if grid[i][j] == 0)
        score += empty_count * 10

        for i in range(size):
            row_values = [grid[i][j] for j in range(size) if grid[i][j] != 0]
            if len(row_values) >= 2:
                diff_sum = sum((row_values[k] - row_values[k + 1]) ** 2
                               for k in range(len(row_values) - 1))
                score += 100 / (diff_sum + 1)

        max_val = max(max(row) for row in grid)
        corner_values = [grid[0][0], grid[0][size - 1], grid[size - 1][0], grid[size - 1][size - 1]]
        if max_val in corner_values:
            score += 50

        for i in range(size):
            for j in range(size):
                if grid[i][j] != 0:
                    if j < size - 1 and grid[i][j] == grid[i][j + 1]:
                        score += 20
                    if i < size - 1 and grid[i][j] == grid[i + 1][j]:
                        score += 20

        return score

    def simulate_move(self, grid, direction):
        size = len(grid)
        new_grid = [row[:] for row in grid]
        score_gain = 0

        if direction == "Left":
            for i in range(size):
                row = [new_grid[i][j] for j in range(size) if new_grid[i][j] != 0]
                new_row = []
                skip = False
                for k in range(len(row)):
                    if skip:
                        skip = False
                        continue
                    if k + 1 < len(row) and row[k] == row[k + 1]:
                        new_row.append(row[k] * 2)
                        score_gain += row[k] * 2
                        skip = True
                    else:
                        new_row.append(row[k])
                new_row += [0] * (size - len(new_row))
                for j in range(size):
                    new_grid[i][j] = new_row[j]
        elif direction == "Right":
            for i in range(size):
                row = [new_grid[i][j] for j in range(size - 1, -1, -1) if new_grid[i][j] != 0]
                new_row = []
                skip = False
                for k in range(len(row)):
                    if skip:
                        skip = False
                        continue
                    if k + 1 < len(row) and row[k] == row[k + 1]:
                        new_row.append(row[k] * 2)
                        score_gain += row[k] * 2
                        skip = True
                    else:
                        new_row.append(row[k])
                new_row += [0] * (size - len(new_row))
                for j in range(size):
                    new_grid[i][size - 1 - j] = new_row[j]
        elif direction == "Up":
            for j in range(size):
                col = [new_grid[i][j] for i in range(size) if new_grid[i][j] != 0]
                new_col = []
                skip = False
                for k in range(len(col)):
                    if skip:
                        skip = False
                        continue
                    if k + 1 < len(col) and col[k] == col[k + 1]:
                        new_col.append(col[k] * 2)
                        score_gain += col[k] * 2
                        skip = True
                    else:
                        new_col.append(col[k])
                new_col += [0] * (size - len(new_col))
                for i in range(size):
                    new_grid[i][j] = new_col[i]
        elif direction == "Down":
            for j in range(size):
                col = [new_grid[i][j] for i in range(size - 1, -1, -1) if new_grid[i][j] != 0]
                new_col = []
                skip = False
                for k in range(len(col)):
                    if skip:
                        skip = False
                        continue
                    if k + 1 < len(col) and col[k] == col[k + 1]:
                        new_col.append(col[k] * 2)
                        score_gain += col[k] * 2
                        skip = True
                    else:
                        new_col.append(col[k])
                new_col += [0] * (size - len(new_col))
                for i in range(size):
                    new_grid[size - 1 - i][j] = new_col[i]

        return new_grid, score_gain

    def show_ai_hint(self):
        if self.game_over:
            canvas_size = 380 + (self.board_size - 4) * 30
            self.canvas.create_text(canvas_size / 2, canvas_size / 2,
                                    text="游戏已结束",
                                    font=("Arial", 24, "bold"),
                                    fill="#e94560")
            self.window.after(1500, self.draw_grid)
            return

        directions = ["Up", "Down", "Left", "Right"]
        best_direction = None
        best_score = -float('inf')
        all_scores = {}

        for direction in directions:
            new_grid, score_gain = self.simulate_move(self.grid, direction)
            if new_grid == self.grid:
                continue
            current_eval = self.evaluate_board(new_grid)
            future_best = 0
            for sub_dir in directions:
                sub_grid, sub_gain = self.simulate_move(new_grid, sub_dir)
                if sub_grid != new_grid:
                    sub_eval = self.evaluate_board(sub_grid) + sub_gain
                    future_best = max(future_best, sub_eval)
            total_score = current_eval + score_gain * 1.5 + future_best * 0.5
            all_scores[direction] = total_score
            if total_score > best_score:
                best_score = total_score
                best_direction = direction

        if best_direction is None:
            canvas_size = 380 + (self.board_size - 4) * 30
            self.canvas.create_text(canvas_size / 2, canvas_size / 2,
                                    text="没有可用移动",
                                    font=("Arial", 24, "bold"),
                                    fill="#e94560")
            self.window.after(1500, self.draw_grid)
            return

        direction_symbols = {"Up": "↑", "Down": "↓", "Left": "←", "Right": "→"}
        direction_names = {"Up": "上", "Down": "下", "Left": "左", "Right": "右"}

        canvas_size = 380 + (self.board_size - 4) * 30
        center_x = canvas_size / 2
        center_y = canvas_size / 2

        self.draw_grid()
        self.canvas.create_rectangle(0, 0, canvas_size, canvas_size,
                                     fill="#000000", stipple="gray50", outline="")

        arrow_size = 40
        if best_direction == "Up":
            self.canvas.create_polygon(
                center_x, center_y - arrow_size,
                center_x - arrow_size / 2, center_y,
                center_x + arrow_size / 2, center_y,
                fill="#e94560", outline="white", width=2
            )
        elif best_direction == "Down":
            self.canvas.create_polygon(
                center_x, center_y + arrow_size,
                center_x - arrow_size / 2, center_y,
                center_x + arrow_size / 2, center_y,
                fill="#e94560", outline="white", width=2
            )
        elif best_direction == "Left":
            self.canvas.create_polygon(
                center_x - arrow_size, center_y,
                center_x, center_y - arrow_size / 2,
                center_x, center_y + arrow_size / 2,
                fill="#e94560", outline="white", width=2
            )
        elif best_direction == "Right":
            self.canvas.create_polygon(
                center_x + arrow_size, center_y,
                center_x, center_y - arrow_size / 2,
                center_x, center_y + arrow_size / 2,
                fill="#e94560", outline="white", width=2
            )

        self.canvas.create_text(center_x, center_y - 70,
                                text=f"建议方向: {direction_symbols[best_direction]} {direction_names[best_direction]}",
                                font=("Arial", 20, "bold"),
                                fill="#e94560")
        self.canvas.create_text(center_x, center_y + 80,
                                text=f"评分: {best_score:.0f}",
                                font=("Arial", 14),
                                fill="white")
        self.canvas.create_text(center_x, center_y + 110,
                                text="按方向键移动",
                                font=("Arial", 12),
                                fill="#cccccc")
        self.window.after(2000, self.draw_grid)

    def change_board_size(self, event=None):
        selected = self.size_var.get()
        new_size = int(selected[0])
        if new_size == self.board_size:
            return
        if any(any(row) for row in self.grid):
            result = messagebox.askyesno("切换棋盘",
                                         f"切换棋盘大小将重新开始游戏，是否继续？")
            if not result:
                self.size_var.set(f"{self.board_size}×{self.board_size}")
                return
        self.board_size = new_size
        window_width = 580 + (self.board_size - 4) * 40
        window_height = 800 + (self.board_size - 4) * 40
        center_window(self.window, window_width, window_height)
        canvas_size = 380 + (self.board_size - 4) * 30
        self.canvas.config(width=canvas_size, height=canvas_size)
        self.new_game()
        theme = self.theme_manager.get_theme(self.current_theme)
        self.window.configure(bg=theme['bg'])

    def switch_theme(self):
        theme_names = self.theme_manager.get_theme_names()
        current_index = theme_names.index(self.current_theme)
        next_index = (current_index + 1) % len(theme_names)
        self.current_theme = theme_names[next_index]
        theme = self.theme_manager.get_theme(self.current_theme)
        self.window.configure(bg=theme['bg'])
        self.colors = theme['colors']
        self.text_colors = theme['text_colors']
        self.draw_grid()
        self.update_stats()
        theme_display_names = {'light': '☀️ 明亮模式', 'dark': '🌙 暗黑模式', 'retro': '📜 复古模式'}
        canvas_size = 380 + (self.board_size - 4) * 30
        self.canvas.create_text(canvas_size / 2, canvas_size / 2,
                                text=theme_display_names.get(self.current_theme, self.current_theme),
                                font=("Arial", 20, "bold"), fill='white')
        self.window.after(1000, self.draw_grid)

    def move_left(self):
        size = self.board_size
        for i in range(size):
            row = [self.grid[i][j] for j in range(size) if self.grid[i][j] != 0]
            new_row = []
            skip = False
            for k in range(len(row)):
                if skip:
                    skip = False
                    continue
                if k + 1 < len(row) and row[k] == row[k + 1]:
                    new_row.append(row[k] * 2)
                    self.score += row[k] * 2
                    skip = True
                else:
                    new_row.append(row[k])
            new_row += [0] * (size - len(new_row))
            for j in range(size):
                self.grid[i][j] = new_row[j]

    def move_right(self):
        size = self.board_size
        for i in range(size):
            row = [self.grid[i][j] for j in range(size - 1, -1, -1) if self.grid[i][j] != 0]
            new_row = []
            skip = False
            for k in range(len(row)):
                if skip:
                    skip = False
                    continue
                if k + 1 < len(row) and row[k] == row[k + 1]:
                    new_row.append(row[k] * 2)
                    self.score += row[k] * 2
                    skip = True
                else:
                    new_row.append(row[k])
            new_row += [0] * (size - len(new_row))
            for j in range(size):
                self.grid[i][size - 1 - j] = new_row[j]

    def move_up(self):
        size = self.board_size
        for j in range(size):
            col = [self.grid[i][j] for i in range(size) if self.grid[i][j] != 0]
            new_col = []
            skip = False
            for k in range(len(col)):
                if skip:
                    skip = False
                    continue
                if k + 1 < len(col) and col[k] == col[k + 1]:
                    new_col.append(col[k] * 2)
                    self.score += col[k] * 2
                    skip = True
                else:
                    new_col.append(col[k])
            new_col += [0] * (size - len(new_col))
            for i in range(size):
                self.grid[i][j] = new_col[i]

    def move_down(self):
        size = self.board_size
        for j in range(size):
            col = [self.grid[i][j] for i in range(size - 1, -1, -1) if self.grid[i][j] != 0]
            new_col = []
            skip = False
            for k in range(len(col)):
                if skip:
                    skip = False
                    continue
                if k + 1 < len(col) and col[k] == col[k + 1]:
                    new_col.append(col[k] * 2)
                    self.score += col[k] * 2
                    skip = True
                else:
                    new_col.append(col[k])
            new_col += [0] * (size - len(new_col))
            for i in range(size):
                self.grid[size - 1 - i][j] = new_col[i]

    def is_game_over(self):
        size = self.board_size
        for i in range(size):
            for j in range(size):
                if self.grid[i][j] == 0:
                    return False
        for i in range(size):
            for j in range(size):
                if (j < size - 1 and self.grid[i][j] == self.grid[i][j + 1]) or \
                        (i < size - 1 and self.grid[i][j] == self.grid[i + 1][j]):
                    return False
        return True

    def save_result(self):
        if not self.is_guest and self.username:
            self.user_manager.save_game_record(self.username, self.score, self.max_number, self.steps)
            if self.score > self.user_info['best_score']:
                self.user_info['best_score'] = self.score
            if self.max_number > self.user_info['max_number']:
                self.user_info['max_number'] = self.max_number

    # ===== 新增 new_game 方法 =====
    def new_game(self):
        """新游戏"""
        self.stop_timer()
        self.init_game()
        theme = self.theme_manager.get_theme(self.current_theme)
        self.window.configure(bg=theme['bg'])

    def show_ranking(self):
        RankingWindow(self.user_manager, self.theme_manager, self.current_theme)

    def show_records(self):
        if self.is_guest:
            messagebox.showinfo("提示", "游客模式无法查看记录，请注册账号")
        else:
            RecordsWindow(self.user_manager, self.username, self.theme_manager, self.current_theme)

    def switch_account(self):
        from login_window import LoginWindow
        self.window.destroy()
        LoginWindow()