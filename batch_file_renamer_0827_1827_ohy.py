# 代码生成时间: 2025-08-27 18:27:53
#!/usr/bin/env python3

"""
Batch File Renamer Tool

A Python script using the Falcon framework to create a REST API for batch file renaming.
It allows users to send a JSON payload with a list of file names to rename and a target directory.
The API will then attempt to rename the files accordingly.

Usage:
    curl -X POST -H 'Content-Type: application/json' \
      -d '["old_name1.txt", "old_name2.txt"]' \
      http://localhost:8000/rename

Limitations:
    - Files must be in the same directory as the script for simplicity.
    - No error checking on file existence before renaming.
    - No checking for file name conflicts after renaming.
"""

import os
import json
import falcon

class FileRenamer:
    """Handles file renaming operations."""
    def __init__(self):
        self.dirname = os.getcwd()  # Assuming files are in the script's directory.

    def on_post(self, req, resp):
        """Handles POST requests to rename files."""
        try:
            file_names = json.load(req.bounded_stream)
            if not isinstance(file_names, list):
                raise ValueError('Expected a list of file names')

            for old_name in file_names:
                new_name = self.generate_new_name(old_name)
                try:
                    os.rename(os.path.join(self.dirname, old_name), 
                               os.path.join(self.dirname, new_name))
                except FileNotFoundError:
                    raise falcon.HTTPError(falcon.HTTP_404, "File not found", "File not found: {}".format(old_name))
                except OSError as e:
                    raise falcon.HTTPError(falcon.HTTP_500, 
                                         "Internal Server Error", str(e))

            resp.status = falcon.HTTP_200
            resp.media = {"message": "Files renamed successfully"}
        except json.JSONDecodeError:
            raise falcon.HTTPError(falcon.HTTP_400, "Bad Request", "Invalid JSON payload")
        except ValueError as e:
            raise falcon.HTTPError(falcon.HTTP_400, "Bad Request", str(e))

    def generate_new_name(self, old_name):
        """Generates a new file name by appending a timestamp."""
        base, ext = os.path.splitext(old_name)
        timestamp = str(int(os.path.getctime(os.path.join(self.dirname, old_name))))
        return "{}_{}{}".format(base, timestamp, ext)

# Set up the Falcon app
api = falcon.API()

# Add a route to the API
renamer = FileRenamer()
api.add_route('/rename', renamer)

if __name__ == "__main__":
    # Run the API locally on port 8000
    import socket
    from wsgiref import simple_server

    httpd = simple_server.make_server('', 8000, api)
    print("Serving on port 8000...")
    httpd.serve_forever()