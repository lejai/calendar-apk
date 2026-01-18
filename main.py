from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.metrics import dp
import datetime
import time
import platform

# 基础配置 - 确保跨设备兼容性
Config.set('graphics', 'maxfps', '60')  # 适中的刷新率，平衡性能和电池
Config.set('graphics', 'multisamples', '0')  # 减少GPU负担
Config.set('kivy', 'log_level', 'warning')  # 减少日志输出
Config.set('kivy', 'default_font', ['Roboto', 'DroidSans', 'DroidSansFallback', 'sans-serif'])  # 确保中文字体支持
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')  # 优化触摸响应

# 全局变量
update_interval = 1  # 秒

class CalendarApp(App):
    def build(self):
        """构建应用界面"""
        # 根布局 - 使用动态间距和内边距
        root = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        
        # 标题 - 使用适中的字体大小
        self.title_label = Label(
            text='极简日历', 
            font_size='36sp', 
            bold=True,
            halign='center', 
            valign='middle'
        )
        self.title_label.size_hint_y = None
        self.title_label.height = dp(80)
        root.add_widget(self.title_label)
        
        # 日期显示 - 使用适中的字体大小
        self.date_label = Label(
            text='', 
            font_size='28sp',
            halign='center', 
            valign='middle'
        )
        self.date_label.size_hint_y = None
        self.date_label.height = dp(60)
        root.add_widget(self.date_label)
        
        # 时间显示 - 使用适中的字体大小
        self.time_label = Label(
            text='', 
            font_size='56sp', 
            bold=True,
            halign='center', 
            valign='middle'
        )
        self.time_label.size_hint_y = None
        self.time_label.height = dp(100)
        root.add_widget(self.time_label)
        
        # 星期显示 - 使用适中的字体大小
        self.weekday_label = Label(
            text='', 
            font_size='24sp',
            halign='center', 
            valign='middle'
        )
        self.weekday_label.size_hint_y = None
        self.weekday_label.height = dp(50)
        root.add_widget(self.weekday_label)
        
        # 初始化显示
        self.update_display()
        
        # 启动定时更新（使用Kivy的Clock，更可靠）
        Clock.schedule_interval(self.update_display, update_interval)
        
        return root
    
    def update_display(self, dt=None):
        """更新显示内容 - 简化版，确保跨设备兼容性"""
        try:
            now = datetime.datetime.now()
            
            # 更新日期 - 使用最简单的格式，避免字体问题
            year = now.year
            month = now.month
            day = now.day
            date_str = f"{year}年{month}月{day}日"
            self.date_label.text = date_str
            
            # 更新时间 - 使用最简单的格式
            hour = now.hour
            minute = now.minute
            second = now.second
            time_str = f"{hour:02d}:{minute:02d}:{second:02d}"
            self.time_label.text = time_str
            
            # 更新星期 - 使用中文
            weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
            weekday_index = now.weekday()
            weekday_str = weekdays[weekday_index]
            self.weekday_label.text = weekday_str
            
        except Exception as e:
            # 出错时显示简单错误信息
            print(f"更新显示失败: {e}")
            self.date_label.text = "日期"
            self.time_label.text = "时间"
            self.weekday_label.text = "星期"
    
    def on_start(self):
        """应用启动时的初始化"""
        # 允许屏幕旋转
        Window.allow_screensaver = False
        Window.fullscreen = 'auto'
        
        # 绑定屏幕尺寸变化事件
        Window.bind(on_resize=self.on_window_resize)
        
        # 应用通用优化
        self.apply_generic_optimizations()
        
        print(f"应用启动成功 - 平台: {platform.system()}")
    
    def on_window_resize(self, window, width, height):
        """屏幕尺寸变化时的处理"""
        print(f"屏幕尺寸变化: {width}x{height}")
        # 根据屏幕方向调整字体大小
        if width > height:
            # 横屏模式
            self.adjust_for_landscape()
        else:
            # 竖屏模式
            self.adjust_for_portrait()
    
    def adjust_for_landscape(self):
        """调整为横屏模式"""
        print("切换到横屏模式")
        # 横屏模式下可以适当减小字体大小
        self.title_label.font_size = '32sp'
        self.date_label.font_size = '24sp'
        self.time_label.font_size = '48sp'
        self.weekday_label.font_size = '20sp'
    
    def adjust_for_portrait(self):
        """调整为竖屏模式"""
        print("切换到竖屏模式")
        # 竖屏模式下恢复默认字体大小
        self.title_label.font_size = '36sp'
        self.date_label.font_size = '28sp'
        self.time_label.font_size = '56sp'
        self.weekday_label.font_size = '24sp'
    
    def apply_generic_optimizations(self):
        """应用通用优化，确保在所有Android设备上正常运行"""
        try:
            # 1. 内存优化
            import gc
            gc.enable()
            gc.collect()
            
            # 2. 窗口状态优化
            Window.softinput_mode = 'pan'  # 处理软键盘弹出
            
            # 3. 确保应用在后台不被过度限制
            Config.set('graphics', 'window_state', 'visible')
            
            print("通用优化已应用")
        except Exception as e:
            print(f"应用优化失败: {e}")
    
    def on_stop(self):
        """应用停止时的清理"""
        print("应用停止")
        # 清理资源
        Clock.unschedule(self.update_display)

if __name__ == '__main__':
    CalendarApp().run()