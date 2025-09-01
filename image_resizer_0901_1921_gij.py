# 代码生成时间: 2025-09-01 19:21:55
import falcon
import os
from PIL import Image
from io import BytesIO

# 图片尺寸批量调整器
class ImageResizer:
    def __init__(self, output_format='JPEG', output_quality=85):
        """
        图片尺寸批量调整器初始化函数。
        :param output_format: 输出图片格式，支持格式为'JPEG'和'PNG'，默认为'JPEG'。
        :param output_quality: 输出图片质量，取值范围0-100，默认为85。
        """
        self.output_format = output_format
        self.output_quality = output_quality

    def resize_image(self, image_path, output_path, size):
        """
        调整单个图片的尺寸。
        :param image_path: 输入图片路径。
        :param output_path: 输出图片路径。
        :param size: 图片尺寸，格式为(width, height)。
        """
        try:
            with Image.open(image_path) as img:
                img.thumbnail(size, Image.ANTIALIAS)
                img.save(output_path, quality=self.output_quality)
                return True
        except IOError as e:
            print(f"Error resizing image {image_path}: {e}")
            return False

    def resize_images(self, input_dir, output_dir, size):
        """
        批量调整文件夹内所有图片的尺寸。
        :param input_dir: 输入文件夹路径。
        :param output_dir: 输出文件夹路径。
        :param size: 图片尺寸，格式为(width, height)。
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        for filename in os.listdir(input_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                input_path = os.path.join(input_dir, filename)
                output_path = os.path.join(output_dir, filename)
                if self.resize_image(input_path, output_path, size):
                    print(f"Image resized: {output_path}")
                else:
                    print(f"Failed to resize image: {output_path}")

# FALCON API端点
class ImageResizerAPI:
    def __init__(self):
        self.resizer = ImageResizer()

    def on_get(self, req, resp):
        "