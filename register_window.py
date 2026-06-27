# register_window.py
import tkinter as tk
from tkinter import messagebox
from utils import center_window


class RegisterWindow:
    """注册窗口"""

    def __init__(self, user_manager, theme_manager):
        self.user_manager = user_manager
        self.theme_manager = theme_manager
        self.window = tk.Toplevel()
        self.window.title("注册账号")
        self.window.resizable(False, False)

        theme = self.theme_manager.get_theme()
        self.window.configure(bg=theme['bg'])

        center_window(self.window, 450, 520)
        self.create_widgets()

    def create_widgets(self):
        theme = self.theme_manager.get_theme()

        main_frame = tk.Frame(self.window, bg=theme['bg'])
        main_frame.pack(expand=True, fill='both', padx=40, pady=30)

        title = tk.Label(main_frame, text="注册账号", font=("Arial", 24, "bold"),
                         bg=theme['bg'], fg=theme['title_color'])
        title.pack(pady=20)

        frame = tk.Frame(main_frame, bg=theme['bg'])
        frame.pack(pady=20)

        tk.Label(frame, text="用户名", font=("Arial", 12),
                 bg=theme['bg'], fg=theme['text_color']).grid(row=0, column=0, pady=10, padx=10, sticky='e')
        self.username_entry = tk.Entry(frame, font=("Arial", 12), width=20,
                                       relief=tk.FLAT, bg='#eee4da')
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(frame, text="密码", font=("Arial", 12),
                 bg=theme['bg'], fg=theme['text_color']).grid(row=1, column=0, pady=10, padx=10, sticky='e')
        self.password_entry = tk.Entry(frame, show="*", font=("Arial", 12), width=20,
                                       relief=tk.FLAT, bg='#eee4da')
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(frame, text="确认密码", font=("Arial", 12),
                 bg=theme['bg'], fg=theme['text_color']).grid(row=2, column=0, pady=10, padx=10, sticky='e')
        self.confirm_entry = tk.Entry(frame, show="*", font=("Arial", 12), width=20,
                                      relief=tk.FLAT, bg='#eee4da')
        self.confirm_entry.grid(row=2, column=1, pady=10, padx=10)

        tk.Label(frame, text="昵称", font=("Arial", 12),
                 bg=theme['bg'], fg=theme['text_color']).grid(row=3, column=0, pady=10, padx=10, sticky='e')
        self.nickname_entry = tk.Entry(frame, font=("Arial", 12), width=20,
                                       relief=tk.FLAT, bg='#eee4da')
        self.nickname_entry.grid(row=3, column=1, pady=10, padx=10)

        register_btn = tk.Button(main_frame, text="注册", font=("Arial", 12, "bold"),
                                 bg=theme['button_secondary'], fg='white', width=15, height=1,
                                 relief=tk.RAISED, command=self.register)
        register_btn.pack(pady=30)

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()
        nickname = self.nickname_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("警告", "用户名和密码不能为空")
            return

        if password != confirm:
            messagebox.showerror("错误", "两次输入的密码不一致")
            return

        success, message = self.user_manager.register(username, password, nickname if nickname else None)
        if success:
            messagebox.showinfo("成功", "注册成功！请登录")
            self.window.destroy()
        else:
            messagebox.showerror("错误", message)