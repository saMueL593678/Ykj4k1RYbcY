# 代码生成时间: 2025-09-01 12:45:17
# coding: utf-8
"""
User Login System using Falcon framework.
"""

import falcon
import json

# A simple in-memory user database for demonstration purposes.
USERS = {
    "user1": "password1",
    "user2": "password2",
}

class UserLoginResource:
    """Handles user login requests."""
    def on_post(self, req, resp):
        """Handles POST requests to /login."""
        try:
            # Parse the request body as JSON.
            user_login_data = json.loads(req.bounded_stream.read())
            username = user_login_data.get("username")
            password = user_login_data.get("password")

            # Check if the credentials are valid.
            if username in USERS and USERS[username] == password:
                # Login successful.
                resp.media = {"message": "Login successful"}
                resp.status = falcon.HTTP_OK
            else:
                # Login failed due to invalid credentials.
                resp.media = {"error": "Invalid username or password"}
                resp.status = falcon.HTTP_UNAUTHORIZED
        except json.JSONDecodeError:
            # Handle JSON decode error.
            resp.media = {"error": "Invalid JSON data"}
            resp.status = falcon.HTTP_BAD_REQUEST
        except Exception as e:
            # Handle any other exceptions.
            resp.media = {"error": str(e)}
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR

# Falcon app setup.
app = falcon.App()
app.add_route('/login', UserLoginResource())