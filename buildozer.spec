[app]
# 应用基本信息
title = 极简日历          # APK显示名称
package.name = calendarapk  # 包名（小写，无特殊字符）
package.domain = org.calendar  # 域名（自定义，格式：org.xxx）
source.dir = .            # 源码目录（当前目录）
source.include_exts = py,png,jpg,kv,atlas  # 包含的文件类型
version = 1.0.0           # 应用版本号

# 依赖配置
requirements = python3,kivy,kivymd  # 项目依赖库
android.api = 33          # 安卓API版本（建议33，适配主流设备）
android.ndk = 25b         # NDK版本（Buildozer兼容版本）
android.sdk = 24          # SDK版本
android.permissions = INTERNET  # 应用权限（日历无需额外权限，保留基础即可）

# 外观配置
android.icon = %(source.dir)s/assets/icon.png  # 图标路径（无图标可删除此行）
android.buildtools = 33.0.0  # 构建工具版本
android.apptheme = @android:style/Theme.Material.Light.NoActionBar  # 应用主题（无标题栏）

# 其他配置
log_level = 2             # 日志级别
warn_on_root = 1          # 根目录警告开关