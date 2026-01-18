#!/usr/bin/env python3
import os
import subprocess
import sys

# 设置项目信息
PROJECT_NAME = "calendarapk"
PACKAGE_NAME = "org.calendar.calendarapk"
ACTIVITY_NAME = "org.kivy.android.PythonActivity"
VERSION = "1.0"
ORIENTATION = "portrait"

# 设置依赖
REQUIREMENTS = "python3,kivy,kivymd"

# 设置 Android 配置
ANDROID_API = "33"
ANDROID_NDK = "25b"
ANDROID_SDK = "33"
ANDROID_PERMISSIONS = "INTERNET"

# 设置目录
CURRENT_DIR = os.getcwd()
BUILD_DIR = os.path.join(CURRENT_DIR, "p4a_build")
DIST_DIR = os.path.join(CURRENT_DIR, "dist")

# 创建构建目录
os.makedirs(BUILD_DIR, exist_ok=True)
os.makedirs(DIST_DIR, exist_ok=True)

# 复制项目文件到构建目录
import shutil
for file in os.listdir(CURRENT_DIR):
    if file.endswith(".py"):
        shutil.copy(os.path.join(CURRENT_DIR, file), BUILD_DIR)
# 复制 assets 目录
assets_dir = os.path.join(CURRENT_DIR, "assets")
if os.path.exists(assets_dir):
    shutil.copytree(assets_dir, os.path.join(BUILD_DIR, "assets"), dirs_exist_ok=True)

# 构建 APK
print("Building APK with Python for Android...")
result = subprocess.run(
    [
        "p4a", "apk",
        "--debug",
        "--arch=armeabi-v7a",
        "--android-api", ANDROID_API,
        "--ndk-api", "25",
        "--sdk-dir", os.environ.get("ANDROID_SDK_ROOT", ""),
        "--ndk-dir", os.environ.get("ANDROID_NDK_HOME", ""),
        "--ndk-version", ANDROID_NDK,
        "--requirements", REQUIREMENTS,
        "--package", PACKAGE_NAME,
        "--name", PROJECT_NAME,
        "--version", VERSION,
        "--orientation", ORIENTATION,
        "--permission", ANDROID_PERMISSIONS,
        "--dist-dir", DIST_DIR,
        "--bootstrap", "sdl2",
        BUILD_DIR
    ],
    capture_output=True,
    text=True
)

# 打印输出
print("Build output:")
print(result.stdout)
print("Build errors:")
print(result.stderr)

# 返回命令的退出码
sys.exit(result.returncode)