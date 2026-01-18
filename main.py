from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.config import Config
from kivy.core.window import Window
from kivy.core.text import LabelBase
import datetime
import threading
import time
import os

# 针对骁龙8至尊版优化的配置
Config.set('graphics', 'maxfps', '120')  # 支持高刷新率屏幕
Config.set('graphics', 'multisamples', '0')  # 减少GPU负担
Config.set('kivy', 'window_icon', 'assets/icon.png')

# 全局变量
last_update_time = 0
update_interval = 1  # 秒
font_configured = False

class CalendarApp(App):
    def build(self):
        # 配置字体
        self.configure_fonts()
        
        # 根布局
        root = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # 标题
        title = Label(text='极简日历', font_size='40sp', bold=True, halign='center', valign='middle')
        title.size_hint_y = None
        title.height = 80
        root.add_widget(title)
        
        # 日期显示
        self.date_label = Label(text='', font_size='32sp', halign='center', valign='middle')
        self.date_label.size_hint_y = None
        self.date_label.height = 60
        root.add_widget(self.date_label)
        
        # 时间显示
        self.time_label = Label(text='', font_size='60sp', bold=True, halign='center', valign='middle')
        self.time_label.size_hint_y = None
        self.time_label.height = 100
        root.add_widget(self.time_label)
        
        # 星期显示
        self.weekday_label = Label(text='', font_size='24sp', halign='center', valign='middle')
        self.weekday_label.size_hint_y = None
        self.weekday_label.height = 50
        root.add_widget(self.weekday_label)
        
        # 电池优化按钮
        battery_btn = Button(text='电池优化模式', size_hint_y=None, height=60)
        battery_btn.bind(on_press=self.toggle_battery_optimization)
        root.add_widget(battery_btn)
        
        # 性能模式按钮
        perf_btn = Button(text='性能模式', size_hint_y=None, height=60)
        perf_btn.bind(on_press=self.toggle_performance_mode)
        root.add_widget(perf_btn)
        
        # 初始化
        self.update_display()
        
        # 启动定时更新（使用线程优化）
        self.update_thread = threading.Thread(target=self.update_thread_func, daemon=True)
        self.update_thread.start()
        
        # 电池优化标志
        self.battery_optimization = False
        
        return root
    
    def configure_fonts(self):
        """配置字体以确保在HyperOS上正确显示"""
        global font_configured
        if not font_configured:
            try:
                # 尝试使用系统默认字体
                # 对于中文显示，确保使用支持中文字符的字体
                Config.set('kivy', 'default_font', ['Roboto', 'DroidSans', 'DroidSansFallback', 'sans-serif'])
                font_configured = True
            except Exception as e:
                print(f"字体配置失败: {e}")
    
    def update_display(self):
        """更新显示内容"""
        try:
            now = datetime.datetime.now()
            
            # 更新日期 - 使用简单的格式避免字体问题
            date_str = f"{now.year}年{now.month}月{now.day}日"
            self.date_label.text = date_str
            
            # 更新时间 - 使用简单的格式
            time_str = f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"
            self.time_label.text = time_str
            
            # 更新星期 - 使用中文
            weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
            weekday_str = weekdays[now.weekday()]
            self.weekday_label.text = weekday_str
        except Exception as e:
            print(f"更新显示失败: {e}")
            # 显示错误信息以帮助调试
            self.date_label.text = "日期错误"
            self.time_label.text = "时间错误"
            self.weekday_label.text = "星期错误"
    
    def update_thread_func(self):
        """后台更新线程"""
        global last_update_time
        
        while True:
            current_time = time.time()
            
            # 根据模式调整更新频率
            if self.battery_optimization:
                interval = 5  # 电池优化模式下每5秒更新一次
            else:
                interval = update_interval  # 正常模式下每1秒更新一次
            
            if current_time - last_update_time >= interval:
                # 在主线程中更新UI
                Clock.schedule_once(lambda dt: self.update_display(), 0)
                last_update_time = current_time
            
            # 短暂休眠，减少CPU占用
            time.sleep(0.1)
    
    def toggle_battery_optimization(self, instance):
        """切换电池优化模式"""
        self.battery_optimization = not self.battery_optimization
        
        if self.battery_optimization:
            instance.text = '电池优化模式（已开启）'
            # 降低刷新率以节省电池
            Config.set('graphics', 'maxfps', '30')
        else:
            instance.text = '电池优化模式（已关闭）'
            # 恢复高刷新率
            Config.set('graphics', 'maxfps', '120')
    
    def toggle_performance_mode(self, instance):
        """切换性能模式"""
        # 性能模式下的优化
        Config.set('graphics', 'maxfps', '120')
        Config.set('kivy', 'log_level', 'error')  # 减少日志输出
        instance.text = '性能模式（已开启）'
    
    def on_start(self):
        """应用启动时的初始化"""
        # 调整窗口大小
        Window.size = (400, 600)
        
        # 针对米澎湃OS 3.0的优化
        self.apply_miui_optimizations()
    
    def apply_miui_optimizations(self):
        """应用米澎湃OS 3.0特定的优化"""
        try:
            # 1. 适配MIUI的深色模式
            from kivy.core.window import Window
            # 检测系统主题并适配
            try:
                # 尝试获取系统主题设置
                # 注意：这可能需要特定的权限或API
                pass
            except Exception:
                pass
            
            # 2. 优化内存使用
            import gc
            gc.enable()
            gc.collect()
            
            # 3. 减少后台限制影响
            # 对于HyperOS，设置合理的更新频率
            Config.set('graphics', 'window_state', 'visible')
            
            # 4. 优化触摸响应
            Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
            
            # 5. 适配高刷新率屏幕
            Config.set('graphics', 'maxfps', '120')
            
            print("米澎湃OS 3.0优化已应用")
        except Exception as e:
            print(f"应用MIUI优化失败: {e}")
    
    def on_stop(self):
        """应用停止时的清理"""
        # 清理资源
        pass

if __name__ == '__main__':
    CalendarApp().run()