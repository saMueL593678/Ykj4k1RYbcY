# 代码生成时间: 2025-09-06 00:39:51
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Image Resizer using the FALCON framework.
This script allows for batch resizing of images.
"""

import falcon
import os
from PIL import Image
from io import BytesIO
from flask import send_file
import logging

# Configuration
IMAGE_DIR = 'images/'  # Directory containing input images
OUTPUT_DIR = 'resized/'  # Directory for output resized images

class ImageResizer:
    """
    A class that handles image resizing.
    """
    def __init__(self):
        self.image_dir = IMAGE_DIR
        self.output_dir = OUTPUT_DIR

    def resize_image(self, image_path, size):
        """
        Resize an image to a specified size.
        :param image_path: The path to the image file.
        :param size: A tuple containing the new width and height.
        :return: The path to the resized image file.
        """
        try:
            with Image.open(image_path) as img:
                img = img.resize(size, Image.ANTIALIAS)
                file_name = os.path.basename(image_path)
                output_path = os.path.join(self.output_dir, file_name)
                img.save(output_path)
                return output_path
        except IOError:
            logging.error(f"Error resizing image {image_path}")
            raise

class ResizeResource:
    """
    A Falcon resource for resizing images.
    """
    def __init__(self):
        self.resizer = ImageResizer()

    def on_get(self, req, resp, image_name):
        """
        Handle GET requests to resize an image.
        :param req: The incoming request.
        :param resp: The outgoing response.
        :param image_name: The name of the image to resize.
        """
        image_path = os.path.join(self.resizer.image_dir, image_name)
        if not os.path.exists(image_path):
            raise falcon.HTTPNotFound("Image not found")

        try:
            resized_image_path = self.resizer.resize_image(image_path, (800, 600))
            resp.body = BytesIO()
            resp.content_type = "image/jpeg"
            resp.status = falcon.HTTP_OK
            return send_file(resized_image_path, as_attachment=True)
        except Exception as e:
            raise falcon.HTTPInternalServerError("Error resizing image", e)

# Initialize Falcon API
api = falcon.API()

# Add the resource
api.add_route('/images/{image_name}', ResizeResource())

# Start the Falcon app
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8000, api)
    print("Starting Falcon image resizer on localhost:8000")
    httpd.serve_forever()