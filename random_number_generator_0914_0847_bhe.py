# 代码生成时间: 2025-09-14 08:47:43
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Random Number Generator Service using Falcon Framework
"""

import falcon
import random
import json
from falcon import HTTP_400, HTTP_200, HTTP_500

# 定义一个资源类
class RandomNumberResource:
    """Generates a random number"""
    def on_get(self, req, resp):
        """Handles GET requests"""
        try:
            # 设置随机数的范围
            min_value = req.get_param('min', default=0)
            max_value = req.get_param('max', default=100)
            
            # 校验参数
            if min_value >= max_value:
                raise ValueError('min must be less than max')
            
            # 生成随机数
            random_number = random.randint(min_value, max_value)
            
            # 构建响应体
            resp.media = {'number': random_number}
            resp.status = HTTP_200
        except ValueError as e:
            # 错误处理，返回400错误
            resp.media = {'error': str(e)}
            resp.status = HTTP_400
        except Exception as e:
            # 其他异常处理，返回500错误
            resp.media = {'error': 'Internal Server Error'}
            resp.status = HTTP_500

# 创建应用实例
app = falcon.App()

# 将资源添加到应用
app.add_route('/random', RandomNumberResource())
