from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import base64
import os
import logging
import json
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import imghdr

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

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
            logger.error("No image file in request")
            return jsonify({'error': '没有上传图片'}), 400
        
        if 'type' not in request.form:
            logger.error("No type specified in request")
            return jsonify({'error': '未生成类型'}), 400
        
        image = request.files['image']
        if image.filename == '':
            logger.error("Empty filename")
            return jsonify({'error': '未选择文件'}), 400

        # 验证文件类型
        if not allowed_file(image.filename):
            logger.error(f"Invalid file type: {image.filename}")
            return jsonify({'error': '不支持的文件格式，请上传 JPG、PNG、GIF 或 WEBP 格式的图片'}), 400

        # 验证文件内容
        if not validate_image(image.stream):
            logger.error("Invalid image content")
            return jsonify({'error': '文件内容无效，请上传有效的图片文件'}), 400

        # 检查文件大小
        image.seek(0, 2)  # 移动到文件末尾
        size = image.tell()  # 获取文件大小
        image.seek(0)  # 重置文件指针
        
        if size > MAX_CONTENT_LENGTH:
            logger.error(f"File too large: {size} bytes")
            return jsonify({'error': '图片大小不能超过 5MB'}), 400

        # 准备上传到 ImgBB
        try:
            imgbb_url = f"https://api.imgbb.com/1/upload?key={IMGBB_API_KEY}"
            files = {'image': (secure_filename(image.filename), image.read(), image.content_type)}
            
            # 添加超时设置
            response = requests.post(imgbb_url, files=files, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"ImgBB upload failed: Status {response.status_code}, Response: {response.text}")
                return jsonify({'error': '图片上传失败，请重试'}), 500
            
            image_url = response.json()['data']['url']
            logger.debug(f"Image uploaded successfully: {image_url}")
            
        except requests.Timeout:
            logger.error("ImgBB upload timeout")
            return jsonify({'error': '图片上传超时，请重试'}), 500
        except requests.RequestException as e:
            logger.error(f"ImgBB upload error: {str(e)}")
            return jsonify({'error': '图片上传失败，请检查网络连接'}), 500
        except Exception as e:
            logger.error(f"Unexpected error during upload: {str(e)}", exc_info=True)
            return jsonify({'error': '图片上传过程中出错'}), 500

        generation_type = request.form['type']
        logger.debug(f"Generation type: {generation_type}")

        # Call Coze API
        try:
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
            
            logger.debug(f"Calling Coze API with data: {json.dumps(coze_data)}")
            coze_response = requests.post(API_URL, json=coze_data, headers=headers)
            logger.debug(f"Coze API response status: {coze_response.status_code}")
            logger.debug(f"Coze API response text: {coze_response.text}")
            
            if coze_response.status_code != 200:
                error_message = str(coze_response.text)
                logger.error(f"Coze API error: Status {coze_response.status_code}, Response: {error_message}")
                if '忘记充值' in error_message:
                    return jsonify({
                        'error': '主人忘记充值了，想不出文案',
                        'type': 'recharge'
                    }), 400
                return jsonify({'error': f'生成失败: {error_message}'}), 500
            
            result = coze_response.json()
            logger.debug(f"Parsed result: {result}")
            
            # 获取返回的数据
            data = result.get('data', '')
            try:
                # 尝试解析数据中的 JSON 字符串
                if isinstance(data, str):
                    data_json = json.loads(data)
                    if '忘记充值' in str(data_json.get('output', '')):
                        return jsonify({
                            'error': '主人忘记充值了，想不出文案',
                            'type': 'recharge'
                        }), 400
                    return jsonify(data_json)
                return jsonify(data)
            except json.JSONDecodeError:
                # 如果不是 JSON 字符串，直接返回
                return jsonify({'output': data})
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error during Coze API call: {str(e)}", exc_info=True)
            return jsonify({'error': '网络请求失败，请稍后重试'}), 500
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}", exc_info=True)
            return jsonify({'error': '返回数据格式错误'}), 500
        except Exception as e:
            logger.error(f"Unexpected error during Coze API call: {str(e)}", exc_info=True)
            return jsonify({'error': str(e)}), 500
            
    except Exception as e:
        logger.error(f"Unexpected error in upload_image: {str(e)}", exc_info=True)
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