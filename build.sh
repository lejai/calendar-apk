#!/bin/bash

# 查找 buildozer 的 __init__.py 文件
BUILDozer_LOCATION=$(pip show buildozer | grep Location | cut -d: -f2 | xargs)
BUILDozer_INIT="$BUILDozer_LOCATION/buildozer/__init__.py"

echo "Found buildozer at: $BUILDozer_LOCATION"
echo "Buildozer __init__.py: $BUILDozer_INIT"

# 修改 buildozer 的 __init__.py 文件，跳过 root 检查
if [ -f "$BUILDozer_INIT" ]; then
    echo "Modifying buildozer __init__.py to skip root check..."
    # 使用 sed 替换 check_root 方法
    sed -i 's/def check_root(self):[^}]*}/def check_root(self):\n        pass/' "$BUILDozer_INIT"
    echo "Modified buildozer __init__.py"
else
    echo "Could not find buildozer __init__.py at $BUILDozer_INIT"
    exit 1
fi

# 构建 APK
echo "Starting APK build..."
buildozer android debug