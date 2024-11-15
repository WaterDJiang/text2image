@echo off
echo 正在启动 AI 图片处理服务...

:: 启动后端服务
echo 启动后端服务...
cd backend
call venv\Scripts\activate
pip install -r requirements.txt
start python run.py

:: 启动前端服务
echo 启动前端服务...
cd ../frontend
call npm install
start npm run dev

echo 服务启动完成！
echo 前端服务地址: http://localhost:5173
echo 后端服务地址: http://localhost:8000 