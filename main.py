import os
import sys
import time
import cv2
import numpy as np
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.utils import platform
from kivy.uix.widget import Widget

# 检测是否为Android环境
ANDROID = platform == 'android'

# 自定义网格组件（用于麻将牌定位）
class LineGrid(Widget):
    pass

# 主屏幕（相机预览）
class MainScreen(Screen):
    camera_layout = ObjectProperty(None)
    cv2_camera = None
    camera_index = 0  # 0=后置摄像头，1=前置摄像头
    camera_preview = None
    button_layout = None

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        print("MainScreen初始化开始")
        # 强制触发布局绑定（双重保险）
        self.bind(on_ref_press=lambda *x: None)
        Builder.apply(self)
        print("MainScreen KV文件加载完成")
        print(f"camera_layout属性: {self.camera_layout}")
        print("MainScreen初始化完成")

    def on_enter(self, *args):
        """进入主屏幕时触发"""
        print("MainScreen进入")
        # 延迟50ms检查权限，等KV布局完全加载
        Clock.schedule_once(lambda dt: self.check_camera_permission(), 0.05)

    def check_camera_permission(self, *args):
        """检查相机权限"""
        print("检查相机权限...")
        if ANDROID:
            # Android环境权限检查
            try:
                from android.permissions import check_permission, request_permission, CAMERA
                if check_permission(CAMERA):
                    print("已获取相机权限")
                    self.setup_camera()
                else:
                    print("请求相机权限...")
                    request_permission(CAMERA, self.on_permission_result)
            except ImportError:
                print("Android权限模块未找到（非Android环境）")
                self.setup_camera()
        else:
            # 非Android环境默认有权限
            print("非Android环境，默认有相机权限")
            self.setup_camera()

    def on_permission_result(self, permission, granted):
        """权限请求结果回调"""
        if granted:
            print("用户授予了相机权限")
            self.setup_camera()
        else:
            print("用户拒绝了相机权限")
            self.show_permission_request()

    def show_permission_request(self):
        """显示权限请求提示"""
        if self.camera_layout:
            self.camera_layout.clear_widgets()
            
            # 权限提示标签
            permission_label = Label(
                text="无法访问相机，请授予相机权限",
                font_size='18sp',
                color=(1, 1, 1, 1),
                halign='center',
                valign='middle',
                size_hint=(1, 0.6)
            )
            
            # 授权按钮
            grant_button = Button(
                text="授予权限",
                size_hint=(0.5, 0.15),
                pos_hint={'center_x': 0.5},
                background_color=(1, 0.5, 0.5, 1),
                font_size='16sp'
            )
            grant_button.bind(on_press=lambda x: self.request_camera_permission())
            
            # 重试按钮
            retry_button = Button(
                text="重试",
                size_hint=(0.4, 0.15),
                pos_hint={'center_x': 0.5},
                background_color=(0.5, 0.5, 1, 1),
                font_size='16sp'
            )
            retry_button.bind(on_press=self.check_camera_permission)
            
            self.camera_layout.add_widget(permission_label)
            self.camera_layout.add_widget(grant_button)
            self.camera_layout.add_widget(retry_button)
        else:
            print("camera_layout仍未初始化，无法显示权限提示")

    def request_camera_permission(self):
        """主动请求相机权限"""
        if ANDROID:
            try:
                from android.permissions import request_permission, CAMERA
                request_permission(CAMERA, self.on_permission_result)
            except ImportError:
                print("Android权限模块未找到")

    def setup_camera(self):
        """初始化相机"""
        print("有权限，设置相机...")
        if self.camera_layout is None:
            print("错误: camera_layout未初始化，尝试重新加载KV")
            # 最后尝试手动加载KV
            Builder.load_file("mahjong_assistant.kv")
            self.camera_layout = self.ids.get('camera_layout', None)
            if self.camera_layout is None:
                print("仍然无法获取camera_layout，显示错误提示")
                self.show_camera_error_alt()
                return
            
        print("开始设置相机...")
        
        # 停止现有相机
        if self.cv2_camera is not None and self.cv2_camera.isOpened():
            self.cv2_camera.release()
            self.cv2_camera = None
        
        # 清空布局
        self.camera_layout.clear_widgets()
        print("已清除相机布局中的组件")
        
        # 创建相机预览组件
        self.camera_preview = Image(size_hint=(1, 1))
        self.camera_layout.add_widget(self.camera_preview)
        print("已添加相机预览组件")
        
        # 创建操作按钮布局
        self.button_layout = BoxLayout(
            size_hint=(1, 0.15),
            spacing=10,
            pos_hint={'y': 0}
        )
        
        # 切换摄像头按钮
        switch_button = Button(
            text="切换",
            size_hint_x=0.3,
            background_color=(0.5, 0.8, 1, 1),
            font_size='16sp'
        )
        switch_button.bind(on_press=self.switch_camera)
        
        # 拍照按钮
        capture_button = Button(
            text="拍照",
            size_hint_x=0.7,
            background_color=(1, 0.5, 0.5, 1),
            font_size='16sp'
        )
        capture_button.bind(on_press=self.capture_image)
        
        self.button_layout.add_widget(switch_button)
        self.button_layout.add_widget(capture_button)
        self.camera_layout.add_widget(self.button_layout)
        print("已添加按钮布局")
        
        # 打开摄像头（WSL下可能失败，正常）
        try:
            self.cv2_camera = cv2.VideoCapture(self.camera_index)
            if self.cv2_camera.isOpened():
                print("相机打开成功")
                # 启动相机预览更新
                Clock.schedule_interval(self.update_camera_preview, 1/30)
            else:
                print("相机打开失败（WSL环境正常）")
                self.show_camera_error()
        except Exception as e:
            print(f"相机初始化异常: {e}（WSL环境正常）")
            self.show_camera_error()
        
        print("相机设置完成")

    def update_camera_preview(self, dt):
        """更新相机预览画面"""
        if self.cv2_camera is None or not self.cv2_camera.isOpened():
            return
            
        ret, frame = self.cv2_camera.read()
        if ret:
            # 处理画面旋转（适配Android竖屏）
            if ANDROID:
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                frame = cv2.flip(frame, 1)  # 水平翻转
            
            # 转换为Kivy纹理
            buf = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            
            # 更新预览
            self.camera_preview.texture = texture

    def switch_camera(self, instance):
        """切换前后摄像头"""
        print("切换摄像头...")
        # 停止当前相机
        Clock.unschedule(self.update_camera_preview)
        if self.cv2_camera is not None and self.cv2_camera.isOpened():
            self.cv2_camera.release()
            self.cv2_camera = None
        
        # 清空布局
        self.camera_layout.clear_widgets()
        
        # 切换摄像头索引
        self.camera_index = 1 - self.camera_index
        print(f"切换到摄像头索引: {self.camera_index}")
        
        # 重新初始化相机
        self.setup_camera()

    def capture_image(self, instance):
        """拍摄照片并跳转到结果页"""
        print("拍摄照片...")
        if self.cv2_camera is None or not self.cv2_camera.isOpened():
            print("相机未初始化，模拟拍照...")
            # 模拟拍照（WSL下无相机时）
            timestamp = int(time.time())
            if ANDROID:
                image_path = os.path.join(App.get_running_app()._app_directory, f"capture_{timestamp}.jpg")
            else:
                image_path = os.path.join(App.get_running_app().user_data_dir, f"capture_{timestamp}.jpg")
            # 创建空图片文件
            cv2.imwrite(image_path, np.zeros((480, 640, 3), dtype=np.uint8))
            print(f"模拟照片已保存到: {image_path}")
            
            # 跳转到结果页
            result_screen = self.manager.get_screen('result')
            result_screen.image_path = image_path
            self.manager.current = 'result'
            return
            
        # 真实拍照逻辑
        ret, frame = self.cv2_camera.read()
        if ret:
            # 处理画面旋转
            if ANDROID:
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                frame = cv2.flip(frame, 1)
            
            # 生成时间戳文件名
            timestamp = int(time.time())
            
            # 保存图片（适配Android存储权限）
            if ANDROID:
                # Android私有目录（无需权限）
                image_path = os.path.join(App.get_running_app()._app_directory, f"capture_{timestamp}.jpg")
            else:
                # 非Android环境
                image_path = os.path.join(App.get_running_app().user_data_dir, f"capture_{timestamp}.jpg")
            
            # 保存图片
            cv2.imwrite(image_path, frame)
            print(f"照片已保存到: {image_path}")
            
            # 停止相机预览
            Clock.unschedule(self.update_camera_preview)
            if self.cv2_camera.isOpened():
                self.cv2_camera.release()
                self.cv2_camera = None
            
            # 传递图片路径到结果页
            result_screen = self.manager.get_screen('result')
            result_screen.image_path = image_path
            
            # 跳转到结果页
            self.manager.current = 'result'
        else:
            print("拍照失败")

    def show_camera_error(self):
        """显示相机错误提示"""
        if self.camera_layout:
            self.camera_layout.clear_widgets()
            error_label = Label(
                text="无法打开相机（WSL环境正常）\n点击拍照可测试跳转功能",
                font_size='16sp',
                color=(1, 1, 1, 1),
                halign='center',
                valign='middle'
            )
            # 添加测试拍照按钮
            test_button = Button(
                text="测试拍照跳转",
                size_hint=(0.6, 0.15),
                pos_hint={'center_x': 0.5, 'y': 0.2},
                background_color=(0.5, 1, 0.5, 1)
            )
            test_button.bind(on_press=self.capture_image)
            
            self.camera_layout.add_widget(error_label)
            self.camera_layout.add_widget(test_button)

    def show_camera_error_alt(self):
        """camera_layout未初始化时的错误提示"""
        # 手动创建根布局显示错误
        self.clear_widgets()
        error_layout = BoxLayout(orientation='vertical', padding=20)
        error_label = Label(
            text="布局加载失败！\n请检查KV文件是否存在且路径正确",
            font_size='18sp',
            color=(1, 0, 0, 1),
            halign='center'
        )
        restart_button = Button(
            text="重启应用",
            size_hint=(0.5, 0.2),
            pos_hint={'center_x': 0.5}
        )
        restart_button.bind(on_press=lambda x: App.get_running_app().stop())
        
        error_layout.add_widget(error_label)
        error_layout.add_widget(restart_button)
        self.add_widget(error_layout)

# 结果屏幕（识别结果展示）
class ResultScreen(Screen):
    result_layout = ObjectProperty(None)
    image_path = ""

    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)

    def on_enter(self, *args):
        """进入结果页时触发"""
        print(f"进入结果页，图片路径: {self.image_path}")
        # 延迟加载结果，确保布局绑定
        Clock.schedule_once(lambda dt: self.show_result(), 0.05)

    def show_result(self):
        """展示识别结果"""
        if self.result_layout is None:
            print("result_layout未初始化，尝试重新加载")
            Builder.load_file("mahjong_assistant.kv")
            self.result_layout = self.ids.get('result_layout', None)
            if self.result_layout is None:
                print("无法获取result_layout，显示简化结果")
                self.show_simple_result()
                return
            
        self.result_layout.clear_widgets()
        
        # 显示拍摄的图片
        if os.path.exists(self.image_path):
            image_widget = Image(
                source=self.image_path,
                size_hint=(1, 0.6),
                allow_stretch=True
            )
            self.result_layout.add_widget(image_widget)
        
        # 模拟识别结果（实际项目中替换为真实识别逻辑）
        result_label = Label(
            text="识别结果：\n手牌：1万 2万 3万 4条 5条 6条 7筒 8筒 9筒\n推荐出牌：9筒",
            font_size='16sp',
            color=(1, 1, 1, 1),
            halign='center',
            valign='middle',
            size_hint=(1, 0.4)
        )
        self.result_layout.add_widget(result_label)

    def show_simple_result(self):
        """简化结果展示（布局未加载时）"""
        self.clear_widgets()
        simple_layout = BoxLayout(orientation='vertical', padding=20)
        simple_layout.add_widget(Label(text="识别结果（简化模式）", font_size='20sp', color=(1,1,1,1)))
        simple_layout.add_widget(Label(text="推荐出牌：9筒", font_size='18sp'))
        back_button = Button(text="返回拍照", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
        back_button.bind(on_press=self.go_back)
        simple_layout.add_widget(back_button)
        self.add_widget(simple_layout)

    def go_back(self):
        """返回拍照页"""
        print("返回拍照页")
        self.manager.current = 'main'
        # 重新启动相机
        main_screen = self.manager.get_screen('main')
        Clock.schedule_once(lambda dt: main_screen.check_camera_permission(), 0.05)

    def re_identify(self):
        """重新识别"""
        print("重新识别...")
        self.show_result()

# 屏幕管理器
class MahjongAssistantScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        print("ScreenManager初始化")
        super(MahjongAssistantScreenManager, self).__init__(**kwargs)
        print("ScreenManager初始化完成")

# 应用主类
class MahjongAssistantApp(App):
    def build(self):
        # 先加载KV文件，再创建ScreenManager
        Builder.load_file("mahjong_assistant.kv")
        
        # 设置应用标题
        self.title = "卡五星麻将助手"
        
        # 设置窗口大小（仅开发环境生效）
        if not ANDROID:
            Window.size = (360, 640)
        
        # 返回屏幕管理器
        return MahjongAssistantScreenManager()

    def on_stop(self):
        """应用退出时清理资源"""
        print("应用退出，清理资源...")
        # 停止所有相机
        try:
            main_screen = self.root.get_screen('main')
            if main_screen.cv2_camera is not None and main_screen.cv2_camera.isOpened():
                main_screen.cv2_camera.release()
            Clock.unschedule(main_screen.update_camera_preview)
        except:
            pass

# 运行应用
if __name__ == '__main__':
    MahjongAssistantApp().run()