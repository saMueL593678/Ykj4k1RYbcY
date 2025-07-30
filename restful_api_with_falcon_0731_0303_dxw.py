# 代码生成时间: 2025-07-31 03:03:27
# restful_api_with_falcon.py
# This file contains an example of a RESTful API using the Falcon framework in Python.

import falcon
from falcon import status, media, testing

# Define a resource class for our API endpoint
class HelloWorld(object):
    """
    Handles HTTP requests to the /hello endpoint.
    """
    def on_get(self, req, resp):
        """
        Handles GET requests.
        """
        # Set the response body and status code
        resp.status = falcon.HTTP_200  # 200 OK
        resp.media = {"message": "Hello, World!"}

# Create an API instance
api = application = falcon.App()

# Add the resource class to the API
api.add_route('/hello', HelloWorld())

# Test the API
class HelloWorldTest(testing.TestBase):
    """"
    A simple test case for our HelloWorld resource.
    """"
    def test_hello_world(self):
        """
        Test that we return a 200 response to a GET request.
        """
        result = self.simulate_request(path='/hello')
        self.assertEqual(result.status, falcon.HTTP_200)
        self.assertIsInstance(result.json, dict)
        self.assertEqual(result.json, {'message': 'Hello, World!'})

# Run the API if this file is executed directly
if __name__ == '__main__':
    import sys
    from wsgiref.simple_server import make_server

    # Start the API on port 8000
    httpd = make_server('0.0.0.0', 8000, application)
    print('Serving on port 8000...')
    httpd.serve_forever()