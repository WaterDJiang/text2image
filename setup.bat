@echo off
echo 创建虚拟环境...
python -m venv venv

echo 激活虚拟环境...
call venv\Scripts\activate.bat

echo 配置环境变量...
if not exist .env (
    echo DEEPSEEK_API_KEY=sk-28eb8b72a1014cb4822c9fa005a54f95> .env
    echo DEEPSEEK_API_BASE=https://api.deepseek.com>> .env
    echo 创建了新的.env文件
) else (
    echo .env文件已存在
)

echo 安装基础依赖...
pip install wheel setuptools

echo 安装GTK和Cairo...
:: 下载并安装GTK运行时
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases/download/2021-04-29/gtk3-runtime-3.24.29-2021-04-29-ts-win64.exe' -OutFile 'gtk3-runtime.exe'"
start /wait gtk3-runtime.exe /S
del gtk3-runtime.exe

echo 安装依赖...
pip install -r requirements.txt

echo 安装完成！
pause 