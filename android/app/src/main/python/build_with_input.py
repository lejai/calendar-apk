#!/usr/bin/env python3
import subprocess
import sys

# 运行 buildozer 命令，模拟用户输入 "y" 来回答 root 提示
process = subprocess.Popen(
    ["buildozer", "android", "debug"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# 模拟用户输入 "y"
stdout, stderr = process.communicate(input="y\n")

# 打印输出
print(stdout)
print(stderr)

# 返回命令的退出码
sys.exit(process.returncode)