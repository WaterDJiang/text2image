from PIL import Image, ImageDraw, ImageFont
import platform
import logging
from io import BytesIO
from cairosvg import svg2png
from backend.config.settings import IMAGE_WIDTH, IMAGE_HEIGHT
import os

logger = logging.getLogger(__name__)

class ImageService:
    def __init__(self):
        self.font = self._get_system_font()
        
    def _get_system_font(self):
        """获取系统字体"""
        system = platform.system()
        font_paths = []
        
        if system == "Darwin":  # macOS
            font_paths = [
                "/System/Library/Fonts/PingFang.ttc",
                "/System/Library/Fonts/STHeiti Light.ttc",
                "/System/Library/Fonts/STHeiti Medium.ttc",
                "/System/Library/Fonts/Hiragino Sans GB.ttc",
                "/Library/Fonts/Arial Unicode.ttf",
            ]
        elif system == "Windows":
            font_paths = [
                "C:\\Windows\\Fonts\\msyh.ttc",
                "C:\\Windows\\Fonts\\simsun.ttc",
                "C:\\Windows\\Fonts\\simhei.ttf",
            ]
        else:  # Linux
            font_paths = [
                "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                "/usr/share/fonts/wqy-microhei/wqy-microhei.ttc",
            ]
            
        for path in font_paths:
            try:
                if os.path.exists(path):
                    return ImageFont.truetype(path, size=24)
            except Exception as e:
                logger.warning(f"加载字体 {path} 失败: {str(e)}")
                continue
                
        logger.warning("未找到任何系统字体，使用默认字体")
        return ImageFont.load_default()
        
    def create_image_with_svg(self, comment, svg):
        """创建包含评论和SVG的图片"""
        try:
            # 创建底图
            background = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color='#F8F8F8')
            d = ImageDraw.Draw(background)
            
            # 设置边距和基本参数
            padding = 30
            text_top_margin = IMAGE_HEIGHT * 0.1
            
            # 文字自动换行处理
            def wrap_text_with_check(text, max_width, font):
                words = text
                lines = []
                current_line = []
                current_width = 0
                
                for char in words:
                    char_width = font.getlength(char)
                    if current_width + char_width <= max_width - padding * 2:
                        current_line.append(char)
                        current_width += char_width
                    else:
                        lines.append(''.join(current_line))
                        current_line = [char]
                        current_width = char_width
                
                if current_line:
                    lines.append(''.join(current_line))
                    
                return lines
            
            # 计算可用于文字显示的最大宽度
            max_text_width = IMAGE_WIDTH - padding * 2
            
            # 自动换行处理文字
            text_lines = wrap_text_with_check(comment, max_text_width, self.font)
            
            # 计算文字总高度
            line_spacing = self.font.size + 10
            total_text_height = len(text_lines) * line_spacing
            
            # 绘制文字
            current_y = text_top_margin
            for line in text_lines:
                line_width = self.font.getlength(line)
                x_position = (IMAGE_WIDTH - line_width) / 2
                d.text((x_position, current_y), line, font=self.font, fill='#333333')
                current_y += line_spacing
            
            # 计算SVG尺寸和位置
            svg_width = 280
            svg_height = 380
            svg_y = current_y + 50
            
            # 绘制分隔线
            separator_y = current_y + 25
            line_start = padding
            line_end = IMAGE_WIDTH - padding
            
            # 绘制渐变分隔线
            for i in range(2):
                alpha = 255 - (i * 128)
                line_color = (51, 51, 51, alpha)
                d.line(
                    [(line_start, separator_y + i), (line_end, separator_y + i)],
                    fill=line_color,
                    width=1
                )
            
            if svg:
                try:
                    # 将SVG转换为PNG
                    png_data = svg2png(
                        bytestring=svg.encode('utf-8'),
                        output_width=svg_width,
                        output_height=svg_height
                    )
                    
                    svg_image = Image.open(BytesIO(png_data))
                    svg_x = (IMAGE_WIDTH - svg_width) // 2
                    background.paste(svg_image, (svg_x, int(svg_y)))
                    logger.info("SVG渲染成功")
                except Exception as e:
                    logger.error(f"SVG渲染失败: {str(e)}")
                    d.text((padding, svg_y), "SVG渲染失败", font=self.font, fill='red')
            
            return background
            
        except Exception as e:
            logger.error(f"创建图片失败: {str(e)}")
            error_img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color='white')
            d = ImageDraw.Draw(error_img)
            d.text((padding, padding), f"图片生成错误: {str(e)}", font=self.font, fill='red')
            return error_img
        