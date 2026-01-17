FROM ubuntu:22.04

# 安装必要的依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    python3 \
    python3-pip \
    openjdk-17-jdk \
    unzip \
    zip \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 安装 buildozer 和 cython
RUN pip3 install buildozer cython

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 构建 APK（使用 echo y 来自动回答 root 提示）
CMD ["bash", "-c", "echo y | buildozer android debug"]