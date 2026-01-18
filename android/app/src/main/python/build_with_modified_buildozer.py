#!/usr/bin/env python3
import subprocess
import sys
import os

# 查找 buildozer 的 __init__.py 文件
def find_buildozer_init():
    result = subprocess.run(
        ["pip", "show", "buildozer"],
        capture_output=True,
        text=True
    )
    for line in result.stdout.splitlines():
        if line.startswith("Location:"):
            location = line.split(":", 1)[1].strip()
            init_path = os.path.join(location, "buildozer", "__init__.py")
            if os.path.exists(init_path):
                return init_path
    return None

# 修改 buildozer 的 __init__.py 文件，跳过 root 检查
def modify_buildozer_init(init_path):
    with open(init_path, "r") as f:
        content = f.read()
    
    # 查找 check_root 方法
    import re
    pattern = r'def check_root\(\self\):[^}]+}'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        # 替换为一个空的方法
        new_content = content.replace(match.group(0), "def check_root(self):\n        pass")
        
        with open(init_path, "w") as f:
            f.write(new_content)
        
        print(f"Modified buildozer __init__.py at {init_path}")
        return True
    else:
        print("Could not find check_root method in buildozer __init__.py")
        return False

# 构建 APK
def build_apk():
    result = subprocess.run(
        ["buildozer", "android", "debug"],
        capture_output=True,
        text=True
    )
    
    print("Build output:")
    print(result.stdout)
    print("Build errors:")
    print(result.stderr)
    
    return result.returncode

def main():
    # 查找并修改 buildozer __init__.py
    init_path = find_buildozer_init()
    if init_path:
        if modify_buildozer_init(init_path):
            # 构建 APK
            return build_apk()
        else:
            return 1
    else:
        print("Could not find buildozer __init__.py")
        return 1

if __name__ == "__main__":
    sys.exit(main())