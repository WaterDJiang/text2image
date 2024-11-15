from PIL import Image

class ImageService:
    """图片处理服务"""
    
    def resize_image(self, image: Image.Image, width: int, height: int) -> Image.Image:
        """
        调整图片大小
        
        Args:
            image: PIL图片对象
            width: 目标宽度
            height: 目标高度
            
        Returns:
            调整大小后的图片对象
        """
        return image.resize((width, height), Image.Resampling.LANCZOS) 