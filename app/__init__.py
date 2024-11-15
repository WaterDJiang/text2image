from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import ProductionConfig
import logging

def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    # 配置限流器
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    
    # 注册蓝图
    from app.routes import main, api
    app.register_blueprint(main.bp)
    app.register_blueprint(api.bp, url_prefix='/api')
    
    # 错误处理
    @app.errorhandler(413)
    def request_entity_too_large(error):
        return {'error': '文件大小超过限制'}, 413
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': '服务器内部错误'}, 500
    
    return app 