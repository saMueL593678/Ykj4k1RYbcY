# 代码生成时间: 2025-08-24 03:55:10
# math_calculator.py
# A simple math calculator using Falcon framework

from falcon import Falcon, API
from wsgiref.simple_server import make_server

# Define a resource for math operations
class MathCalculator:
    def on_get(self, req, resp):
        """Handle GET requests."""
        try:
            # Extract query parameters
            a = float(req.get_param('a', None))
            b = float(req.get_param('b', None))
            operation = req.get_param('operation', None)

            # Perform the requested operation
            if operation == 'add':
                result = a + b
            elif operation == 'subtract':
                result = a - b
            elif operation == 'multiply':
                result = a * b
            elif operation == 'divide':
                if b == 0:
                    raise ValueError('Cannot divide by zero.')
                result = a / b
            else:
                raise ValueError('Invalid operation.')

            # Return the result in the response
            resp.media = {'result': result}
            resp.status = falcon.HTTP_200
        except ValueError as e:
            # Handle errors and return an error message
            resp.media = {'error': str(e)}
            resp.status = falcon.HTTP_400

# Create an API instance and add the resource
api = API()
api.add_route('/math', MathCalculator())

# Run the Falcon application
if __name__ == '__main__':
    httpd = make_server('localhost', 8000, api)
    print('Starting math calculator on localhost:8000...')
    httpd.serve_forever()