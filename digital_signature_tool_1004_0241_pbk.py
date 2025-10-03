# 代码生成时间: 2025-10-04 02:41:25
# digital_signature_tool.py
# This tool uses the Falcon framework to provide a digital signature service.

import falcon
import jwt  # PyJWT library is used for generating and verifying JWT tokens
from datetime import datetime, timedelta
from urllib.parse import quote_plus

# Falcon API resource class for handling signature requests
class SignatureResource:
    """
    Handles the creation and verification of digital signatures.
    """

    def on_post(self, req, resp):
        try:
            # Get the signing key and payload from the request body
            signing_key = req.get_param('signing_key')
            payload = req.get_param('payload')

            # Check if the required parameters are provided
            if not signing_key or not payload:
                raise falcon.HTTPBadRequest('Missing parameters', 'Signing key and payload are required.')

            # Generate a JWT token with the payload and the provided signing key
            token = jwt.encode(payload, signing_key, algorithm='HS256')
            resp.body = token
            resp.status = falcon.HTTP_200

        except jwt.PyJWTError as e:
            # Handle JWT errors
            resp.body = str(e)
            resp.status = falcon.HTTP_400

    def on_get(self, req, resp):
        try:
            # Get the token to be verified from the query parameter
            token_to_verify = req.get_param('token')

            # Check if the token is provided
            if not token_to_verify:
                raise falcon.HTTPBadRequest('Missing parameter', 'Token is required.')

            # Verify the JWT token
            signing_key = req.get_param('signing_key')
            jwt.decode(token_to_verify, signing_key, algorithms=['HS256'])

            resp.body = 'Token is valid.'
            resp.status = falcon.HTTP_200

        except jwt.ExpiredSignatureError:
            # Handle expired token errors
            resp.body = 'Token has expired.'
            resp.status = falcon.HTTP_401
        except jwt.InvalidTokenError:
            # Handle invalid token errors
            resp.body = 'Invalid token.'
            resp.status = falcon.HTTP_400

# Instantiate the Falcon API object
app = falcon.API()

# Add the SignatureResource to the API
app.add_route('/sign', SignatureResource())
app.add_route('/verify', SignatureResource())

# Below is the code for running the application in a local server,
# but in a production environment, you would typically use a WSGI server.
if __name__ == '__main__':
    import wsgiref.simple_server
    
    # Create a WSGI server to serve the Falcon app
    httpd = wsgiref.simple_server.make_server('127.0.0.1', 8000, app)
    print('Serving on http://127.0.0.1:8000')
    httpd.serve_forever()