from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import textwrap
import os
import logging
import platform
import traceback
import base64
import httpx

logger = logging.getLogger(__name__)

class ImageService:
    def __init__(self):
        # 根据操作系统选择字体
        if platform.system() == "Darwin":  # macOS
            self.font_path = "/System/Library/Fonts/STHeiti Light.ttc"  # 使用华文黑体
        elif platform.system() == "Windows":
            self.font_path = "C:\\Windows\\Fonts\\simhei.ttf"  # 使用黑体
        else:  # Linux
            self.font_path = "/usr/share/fonts/truetype/arphic/uming.ttc"  # 使用文鼎明体
            
    async def create_postcard(self, image_url: str, text: str) -> str:
        """
        创建明信片样式的图片
        :param image_url: 原始图片URL
        :param text: 要添加的文本
        :return: base64编码的图片
        """
        try:
            # 下载原始图片
            async with httpx.AsyncClient() as client:
                response = await client.get(image_url)
                response.raise_for_status()
                image_data = response.content

            # 打开图片
            image = Image.open(BytesIO(image_data))
            
            # 调整图片大小，保持宽高比
            max_size = (1200, 1200)  # 增加图片尺寸
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # 创建新的画布，底部留出空间给文字
            text_height = 300  # 增加文字区域高度
            new_image = Image.new('RGB', (image.width, image.height + text_height), 'white')
            new_image.paste(image, (0, 0))
            
            # 创建绘图对象
            draw = ImageDraw.Draw(new_image)
            
            # 设置字体
            try:
                font_size = 48  # 增大字体大小
                font = ImageFont.truetype(self.font_path, font_size)
                logger.info(f"成功加载字体: {self.font_path}")
            except Exception as e:
                logger.error(f"加载字体失败: {str(e)}, 尝试加载备用字体")
                # 尝试加载备用字体
                backup_fonts = [
                    "/System/Library/Fonts/PingFang.ttc",
                    "/System/Library/Fonts/Hiragino Sans GB.ttc",
                    "C:\\Windows\\Fonts\\msyh.ttf",
                    "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf"
                ]
                for backup_font in backup_fonts:
                    try:
                        font = ImageFont.truetype(backup_font, font_size)
                        logger.info(f"成功加载备用字体: {backup_font}")
                        break
                    except Exception:
                        continue
                else:
                    logger.error("所有字体加载失败，使用默认字体")
                    font = ImageFont.load_default()
            
            # 文本换行处理
            margin = 40  # 增加边距
            text_width = image.width - 2 * margin
            wrapped_text = textwrap.fill(text, width=20)  # 减少每行字数以增大字体
            
            # 计算文本位置（居中）
            text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height_actual = text_bbox[3] - text_bbox[1]
            
            x = (image.width - text_width) / 2
            y = image.height + (text_height - text_height_actual) / 2
            
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
                spacing=10  # 增加行间距
            )
            
            # 转换为base64
            buffered = BytesIO()
            new_image.save(buffered, format="JPEG", quality=95)  # 提高图片质量
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