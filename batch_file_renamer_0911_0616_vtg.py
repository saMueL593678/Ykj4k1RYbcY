# 代码生成时间: 2025-09-11 06:16:48
import os
import sys
from falcon import Falcon, Request, Response

# 批量文件重命名工具配置类
class RenamerConfig:
    def __init__(self, directory, prefix):
        self.directory = directory
        self.prefix = prefix

# 批量文件重命名工具
class BatchFileRenamer:
    def __init__(self, config):
        self.config = config

    def rename_files(self):
        """重命名指定目录下的所有文件"""
        try:
            for filename in os.listdir(self.config.directory):
                file_path = os.path.join(self.config.directory, filename)
                if os.path.isfile(file_path):
                    new_filename = f"{self.config.prefix}_{filename}"
                    new_file_path = os.path.join(self.config.directory, new_filename)
                    os.rename(file_path, new_file_path)
        except OSError as e:
            print(f"Error renaming files: {e}")
            sys.exit(1)

# FALCON API 路由
class RenamerResource:
    def on_get(self, req: Request, resp: Response):
        "