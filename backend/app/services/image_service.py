from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import textwrap
import os
import logging
import platform

# 获取logger实例
logger = logging.getLogger(__name__)

class ImageService:
    """图片处理服务"""
    
    def _get_system_font(self):
        """
        获取系统默认中文字体
        """
        system = platform.system()
        if system == "Windows":
            # Windows 默认中文字体
            font_paths = [
                "C:\\Windows\\Fonts\\msyh.ttc",  # 微软雅黑
                "C:\\Windows\\Fonts\\simsun.ttc",  # 宋体
            ]
        elif system == "Darwin":  # macOS
            font_paths = [
                "/System/Library/Fonts/PingFang.ttc",  # 苹方
                "/System/Library/Fonts/STHeiti Light.ttc",  # 华文黑体
            ]
        else:  # Linux
            font_paths = [
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",  # Noto Sans CJK
                "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",  # Droid Sans
            ]
        
        # 尝试加载系统字体
        for font_path in font_paths:
            try:
                if os.path.exists(font_path):
                    return ImageFont.truetype(font_path, 24)
            except Exception as e:
                logger.warning(f"加载字体 {font_path} 失败: {str(e)}")
        
        # 如果没有找到合适的字体，返回默认字体
        logger.warning("未找到系统中文字体，使用默认字体")
        return ImageFont.load_default()
    
    def create_postcard(self, image_url: str, text: str) -> bytes:
        """
        创建明信片风格的图文组合
        
        Args:
            image_url: 原始图片URL
            text: 要添加的文字
            
        Returns:
            bytes: 生成的图片二进制数据
        """
        try:
            # 下载原始图片
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            
            # 调整图片大小，保持比例
            base_width = 800
            w_percent = base_width / float(img.size[0])
            h_size = int(float(img.size[1]) * float(w_percent))
            img = img.resize((base_width, h_size), Image.Resampling.LANCZOS)
            
            # 创建新的画布，底色为白色
            margin = 40  # 边距
            text_height = 200  # 文字区域高度
            canvas = Image.new('RGB', 
                             (base_width + 2*margin, 
                              h_size + 2*margin + text_height), 
                             'white')
            
            # 粘贴原图
            canvas.paste(img, (margin, margin))
            
            # 添加文字
            draw = ImageDraw.Draw(canvas)
            
            # 获取系统字体
            font = self._get_system_font()
            font_size = 24 if font != ImageFont.load_default() else 16
            
            # 文字换行处理
            wrapper = textwrap.TextWrapper(width=40)  # 每行大约40个字符
            text_lines = wrapper.wrap(text)
            
            # 计算文字位置并绘制
            text_y = margin + h_size + 40
            for line in text_lines:
                # 使用 getsize 替代 getlength（兼容旧版本PIL）
                try:
                    text_width = font.getlength(line)
                except AttributeError:
                    text_width, _ = font.getsize(line)
                    
                text_x = margin + (base_width - text_width) / 2  # 居中对齐
                draw.text((text_x, text_y), line, font=font, fill='black')
                text_y += font_size + 10
            
            # 添加装饰边框
            border_width = 2
            draw.rectangle(
                [(margin-border_width, margin-border_width),
                 (margin+base_width+border_width, margin+h_size+text_height+border_width)],
                outline='#CCCCCC',
                width=border_width
            )
            
            # 转换为二进制数据
            output = BytesIO()
            canvas.save(output, format='PNG')
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"创建明信片失败: {str(e)}")
            return None
    
    def resize_image(self, image: Image.Image, width: int, height: int) -> Image.Image:
        """调整图片大小"""
        return image.resize((width, height), Image.Resampling.LANCZOS)