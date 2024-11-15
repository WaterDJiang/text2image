from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import base64
import os
import logging
import json
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from PIL import Image
import io
import time

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 从环境变量获取敏感信息
API_URL = os.getenv('COZE_API_URL', 'https://api.coze.cn/v1/workflow/run')
API_KEY = os.getenv('COZE_API_KEY')
IMGBB_API_KEY = os.getenv('IMGBB_API_KEY')

# 不同功能对应的 workflow_id
WORKFLOWS = {
    'mood': os.getenv('WORKFLOW_ID_MOOD'),
    'sarcastic': os.getenv('WORKFLOW_ID_SARCASTIC'),
    'poetry': os.getenv('WORKFLOW_ID_POETRY'),
    'story': os.getenv('WORKFLOW_ID_STORY'),
}

# 验证必要的环境变量是否存在
required_vars = ['COZE_API_KEY', 'IMGBB_API_KEY', 'WORKFLOW_ID_MOOD']
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
    logger.error(error_msg)
    raise ValueError(error_msg)

# 添加配置
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# 在现有的环境变量配置后添加
VERCEL_ENV = os.getenv('VERCEL_ENV', 'development')
VERCEL_URL = os.getenv('VERCEL_URL', 'localhost:5001')
VERCEL_REGION = os.getenv('VERCEL_REGION', 'dev1')
VERCEL_DEPLOYMENT_ID = os.getenv('VERCEL_DEPLOYMENT_ID', '')

# 根据环境设置基础 URL
BASE_URL = f"https://{VERCEL_URL}" if VERCEL_ENV == 'production' else f"http://{VERCEL_URL}"

# 修改 Flask 配置
app.config.update(
    SERVER_NAME=VERCEL_URL if VERCEL_ENV == 'production' else None,
    PREFERRED_URL_SCHEME='https' if VERCEL_ENV == 'production' else 'http'
)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(stream):
    try:
        image = Image.open(stream)
        image.verify()
        stream.seek(0)
        format = image.format.lower()
        if format not in ['jpeg', 'jpg', 'png', 'gif', 'webp']:
            return None
        return '.' + (format if format != 'jpeg' else 'jpg')
    except Exception:
        return None

def upload_to_imgbb(image, max_retries=3):
    for attempt in range(max_retries):
        try:
            imgbb_url = f"https://api.imgbb.com/1/upload?key={IMGBB_API_KEY}"
            files = {'image': (secure_filename(image.filename), image.read(), image.content_type)}
            response = requests.post(imgbb_url, files=files, timeout=10)
            
            if response.status_code == 200:
                return response.json()['data']['url']
            
            logger.warning(f"Upload attempt {attempt + 1} failed: Status {response.status_code}")
            
        except Exception as e:
            logger.error(f"Upload attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries - 1:
                raise
            
        time.sleep(1)  # 等待1秒后重试
    
    raise Exception("Max retries exceeded")

@app.route('/')
def index():
    return redirect(url_for('mood'))

@app.route('/mood')
def mood():
    return render_template('mood.html')

@app.route('/sarcastic')
def sarcastic():
    return render_template('sarcastic.html')

@app.route('/poetry')
def poetry():
    return render_template('coming_soon.html', page_title='诗意看图')

@app.route('/story')
def story():
    return render_template('coming_soon.html', page_title='故事创作')

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': '没有上传图片'}), 400
        
        if 'type' not in request.form:
            return jsonify({'error': '未指定生成类型'}), 400
        
        generation_type = request.form['type']
        logger.debug(f"Generation type: {generation_type}")
        
        if generation_type not in WORKFLOWS:
            return jsonify({'error': '不支持的生成类型'}), 400
        
        image = request.files['image']
        if image.filename == '':
            return jsonify({'error': '未选择文件'}), 400
        
        # Upload to ImgBB
        try:
            imgbb_url = f"https://api.imgbb.com/1/upload?key={IMGBB_API_KEY}"
            files = {'image': (image.filename, image.read(), image.content_type)}
            response = requests.post(imgbb_url, files=files, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"ImgBB upload failed: {response.text}")
                return jsonify({'error': '图片上传失败'}), 500
            
            image_url = response.json()['data']['url']
            logger.debug(f"Image uploaded successfully: {image_url}")
            
            # Call Coze API
            coze_data = {
                "workflow_id": WORKFLOWS[generation_type],
                "parameters": {
                    "BOT_USER_INPUT": image_url
                },
                "is_async": False
            }
            
            headers = {
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            }
            
            coze_response = requests.post(API_URL, json=coze_data, headers=headers)
            logger.debug(f"Coze API response: {coze_response.text}")
            
            if coze_response.status_code != 200:
                return jsonify({'error': '生成失败'}), 500
            
            result = coze_response.json()
            
            # 检查是否包含充值提示
            if '忘记充值' in str(result):
                return jsonify({
                    'error': '主人忘记充值了，想不出文案',
                    'type': 'recharge'
                }), 400
            
            # 解析返回数据
            try:
                data = result.get('data', '')
                if isinstance(data, str):
                    data_json = json.loads(data)
                    if '忘记充值' in str(data_json.get('output', '')):
                        return jsonify({
                            'error': '主人忘记充值了，想不出文案',
                            'type': 'recharge'
                        }), 400
                    return jsonify(data_json)
                return jsonify({'output': data})
            except json.JSONDecodeError:
                return jsonify({'output': data})
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            return jsonify({'error': '网络请求失败，请稍后重试'}), 500
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/history')
def history():
    return render_template('coming_soon.html', page_title='历史记录')

@app.route('/settings')
def settings():
    return render_template('coming_soon.html', page_title='设置')

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5001)), debug=debug_mode) 