# 代码生成时间: 2025-09-18 06:38:24
#!/usr/bin/env python

"""
Access Control Application using Falcon Framework

This application demonstrates basic access control using Falcon.
It allows only authenticated users with a specific role to access certain resources.
"""

import falcon
from falcon import HTTPNotFound
from falcon_auth import FalconAuth

# Define your user database and roles here for demonstration purposes
# In a real application, you would use a database or another data store.
USERS = {
    "user1": {"password": "password1", "role": "admin"},
    "user2": {"password": "password2", "role": "user"},
}

# Define the roles that have access to protected resources
AUTHORIZED_ROLES = ["admin"]

class BasicAuthMiddleware:
    """
    Middleware to handle basic authentication and role-based access control.
    """
    def process_request(self, req, resp):
        # Get the Authorization header
        auth_header = req.headers.get('Authorization')
        if auth_header:
            # Check if the Authorization header is in Basic Auth format
            auth_type, encoded_credentials = auth_header.split(' ', 1)
            if auth_type.lower() == 'basic':
                # Decode the credentials
                decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
                username, password = decoded_credentials.split(':', 1)
                try:
                    # Check if the user exists and the password is correct
                    user = USERS[username]
                    if user['password'] == password:
                        # Check if the user has the required role
                        if user['role'] in AUTHORIZED_ROLES:
                            return
                    else:
                        raise falcon.HTTPForbidden(
                            'User does not have the required role for this resource.',
                            'Only authorized users with specific roles can access this resource.'
                        )
                except KeyError:
                    raise falcon.HTTPUnauthorized(
                        'Authentication failed',
                        'Invalid username or password'
                    )
            else:
                raise falcon.HTTPUnauthorized(
                    'Invalid authentication type',
                    'Only Basic Auth is supported.'
                )
        else:
            raise falcon.HTTPUnauthorized(
                'Authentication required',
                'No Authorization header found.'
            )

# Define a protected resource
class ProtectedResource:
    """
    A protected resource that only allows access to authorized users with specific roles.
    """
    def on_get(self, req, resp):
        # Respond to a GET request
        resp.status = falcon.HTTP_200
        resp.media = {"message": "You have accessed a protected resource."}

# Instantiate the Falcon API
api = falcon.API(middleware=[BasicAuthMiddleware()])

# Add the protected resource to the API
api.add_route('/protected', ProtectedResource())

# Run the API on port 8000
if __name__ == '__main__':
    import socket
    from wsgiref import simple_server

    with socket.setdefaulttimeout(1):
        httpd = simple_server.make_server('0.0.0.0', 8000, api)
        print('Starting API on port 8000...')
        httpd.serve_forever()