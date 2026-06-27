# user_manager.py
import json
import os
from datetime import datetime


class UserManager:
    """用户管理类（本地文件存储）"""

    def __init__(self):
        # 获取当前文件所在目录（项目根目录）
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.base_dir, "data")
        self.data_file = os.path.join(self.data_dir, "game2048_users.json")

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        self.current_user = None
        self.load_data()

    def load_data(self):
        """加载用户数据"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.users = json.load(f)
        else:
            self.users = {}

    def save_data(self):
        """保存用户数据"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)

    def register(self, username, password, nickname=None):
        """用户注册"""
        if username in self.users:
            return False, "用户名已存在"

        if not nickname:
            nickname = username

        self.users[username] = {
            'password': password,
            'nickname': nickname,
            'best_score': 0,
            'max_number': 2,
            'total_games': 0,
            'records': []
        }
        self.save_data()
        return True, "注册成功"

    def login(self, username, password):
        """用户登录"""
        if username not in self.users:
            return False, "用户名不存在"

        if self.users[username]['password'] != password:
            return False, "密码错误"

        self.current_user = username
        return True, self.users[username]

    def save_game_record(self, username, score, max_number, steps):
        """保存游戏记录"""
        if username in self.users:
            user = self.users[username]
            user['records'].append({
                'score': score,
                'max_number': max_number,
                'steps': steps,
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            if len(user['records']) > 20:
                user['records'] = user['records'][-20:]
            if score > user['best_score']:
                user['best_score'] = score
            if max_number > user['max_number']:
                user['max_number'] = max_number
            user['total_games'] += 1
            self.save_data()
            return True
        return False

    def get_ranking(self):
        """获取排行榜"""
        ranking = []
        for username, info in self.users.items():
            ranking.append({
                'nickname': info['nickname'],
                'best_score': info['best_score'],
                'max_number': info['max_number'],
                'total_games': info['total_games']
            })
        ranking.sort(key=lambda x: x['best_score'], reverse=True)
        return ranking

    def get_user_records(self, username):
        """获取用户记录"""
        if username in self.users:
            return self.users[username]['records']
        return []