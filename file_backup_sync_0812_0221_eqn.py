# 代码生成时间: 2025-08-12 02:21:11
#!/usr/bin/env python

"""
A File Backup and Sync Tool using FALCON framework.
This tool is designed to backup and sync files between two locations.
"""

import os
import shutil
from falcon import API, Request, Response, HTTP_200, HTTP_400, HTTP_500
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("file_backup_sync")

class FileBackupSync:
    """
    A class to handle file backup and synchronization.
    """
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def backup(self):
        """
        Backs up files from the source directory to the destination directory.
        """
        try:
            # Check if source and destination directories exist
            if not os.path.exists(self.source):
                raise FileNotFoundError("Source directory does not exist")
            if not os.path.exists(self.destination):
                os.makedirs(self.destination)

            # Copy files from source to destination
            for item in os.listdir(self.source):
                s = os.path.join(self.source, item)
                d = os.path.join(self.destination, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)

            logger.info("Backup completed successfully")
            return {
                "message": "Backup completed successfully",
                "status": HTTP_200
            }
        except Exception as e:
            logger.error(f"Backup failed: {str(e)}")
            return {
                "message": f"Backup failed: {str(e)}",
                "status": HTTP_500
            }

    def sync(self):
        """
        Syncs files between the source and destination directories.
        """
        try:
            # Check if source and destination directories exist
            if not os.path.exists(self.source):
                raise FileNotFoundError("Source directory does not exist")
            if not os.path.exists(self.destination):
                os.makedirs(self.destination)

            # Sync files between source and destination
            for item in os.listdir(self.source):
                s = os.path.join(self.source, item)
                d = os.path.join(self.destination, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)

            # Check for any new files in the destination that are not in the source
            for item in os.listdir(self.destination):
                s = os.path.join(self.source, item)
                d = os.path.join(self.destination, item)
                if not os.path.exists(s):
                    os.remove(d)

            logger.info("Sync completed successfully")
            return {
                "message": "Sync completed successfully",
                "status": HTTP_200
            }
        except Exception as e:
            logger.error(f"Sync failed: {str(e)}")
            return {
                "message": f"Sync failed: {str(e)}",
                "status": HTTP_500
            }

class BackupSyncResource:
    """
    A Falcon resource for backup and sync operations.
    """
    def on_post(self, req, resp, operation="backup"):
        """
        Handles POST requests for backup and sync operations.
        """
        try:
            data = json.load(req.stream)
            source = data["source"]
            destination = data["destination"]

            if operation == "backup":
                file_backup_sync = FileBackupSync(source, destination)
                result = file_backup_sync.backup()
            elif operation == "sync":
                file_backup_sync = FileBackupSync(source, destination)
                result = file_backup_sync.sync()
            else:
                raise ValueError("Invalid operation")

            resp.status = result["status"]
            resp.media = result
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            raise falcon.HTTPError(f"{operation} failed: {str(e)}", status=HTTP_400)

api = API()
api.add_route("/backup", BackupSyncResource())
api.add_route("/sync", BackupSyncResource())