# login_window.py
import tkinter as tk
from tkinter import messagebox
from user_manager import UserManager
from theme_manager import ThemeManager
from register_window import RegisterWindow
from game_window import GameWindow
from utils import center_window


class LoginWindow:
    """登录窗口"""

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("2048游戏")
        self.window.resizable(False, False)

        self.theme_manager = ThemeManager()
        theme = self.theme_manager.get_theme()
        self.window.configure(bg=theme['bg'])

        center_window(self.window, 450, 500)

        self.user_manager = UserManager()

        self.create_widgets()
        self.window.mainloop()

    def create_widgets(self):
        theme = self.theme_manager.get_theme()

        main_frame = tk.Frame(self.window, bg=theme['bg'])
        main_frame.pack(expand=True, fill='both', padx=40, pady=30)

        title = tk.Label(main_frame, text="2048", font=("Arial", 52, "bold"),
                         bg=theme['bg'], fg=theme['title_color'])
        title.pack(pady=20)

        subtitle = tk.Label(main_frame, text="数字合并游戏", font=("Arial", 14),
                            bg=theme['bg'], fg='#bbada0')
        subtitle.pack(pady=(0, 30))

        login_frame = tk.Frame(main_frame, bg=theme['bg'])
        login_frame.pack(pady=20)

        tk.Label(login_frame, text="用户名", font=("Arial", 12),
                 bg=theme['bg'], fg=theme['text_color']).grid(row=0, column=0, pady=12, padx=10, sticky='e')
        self.username_entry = tk.Entry(login_frame, font=("Arial", 12), width=20,
                                       relief=tk.FLAT, bg='#eee4da', fg=theme['text_color'])
        self.username_entry.grid(row=0, column=1, pady=12, padx=10)

        tk.Label(login_frame, text="密码", font=("Arial", 12),
                 bg=theme['bg'], fg=theme['text_color']).grid(row=1, column=0, pady=12, padx=10, sticky='e')
        self.password_entry = tk.Entry(login_frame, show="*", font=("Arial", 12), width=20,
                                       relief=tk.FLAT, bg='#eee4da', fg=theme['text_color'])
        self.password_entry.grid(row=1, column=1, pady=12, padx=10)

        button_frame = tk.Frame(main_frame, bg=theme['bg'])
        button_frame.pack(pady=30)

        login_btn = tk.Button(button_frame, text="登录", font=("Arial", 12, "bold"),
                              bg=theme['button_primary'], fg='white', width=10, height=1,
                              relief=tk.RAISED, command=self.login)
        login_btn.pack(side=tk.LEFT, padx=10)

        register_btn = tk.Button(button_frame, text="注册", font=("Arial", 12, "bold"),
                                 bg=theme['button_secondary'], fg='white', width=10, height=1,
                                 relief=tk.RAISED, command=self.show_register)
        register_btn.pack(side=tk.LEFT, padx=10)

        guest_btn = tk.Button(main_frame, text="游客模式", font=("Arial", 10),
                              bg=theme['bg'], fg='#bbada0', relief=tk.FLAT,
                              cursor='hand2', command=self.guest_login)
        guest_btn.pack(pady=20)

        self.username_entry.bind('<Return>', lambda e: self.login())
        self.password_entry.bind('<Return>', lambda e: self.login())
        self.username_entry.focus()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("警告", "请输入用户名和密码")
            return

        success, result = self.user_manager.login(username, password)
        if success:
            self.window.destroy()
            GameWindow(self.user_manager, username, result)
        else:
            messagebox.showerror("错误", result)

    def show_register(self):
        RegisterWindow(self.user_manager, self.theme_manager)

    def guest_login(self):
        self.window.destroy()
        GameWindow(self.user_manager, None, None)