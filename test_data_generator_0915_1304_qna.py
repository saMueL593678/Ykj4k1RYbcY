# 代码生成时间: 2025-09-15 13:04:16
import falcon
import json
import random
import string
from datetime import datetime, timedelta


# 测试数据生成器类
class TestDataGenerator:
    def __init__(self):
        # 初始化测试数据生成器
        pass

    def generate_random_string(self, length=10):
        """
        生成随机字符串
        :param length: 字符串长度，默认10
        :return: 随机字符串
        """
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

    def generate_random_number(self, min_value=1, max_value=100):
        """
        生成指定范围内的随机数
        :param min_value: 最小值，默认1
        :param max_value: 最大值，默认100
        :return: 随机数
        """
        return random.randint(min_value, max_value)

    def generate_random_datetime(self, days=30):
        """
        生成随机日期（当前日期前后30天内）
        :param days: 天数，默认30
        :return: 随机日期
        """
        random_days = random.randrange(days * 2) - days
        return datetime.now() + timedelta(days=random_days)

    def generate_test_data(self, num_records=100):
        """
        生成测试数据
        :param num_records: 生成记录数，默认100
        :return: 测试数据列表
        """
        test_data = []
        for _ in range(num_records):
            data = {
                'id': self.generate_random_string(10),
                'name': self.generate_random_string(20),
                'age': self.generate_random_number(18, 60),
                'created_at': self.generate_random_datetime().isoformat()
            }
            test_data.append(data)
        return test_data

# Falcon API 路由和处理函数
api = application = falcon.App()

# 测试数据生成器接口
class TestDataResource:
    def on_get(self, req, resp):
        """
        GET 请求处理函数，生成测试数据并返回
        """
        try:
            generator = TestDataGenerator()
            test_data = generator.generate_test_data()
            resp.media = {'test_data': test_data}
            resp.status = falcon.HTTP_200
        except Exception as e:
            # 错误处理
            resp.media = {'error': str(e)}
            resp.status = falcon.HTTP_500

# 注册路由
api.add_route('/test-data', TestDataResource())
