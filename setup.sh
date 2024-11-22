#!/bin/bash

# 确保在项目根目录
cd "$(dirname "$0")"

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装基础依赖
pip install --upgrade pip wheel setuptools

# 安装项目依赖
pip install -r requirements.txt

# 创建并配置.env文件
if [ ! -f .env ]; then
    echo "DEEPSEEK_API_KEY=sk-28eb8b72a1014cb4822c9fa005a54f95" > .env
    echo "DEEPSEEK_API_BASE=https://api.deepseek.com" >> .env
    echo "创建了新的.env文件"
else
    echo ".env文件已存在"
fi

echo "安装完成！" 