@echo off
echo 正在启动 AI 图片处理服务...

:: 检查 Python 环境
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 错误: 未找到 Python，请先安装 Python
    exit /b 1
)

:: 检查 Node.js 环境
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 错误: 未找到 Node.js，请先安装 Node.js
    exit /b 1
)

:: 启动后端服务
echo 启动后端服务...
cd backend

:: 检查虚拟环境是否存在
if not exist venv (
    echo 创建虚拟环境...
    python -m venv venv
)

:: 激活虚拟环境并安装依赖
call venv\Scripts\activate
echo 安装后端依赖...
pip install -r requirements.txt

:: 启动后端服务
start cmd /k "python run.py"

:: 返回上级目录
cd ..

:: 启动前端服务
echo 启动前端服务...
cd frontend

:: 安装前端依赖
echo 安装前端依赖...
call npm install

:: 启动前端开发服务器
start cmd /k "npm run dev"

echo 服务启动完成！
echo 前端服务地址: http://localhost:5173
echo 后端服务地址: http://localhost:8000

:: 等待用户按键
pause