from PIL import Image, ImageDraw, ImageFont
import logging
import textwrap
import base64
import requests
from io import BytesIO
import traceback
import platform
import os

logger = logging.getLogger(__name__)

class ImageService:
    def __init__(self):
        """初始化图片服务"""
        self.custom_font_path = os.getenv('CUSTOM_FONT_PATH')  # 可以通过环境变量配置自定义字体
        self.font_size = 30
        self.system_fonts = self._get_system_fonts()
        
    def _get_system_fonts(self):
        """获取系统字体列表"""
        system = platform.system()
        if system == "Darwin":  # macOS
            return [
                "/System/Library/Fonts/PingFang.ttc",  # PingFang
                "/System/Library/Fonts/STHeiti Light.ttc",  # Heiti
                "/System/Library/Fonts/Hiragino Sans GB.ttc"  # Hiragino
            ]
        elif system == "Windows":
            return [
                "C:\\Windows\\Fonts\\msyh.ttc",  # Microsoft YaHei
                "C:\\Windows\\Fonts\\simhei.ttf",  # SimHei
                "C:\\Windows\\Fonts\\simsun.ttc"  # SimSun
            ]
        return []  # 其他系统返回空列表

    def _get_font(self, size=20):
        """获取字体，优先使用配置的自定义字体，否则尝试系统字体"""
        try:
            # 首先尝试使用自定义字体
            if self.custom_font_path and os.path.exists(self.custom_font_path):
                logger.info(f"使用自定义字体: {self.custom_font_path}")
                return ImageFont.truetype(self.custom_font_path, size)
            
            # 尝试系统字体
            for font_path in self.system_fonts:
                if os.path.exists(font_path):
                    logger.info(f"使用系统字体: {font_path}")
                    return ImageFont.truetype(font_path, size)
            
            # 如果都失败了，使用默认字体
            logger.warning("未找到合适的字体，使用默认字体")
            return ImageFont.load_default()
            
        except Exception as e:
            logger.error(f"加载字体失败: {str(e)}")
            return ImageFont.load_default()

    async def create_postcard(self, image_url: str, text: str) -> str:
        """创建明信片样式图片"""
        try:
            logger.info(f"开始处理图片，文本长度: {len(text)}")
            
            # 获取图片
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            
            # 计算新图片尺寸
            text_height = max(200, len(text) * 2)  # 根据文本长度动态调整文本区域高度
            new_height = image.height + text_height
            new_image = Image.new('RGB', (image.width, new_height), 'white')
            new_image.paste(image, (0, 0))
            
            # 创建绘图对象
            draw = ImageDraw.Draw(new_image)
            
            # 获取字体
            font = self._get_font(self.font_size)
            
            # 文本换行处理
            margin = 40  # 左右边距
            max_width = image.width - (margin * 2)
            avg_char_width = font.getlength("测")  # 使用中文字符计算平均字符宽度
            chars_per_line = int(max_width / avg_char_width)
            wrapped_text = textwrap.fill(text, width=chars_per_line)
            
            # 获取文本尺寸
            text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height_actual = text_bbox[3] - text_bbox[1]
            
            # 计算文本位置
            x = (image.width - text_width) / 2
            y = image.height + ((text_height - text_height_actual) / 2)
            
            # 绘制文本背景
            padding = 20
            background_bbox = (
                x - padding,
                y - padding,
                x + text_width + padding,
                y + text_height_actual + padding
            )
            draw.rectangle(background_bbox, fill='white')
            
            # 绘制文本
            draw.multiline_text(
                (x, y),
                wrapped_text,
                font=font,
                fill='black',
                align='center',
                spacing=10
            )
            
            # 记录调试信息
            logger.debug(f"图片尺寸: {image.width}x{image.height}")
            logger.debug(f"新图片尺寸: {new_image.width}x{new_height}")
            logger.debug(f"文本框尺寸: {text_bbox}")
            logger.debug(f"计算的文本位置: x={x}, y={y}")
            logger.debug(f"换行后的文本:\n{wrapped_text}")
            
            # 转换为base64
            buffered = BytesIO()
            new_image.save(buffered, format="JPEG", quality=95)
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            logger.info("成功创建明信片样式图片")
            return f"data:image/jpeg;base64,{img_str}"
            
        except Exception as e:
            logger.error(f"创建明信片失败: {str(e)}")
            logger.error(traceback.format_exc())
            return None
    
    def resize_image(self, image: Image.Image, width: int, height: int) -> Image.Image:
        """调整图片大小"""
        return image.resize((width, height), Image.Resampling.LANCZOS)