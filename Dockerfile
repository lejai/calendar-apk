FROM kivy/buildozer:latest

# 设置环境变量
ENV BUILDOZER_ALLOW_ROOT=1

# 创建工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 构建 APK
CMD ["bash", "-c", "buildozer android debug"]