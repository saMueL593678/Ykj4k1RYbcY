# 代码生成时间: 2025-08-07 20:45:07
import falcon
import xlsxwriter
import os
from datetime import datetime

# 定义全局变量
OUTPUT_DIR = "./output"  # 输出目录
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# 异常处理类
class ExcelGeneratorError(Exception):
    """自定义异常类"""
    def __init__(self, message="Excel generation failed"):
        self.message = message
        super().__init__(self.message)

# Excel表格自动生成器
class ExcelGenerator:
    def __init__(self, filename, data):
        "