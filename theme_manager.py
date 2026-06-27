# theme_manager.py


class ThemeManager:
    """主题管理类"""

    # 主题配色方案
    THEMES = {
        'light': {
            'name': '☀️ 明亮模式',
            'bg': '#faf8ef',
            'grid_bg': '#bbada0',
            'title_color': '#776e65',
            'text_color': '#776e65',
            'info_bg': '#eee4da',
            'button_primary': '#8f7a66',
            'button_secondary': '#f2b179',
            'colors': {
                0: "#cdc1b4",
                2: "#eee4da",
                4: "#ede0c8",
                8: "#f2b179",
                16: "#f59563",
                32: "#f67c5f",
                64: "#f65e3b",
                128: "#edcf72",
                256: "#edcc61",
                512: "#edc850",
                1024: "#edc53f",
                2048: "#edc22e",
                4096: "#3c3a32"
            },
            'text_colors': {
                'dark': "#776e65",
                'light': "white"
            }
        },
        'dark': {
            'name': '🌙 暗黑模式',
            'bg': '#1a1a2e',
            'grid_bg': '#16213e',
            'title_color': '#e94560',
            'text_color': '#eeeeee',
            'info_bg': '#0f3460',
            'button_primary': '#e94560',
            'button_secondary': '#533483',
            'colors': {
                0: "#2d2d44",
                2: "#3d3d5c",
                4: "#4d4d74",
                8: "#e94560",
                16: "#f5a623",
                32: "#f5a623",
                64: "#f5a623",
                128: "#e94560",
                256: "#e94560",
                512: "#e94560",
                1024: "#e94560",
                2048: "#e94560",
                4096: "#ff6b6b"
            },
            'text_colors': {
                'dark': "#eeeeee",
                'light': "white"
            }
        },
        'retro': {
            'name': '📜 复古模式',
            'bg': '#f5e6d3',
            'grid_bg': '#d4a574',
            'title_color': '#8b6b4d',
            'text_color': '#5d4037',
            'info_bg': '#e8d5c4',
            'button_primary': '#8b6b4d',
            'button_secondary': '#b8956a',
            'colors': {
                0: "#d4c5a9",
                2: "#f0e6d3",
                4: "#e8d5c4",
                8: "#d4a574",
                16: "#c4956a",
                32: "#b8855a",
                64: "#a8754a",
                128: "#d4a574",
                256: "#c4956a",
                512: "#b8855a",
                1024: "#a8754a",
                2048: "#8b6b4d",
                4096: "#5d4037"
            },
            'text_colors': {
                'dark': "#5d4037",
                'light': "#f5e6d3"
            }
        }
    }

    def __init__(self):
        self.current_theme = 'light'

    def get_theme(self, theme_name=None):
        if theme_name is None:
            theme_name = self.current_theme
        return self.THEMES.get(theme_name, self.THEMES['light'])

    def switch_theme(self, theme_name):
        if theme_name in self.THEMES:
            self.current_theme = theme_name
            return True
        return False

    def get_theme_names(self):
        return list(self.THEMES.keys())

    def get_theme_display_names(self):
        return [self.THEMES[name]['name'] for name in self.THEMES]