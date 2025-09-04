# 代码生成时间: 2025-09-04 18:54:40
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A Falcon framework-based data backup and restore service.
"""

import falcon
import json
import os
import shutil
from datetime import datetime

class DataBackupResource:
    """ Handles backup and restore operations. """
    def __init__(self, backup_directory):
        self.backup_directory = backup_directory
        # Ensure the backup directory exists
        os.makedirs(self.backup_directory, exist_ok=True)

    def on_get(self, req, resp):
        """ Returns a list of available backups. """
        try:
            backup_files = [f for f in os.listdir(self.backup_directory) if os.path.isfile(os.path.join(self.backup_directory, f))]
            resp.body = json.dumps(backup_files)
            resp.status = falcon.HTTP_200
        except Exception as e:
            resp.body = json.dumps({"error": str(e)})
            resp.status = falcon.HTTP_500

    def on_post(self, req, resp):
        """ Creates a new backup. """
        try:
            backup_name = datetime.now().strftime('%Y%m%d%H%M%S')
            backup_path = os.path.join(self.backup_directory, f'{backup_name}.zip')
            # Assuming the data to backup is in the current directory
            shutil.make_archive(backup_path, 'zip', '.')
            resp.body = json.dumps({"message": f'Backup created: {backup_path}'})
            resp.status = falcon.HTTP_201
        except Exception as e:
            resp.body = json.dumps({"error": str(e)})
            resp.status = falcon.HTTP_500

    def on_put(self, req, resp):
        """ Restores data from a backup. """
        try:
            # Extract the backup file name from the request
            backup_file = req.media.get('backup_file')
            backup_path = os.path.join(self.backup_directory, backup_file)
            if not os.path.exists(backup_path):
                raise FileNotFoundError(f'Backup file {backup_file} not found.')
            # Assuming the data will be restored to the current directory
            shutil.unpack_archive(backup_path, '.')
            resp.body = json.dumps({"message": f'Data restored from {backup_file}.'})
            resp.status = falcon.HTTP_200
        except Exception as e:
            resp.body = json.dumps({"error": str(e)})
            resp.status = falcon.HTTP_500


def main():
    # Instantiate the data backup resource with a backup directory
    backup_directory = './backups'
    data_backup_resource = DataBackupResource(backup_directory)

    # Create a Falcon app
    app = falcon.App()
    # Add routes for the backup resource
    app.add_route('/backup', data_backup_resource, suffix="")
    app.add_route('/restore', data_backup_resource, suffix="")

    # Run the app
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8000)

if __name__ == '__main__':
    main()
