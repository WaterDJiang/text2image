#!/bin/bash

# 检查并安装系统依赖
echo "检查系统依赖..."
if [ "$(uname)" == "Darwin" ]; then
    # macOS
    which brew > /dev/null || {
        echo "正在安装Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    }
    brew install cairo pkg-config
    export PKG_CONFIG_PATH="/opt/homebrew/lib/pkgconfig:/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH"
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    # Linux
    if [ -f /etc/debian_version ]; then
        # Debian/Ubuntu
        sudo apt-get update
        sudo apt-get install -y python3-cairo libcairo2-dev pkg-config python3-dev
    elif [ -f /etc/redhat-release ]; then
        # RHEL/CentOS
        sudo yum install -y cairo-devel pkg-config python3-devel
    fi
fi

# 创建虚拟环境
echo "创建虚拟环境..."
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 确保 pip 是最新的
echo "更新 pip..."
pip install --upgrade pip

# 安装基础依赖
echo "安装基础依赖..."
pip install wheel setuptools

# 安装 Cairo 相关依赖
echo "安装 Cairo 相关依赖..."
if [ "$(uname)" == "Darwin" ]; then
    LDFLAGS="-L/opt/homebrew/lib" CPPFLAGS="-I/opt/homebrew/include" pip install cairosvg
else
    pip install cairosvg
fi

# 安装其他依赖
echo "安装其他依赖..."
pip install -r requirements.txt

# 创建并配置.env文件
echo "配置环境变量..."
if [ ! -f .env ]; then
    echo "DEEPSEEK_API_KEY=sk-28eb8b72a1014cb4822c9fa005a54f95" > .env
    echo "DEEPSEEK_API_BASE=https://api.deepseek.com" >> .env
    echo "创建了新的.env文件"
else
    echo ".env文件已存在"
fi

echo "安装完成！" 