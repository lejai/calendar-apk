#!/bin/bash

# 设置环境变量
export BUILDOZER_ALLOW_ROOT=1

# 创建基本的项目文件
cat > main.py << 'EOF'
from kivy.app import App
from kivy.uix.label import Label

class CalendarApp(App):
    def build(self):
        return Label(text='Hello World')

if __name__ == '__main__':
    CalendarApp().run()
EOF

# 创建 buildozer.spec
cat > buildozer.spec << 'EOF'
[app]
title = 极简日历
package.name = calendarapk
package.domain = org.calendar
source.dir = .
requirements = python3,kivy
android.api = 33
android.sdk = 33
android.ndk = 25b
android.arch = armeabi-v7a
[buildozer]
log_level = 2
warn_on_root = 0
EOF

# 运行 buildozer 构建
echo "Starting build..."
buildozer android debug