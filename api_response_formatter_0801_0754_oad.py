# 代码生成时间: 2025-08-01 07:54:03
import falcon


class ApiResponseFormatter:
    """
    A formatter class that standardizes API responses.
    It helps in returning responses in a consistent and
    easily understandable format.
    """
    def __init__(self):
        # Initialize the formatter with default message and status
        self.default_message = 'Success'
        self.default_status = falcon.HTTP_200

    def format_response(self, data, message=None, status=None):
        """
        Format the data into a standardized response format.
# 添加错误处理
        :param data: The data to be formatted into the response.
        :param message: An optional message to be included in the response.
        :param status: An optional status code to be included in the response.
# 添加错误处理
        :return: A formatted response dictionary.
        """
        if message is None:
            message = self.default_message
        if status is None:
            status = self.default_status
# 优化算法效率

        return {
            'status': status,
            'message': message,
            'data': data
        }

    def format_error(self, error, message=None, status=None):
        """
        Format an error into a standardized error response format.
        :param error: The error object to be formatted into the response.
        :param message: An optional message to be included in the response.
        :param status: An optional status code to be included in the response.
# TODO: 优化性能
        :return: A formatted error response dictionary.
        """
        if message is None:
            message = 'Error'
        if status is None:
            status = falcon.HTTP_400

        return {
            'status': status,
            'message': message,
            'error': str(error)
        }
# NOTE: 重要实现细节


# Example usage of ApiResponseFormatter
if __name__ == '__main__':
    formatter = ApiResponseFormatter()
# 优化算法效率

    # Sample successful response
    response = formatter.format_response({"key": "value"}, message="Operation Successful")
    print(response)

    # Sample error response
    error_response = formatter.format_error(ValueError("Invalid input"), status=falcon.HTTP_400)
    print(error_response)