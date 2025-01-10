# 使用官方 Python 镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY GymReservation.py .
COPY Captcha.py .
COPY config.yaml .

# 设置环境变量
ENV CONFIG_PATH=/app/config.yaml

# 声明挂载点
# VOLUME /app

# 运行程序
CMD ["python", "GymReservation.py"]