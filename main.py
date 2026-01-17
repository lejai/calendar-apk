# -*- coding: utf-8 -*-
"""
日历APK项目入口（前后端桥接）
职责：初始化后端核心和前端UI，启动应用，无业务/UI逻辑
"""
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from backend_core import CalendarBackend
from frontend_ui import CalendarFrontend
from kivy.config import Config

# 配置中文字体支持
Config.set('kivy', 'default_font', ['Microsoft YaHei', 'SimHei', 'Arial', 'sans-serif'])

class CalendarAPKApp(MDApp):
    def build(self):
        """应用构建方法：初始化前后端，返回主屏幕"""
        # 1. 初始化后端核心（纯业务逻辑）
        self.backend = CalendarBackend()
        # 2. 初始化前端UI，注入后端实例（前端通过后端接口获取数据）
        self.frontend = CalendarFrontend(self.backend)
        # 3. 全局主题配置（统一APP风格）
        self.theme_cls.primary_palette = "Blue"  # 主色调（与UI_CONFIG一致）
        self.theme_cls.theme_style = "Light"  # 浅色主题
        
        # 创建主屏幕，添加前端布局
        screen = MDScreen()
        screen.add_widget(self.frontend)
        return screen

# 启动应用
if __name__ == "__main__":
    CalendarAPKApp().run()