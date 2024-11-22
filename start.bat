@echo off
echo 激活虚拟环境...
call venv\Scripts\activate.bat

# 设置 PYTHONPATH
set PYTHONPATH=%PYTHONPATH%;%CD%

echo 检查Ollama服务...
curl -s http://localhost:11434/api/version > nul 2>&1
if errorlevel 1 (
    echo 错误: 无法连接到Ollama服务，请确保Ollama已启动
    exit /b 1
)

echo 启动后端服务...
cd backend
start /b cmd /c "python -m uvicorn main:app --reload --port 8000 --log-level debug"

echo 等待后端服务启动...
set max_attempts=30
set attempt=0
:wait_loop
if %attempt% geq %max_attempts% (
    echo 错误: 后端服务启动超时
    exit /b 1
)
curl -s http://localhost:8000/health > nul 2>&1
if errorlevel 1 (
    set /a attempt+=1
    echo 等待后端服务启动中... (%attempt%/%max_attempts%)
    timeout /t 1 /nobreak > nul
    goto wait_loop
)

echo 后端服务已启动！

echo 启动前端服务...
cd frontend
set PYTHONPATH=%PYTHONPATH%;%CD%\..
streamlit run app.py