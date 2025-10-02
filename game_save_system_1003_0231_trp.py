# 代码生成时间: 2025-10-03 02:31:23
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Game Save System
A simple game save system using Falcon framework.
"""

import falcon
import json
import os

# Define the path where game saves will be stored
SAVES_DIRECTORY = 'game_saves'

# Ensure the game saves directory exists
if not os.path.exists(SAVES_DIRECTORY):
    os.makedirs(SAVES_DIRECTORY)

# Define the API resource
class GameSaveResource:
    """Handles game save operations."""
    def on_get(self, req, resp, game_id):
        """Retrieve a game save."""
        save_path = os.path.join(SAVES_DIRECTORY, f'{game_id}.save')
        if not os.path.exists(save_path):
            raise falcon.HTTPNotFound(
                "Game save not found", "No game save found for the given ID.")
        with open(save_path, 'r') as file:
            save_data = file.read()
        resp.body = json.dumps(save_data)
        resp.status = falcon.HTTP_OK

    def on_post(self, req, resp, game_id):
        """Create a new game save."""
        save_path = os.path.join(SAVES_DIRECTORY, f'{game_id}.save')
        try:
            save_data = req.bounded_stream.read()
            with open(save_path, 'w') as file:
                file.write(save_data)
            resp.status = falcon.HTTP_CREATED
        except Exception as e:
            raise falcon.HTTPError(falcon.HTTP_500, "Internal Server Error", str(e))

    def on_delete(self, req, resp, game_id):
        """Delete a game save."""
        save_path = os.path.join(SAVES_DIRECTORY, f'{game_id}.save')
        try:
            os.remove(save_path)
            resp.status = falcon.HTTP_OK
        except FileNotFoundError:
            raise falcon.HTTPNotFound(
                "Game save not found", "No game save found for the given ID.")
        except Exception as e:
            raise falcon.HTTPError(falcon.HTTP_500, "Internal Server Error", str(e))

# Initialize the Falcon API
api = falcon.API()

# Add the game save resource to the API
api.add_route('/saves/{game_id}', GameSaveResource())
