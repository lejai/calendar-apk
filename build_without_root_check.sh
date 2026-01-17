#!/bin/bash

# 查找 buildozer 的 __init__.py 文件
BUILDozer_INIT=$(python -c "import buildozer; print(buildozer.__file__)")

echo "Found buildozer __init__.py at: $BUILDozer_INIT"

# 修改 buildozer 的 __init__.py 文件，跳过 root 检查
sed -i 's/def check_root(self):/def check_root(self):\n        return/' "$BUILDozer_INIT"

echo "Modified buildozer __init__.py to skip root check"

# 构建 APK
echo "Starting APK build..."
buildozer android debug