# -*- coding: utf-8 -*-
"""
日历APK前端UI（纯渲染交互，前后端分离）
基于KivyMD实现风格化设计，无任何业务逻辑，仅调用后端接口
"""
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivy.utils import get_color_from_hex
from kivy.animation import Animation
from kivy.uix.image import Image

# ===================== 全局UI风格配置（统一视觉效果，便于换肤） =====================
UI_CONFIG = {
    "MAIN_COLOR": get_color_from_hex("#002554"),       # 主色调：深蓝色（更现代）
    "ACCENT_COLOR": get_color_from_hex("#f8a3bc"),     # 强调色：亮粉色（更醒目）
    "GRAY_LIGHT": get_color_from_hex("#F5F5F5"),       # 浅灰色：空白日期背景
    "GRAY_DARK": get_color_from_hex("#115740"),         # 深绿色：当月日期文本
    "TEXT_WHITE": get_color_from_hex("#FFFFFF"),        # 白色文本：高亮背景搭配
    "SCHEDULE_BG": get_color_from_hex("#E3F2FD"),       # 日程标记背景色
    "BORDER_RADIUS": 24,                               # 全局控件圆角（更柔和）
    "SPACING": 10,                                     # 控件间距（更舒适）
    "PADDING": 24,                                     # 布局内边距（更宽松）
    "CARD_BG": get_color_from_hex("#FFFFFF"),           # 卡片背景色
    "TODAY_BG": get_color_from_hex("#f8a3bc"),          # 今日日期背景色
    "TODAY_TEXT": get_color_from_hex("#FFFFFF"),        # 今日日期文本色
}

class CalendarDateCard(MDCard):
    """自定义日期卡片组件：实现风格化显示，支持今日高亮、日程标记和点击动画"""
    def __init__(self, day=0, is_today=False, is_current_month=True, has_schedule=False, **kwargs):
        super().__init__(**kwargs)
        self.day = day  # 存储当前日期数字
        self.is_today = is_today
        self.is_current_month = is_current_month
        self.has_schedule = has_schedule
        
        # 卡片基础设置
        self.size_hint = (1, 1)
        self.orientation = 'vertical'
        self.radius = [UI_CONFIG["BORDER_RADIUS"]]
        
        # 创建日期标签
        self.date_label = MDLabel(
            text=str(day) if day != 0 else "",
            halign="center",
            valign="center",
            font_size="18sp",
            font_name="SimHei",  # 直接使用中文字体
            theme_text_color="Custom"
        )
        
        # 创建日程标记点
        self.schedule_dot = MDLabel(
            size_hint=(None, None),
            size=(6, 6),
            pos_hint={"center_x": 0.5},
            opacity=0
        )
        
        # 添加子控件
        self.add_widget(self.date_label)
        self.add_widget(self.schedule_dot)
        
        # 设置样式
        self._update_style()
        
    def _update_style(self):
        """根据日期类型更新卡片样式"""
        if not self.is_current_month or self.day == 0:
            # 非当月日期或空白日期
            self.md_bg_color = UI_CONFIG["GRAY_LIGHT"]
            self.date_label.text_color = get_color_from_hex("#9E9E9E")
            self.elevation = 0  # 无阴影
        elif self.is_today:
            # 今日日期
            self.md_bg_color = UI_CONFIG["TODAY_BG"]
            self.date_label.text_color = UI_CONFIG["TODAY_TEXT"]
            self.date_label.font_style = "H6"  # 加粗字体
            self.elevation = 0  # 无阴影
        else:
            # 当月正常日期
            self.md_bg_color = UI_CONFIG["CARD_BG"]
            self.date_label.text_color = UI_CONFIG["GRAY_DARK"]
            self.elevation = 0  # 无阴影
        
        # 日程标记
        if self.has_schedule and self.day != 0 and self.is_current_month:
            # 有日程的日期显示日程标记
            self.schedule_dot.opacity = 1
            self.schedule_dot.md_bg_color = UI_CONFIG["MAIN_COLOR"]
            # 为日程标记点设置圆形形状
            self.schedule_dot.radius = [3]
    
    def on_touch_down(self, touch):
        """处理点击事件，添加动画效果"""
        if self.collide_point(*touch.pos):
            # 添加点击动画
            anim = Animation(size_hint=(0.9, 0.9), duration=0.1)
            anim += Animation(size_hint=(1, 1), duration=0.1)
            anim.start(self)
        return super().on_touch_down(touch)

class CalendarFrontend(MDBoxLayout):
    """前端主布局：顶部导航栏+星期头部+日历网格+底部日程操作区"""
    def __init__(self, backend, **kwargs):
        super().__init__(**kwargs)
        self.backend = backend  # 注入后端实例（仅调用接口，不处理逻辑）
        self.orientation = "vertical"  # 垂直布局
        self.padding = UI_CONFIG["PADDING"]
        self.spacing = UI_CONFIG["SPACING"]
        
        # 顶部导航栏：年月标题 + 上月/今日/下月按钮
        self._create_top_bar()
        
        # 星期头部：显示星期
        self._create_week_header()
        
        # 3. 日历主体网格：6行7列（标准日历布局）
        self.calendar_grid = MDGridLayout(
            cols=7, 
            spacing=UI_CONFIG["SPACING"], 
            size_hint=(1, 0.8),
            padding=[UI_CONFIG["SPACING"], UI_CONFIG["SPACING"], UI_CONFIG["SPACING"], UI_CONFIG["SPACING"]]
        )
        self.add_widget(self.calendar_grid)
        
        # 4. 生肖底纹显示
        self._create_zodiac_display()
        
        # 初始化渲染日历界面
        self.refresh_calendar()

    def _create_zodiac_display(self):
        """创建生肖底纹显示"""
        self.zodiac_image = Image(
            source=f"assets/{self.backend.get_zodiac()}.jpg",
            size_hint=(0.25, 0.25),
            opacity=0.4,
            pos_hint={"center_x": 0.85, "center_y": 0.25}
        )
        self.add_widget(self.zodiac_image)

    def _create_divider(self):
        """创建分割线，增强视觉层次"""
        divider = MDBoxLayout(size_hint=(1, 0.005))
        divider.md_bg_color = get_color_from_hex("#E0E0E0")
        self.add_widget(divider)

    def _create_top_bar(self):
        """创建顶部导航栏（风格化设计，便于操作）"""
        top_bar = MDBoxLayout(
            orientation="horizontal", 
            size_hint=(1, 0.12), 
            spacing=16, 
            padding=[UI_CONFIG["PADDING"], 8, UI_CONFIG["PADDING"], 8],
            md_bg_color=get_color_from_hex("#F9FAFC")
        )
        
        # 上一年按钮（图标按钮，主色调）
        self.prev_year_btn = MDIconButton(
            icon="chevron-double-left",
            icon_color=UI_CONFIG["MAIN_COLOR"],
            on_release=lambda x: self._switch_year(-1),  # 绑定切换上一年事件
            theme_icon_color="Custom",
            icon_size="24sp"
        )
        
        # 上月按钮（图标按钮，主色调）
        self.prev_btn = MDIconButton(
            icon="chevron-left",
            icon_color=UI_CONFIG["MAIN_COLOR"],
            on_release=lambda x: self._switch_month(-1),  # 绑定切换上月事件
            theme_icon_color="Custom",
            icon_size="24sp"
        )
        
        # 年月标题（主色调文本，居中显示）
        self.date_title = MDLabel(
            text=self.backend.get_current_date_str(),
            halign="center",
            valign="center",
            font_size="32sp",  # 保持较大的字体大小
            theme_text_color="Custom",
            text_color=UI_CONFIG["MAIN_COLOR"],
            size_hint=(1, 1),
            bold=True
        )
        
        # 今日按钮（强调色背景，圆角样式）
        self.today_btn = MDFlatButton(
            text="Today",
            md_bg_color=UI_CONFIG["ACCENT_COLOR"],
            text_color=get_color_from_hex("#000000"),
            size_hint=(0.15, 1),
            rounded_button=True,
            font_name="SimHei",  # 直接使用中文字体
            font_size="16sp"
        )
        self.today_btn.bind(on_release=lambda x: self._back_to_today())  # 绑定返回今日事件
        
        # 下月按钮（图标按钮，主色调）
        self.next_btn = MDIconButton(
            icon="chevron-right",
            icon_color=UI_CONFIG["MAIN_COLOR"],
            on_release=lambda x: self._switch_month(1),  # 绑定切换下月事件
            theme_icon_color="Custom",
            icon_size="24sp"
        )
        
        # 下一年按钮（图标按钮，主色调）
        self.next_year_btn = MDIconButton(
            icon="chevron-double-right",
            icon_color=UI_CONFIG["MAIN_COLOR"],
            on_release=lambda x: self._switch_year(1),  # 绑定切换下一年事件
            theme_icon_color="Custom",
            icon_size="24sp"
        )
        
        # 将控件添加到导航栏
        top_bar.add_widget(self.prev_year_btn)
        top_bar.add_widget(self.prev_btn)
        top_bar.add_widget(self.date_title)
        top_bar.add_widget(self.today_btn)
        top_bar.add_widget(self.next_btn)
        top_bar.add_widget(self.next_year_btn)
        self.add_widget(top_bar)

    def _create_week_header(self):
        """创建星期头部（固定样式，区分日期维度）"""
        week_days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        week_bar = MDBoxLayout(
            orientation="horizontal", 
            size_hint=(1, 0.08), 
            spacing=0,
            padding=[UI_CONFIG["SPACING"], 0, UI_CONFIG["SPACING"], 0],
            md_bg_color=get_color_from_hex("#F5F7FA")
        )
        
        for day in week_days:
            day_box = MDBoxLayout(size_hint=(1/7, 1), padding=5)
            lbl = MDLabel(
                text=day,
                halign="center",
                valign="center",
                font_size="14sp",
                theme_text_color="Custom",
                text_color=UI_CONFIG["MAIN_COLOR"],
                bold=True
            )
            day_box.add_widget(lbl)
            week_bar.add_widget(day_box)
        
        self.add_widget(week_bar)



    def refresh_calendar(self):
        """核心渲染方法：调用后端接口获取数据，刷新日历界面"""
        self.calendar_grid.clear_widgets()  # 清空原有日历控件
        cal_matrix = self.backend.get_calendar_matrix()  # 从后端获取日历矩阵
        self.date_title.text = self.backend.get_current_date_str()  # 更新年月标题
        self.zodiac_image.source = f"assets/{self.backend.get_zodiac()}.jpg"  # 更新生肖显示
        
        # 检查当前是否为当月，控制今日按钮的可见性
        from datetime import datetime
        now = datetime.now()
        current_year_month = f"{now.year}/{now.month:02d}"
        is_current_month = (self.date_title.text == current_year_month)
        self.today_btn.opacity = 0 if is_current_month else 1
        self.today_btn.disabled = is_current_month
        
        # 遍历日历矩阵，创建日期卡片并添加到网格
        for week in cal_matrix:
            for day in week:
                is_today = self.backend.is_today(day)  # 判断是否为今日
                is_current = self.backend.get_current_month_day(day)  # 判断是否为当月日期
                has_schedule = len(self.backend.get_schedule(day)) > 0  # 判断是否有日程
                
                # 创建风格化日期卡片
                date_card = CalendarDateCard(
                    day=day,
                    is_today=is_today,
                    is_current_month=is_current,
                    has_schedule=has_schedule
                )
                
                # 绑定点击事件：选中日期并显示日程
                date_card.bind(on_release=lambda x, d=day: self._select_day(d))
                self.calendar_grid.add_widget(date_card)

    def _switch_month(self, offset):
        """切换月份：调用后端接口，刷新UI"""
        self.backend.switch_month(offset)
        self.refresh_calendar()

    def _switch_year(self, offset):
        """切换年份：调用后端接口，刷新UI"""
        self.backend.switch_year(offset)
        self.refresh_calendar()

    def _back_to_today(self):
        """返回今日：调用后端接口，刷新UI"""
        self.backend.back_to_today()
        self.refresh_calendar()

    def _select_day(self, day):
        """选中日期：显示该日期的日程"""
        self.selected_day = day
        # 这里可以添加日程显示逻辑，例如弹出对话框显示详细日程
        # 目前仅在控制台打印日程内容
        schedule_content = self.backend.get_schedule(day)
        if schedule_content:
            print(f"日程（{day}日）：{schedule_content}")

