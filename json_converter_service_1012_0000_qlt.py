# 代码生成时间: 2025-10-12 00:00:17
# -*- coding: utf-8 -*-

"""
JSON Converter Service using Falcon framework
"""

import falcon
import json
from falcon import API

class JsonConverterResource:
    """
    Falcon resource for handling JSON data conversion
    """

    def on_post(self, req, resp):
        """
        Handle POST requests to convert JSON data
        """
        # Check if the request's body is empty
        if not req.bounded_stream:
            raise falcon.HTTPBadRequest('Empty request body', 'No data provided')

        try:
            # Attempt to parse the JSON data from the request body
            data = req.bounded_stream.read()
            json_data = json.loads(data)

            # Convert the JSON data to a string and send it back as a response
            resp.body = json.dumps(json_data)
            resp.status = falcon.HTTP_200
        except json.JSONDecodeError as e:
            # If there's an error in parsing the JSON data, raise a BAD REQUEST
            raise falcon.HTTPBadRequest('Invalid JSON format', str(e))

# Initialize the Falcon API
api = API()

# Add a resource to the API
api.add_route('/json', JsonConverterResource())

# Export this service to be run by a WSGI server
if __name__ == '__main__':
    import wsgiref.simple_server as wsgiref

    # Start the API service
    wsgiref.make_server('0.0.0.0', 8000) serve api