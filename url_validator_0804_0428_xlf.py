# 代码生成时间: 2025-08-04 04:28:50
# url_validator.py
#
# This script is designed to validate the URL using the FALCON framework in Python.
# It includes error handling and follows best practices for readability and maintainability.

import falcon
import requests
from urllib.parse import urlparse, parse_qs
from falcon import HTTP_400, HTTP_404, HTTP_200, HTTP_500

class URLValidator:
    """
    A Falcon resource class to validate URL links.
    """
    def on_get(self, req, resp):
        # Check if URL parameter is provided in the query string
        query_params = req.query_string
        if not query_params or 'url' not in query_params:
            raise falcon.HTTPBadRequest('URL parameter is missing', 'Please provide a URL parameter.')

        # Extract the URL from the query string
        url_to_validate = parse_qs(query_params)['url'][0]
        try:
            # Use the requests.head method to validate the URL without downloading the content
            response = requests.head(url_to_validate, allow_redirects=True)
            # Check if the URL is valid based on the HTTP status code
            if response.status_code == 200:
                resp.status = HTTP_200
                resp.media = {'message': 'URL is valid'}
            else:
                resp.status = HTTP_404
                resp.media = {'message': 'URL is invalid or not found'}
        except requests.exceptions.RequestException as e:
            # Handle any exceptions that occur during the request
            resp.status = HTTP_500
            resp.media = {'message': 'Error validating URL', 'error': str(e)}

# Initialize the Falcon API
api = falcon.API()

# Add the URLValidator resource to the API with the corresponding route
api.add_route('/validate_url', URLValidator())


# Run the API if this script is executed directly
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('0.0.0.0', 8000, api)
    print('Serving on port 8000...')
    httpd.serve_forever()