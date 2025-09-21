# 代码生成时间: 2025-09-21 09:48:25
#!/usr/bin/env python

"""
Security Audit Log Service using Falcon Framework
This service provides an endpoint to record and retrieve security audit logs.
"""

import falcon
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(filename='security_audit.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Create a logger
logger = logging.getLogger('SecurityAuditLogger')

# In-memory database to store audit logs
audit_logs = []

# Helper function to log messages
def log_message(message):
    logger.info(message)

# Falcon API resource for security audit logs
class AuditLogResource:
    """Handles HTTP requests for security audit logs."""
    def on_get(self, req, resp):
        """
        Retrieves the list of security audit logs.
        Returns a JSON-formatted list of logs.
        """
        try:
            resp.media = {'logs': audit_logs}
            resp.status = falcon.HTTP_OK
        except Exception as e:
            resp.media = {'error': str(e)}
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR
            log_message(str(e))

    def on_post(self, req, resp):
        """
        Creates a new security audit log entry.
        Requires a JSON payload with 'message' and 'level' keys.
        """
        try:
            data = json.loads(req.bounded_stream.read())
            message = data.get('message')
            level = data.get('level', 'INFO').upper()
            if not message:
                raise ValueError("Missing 'message' in the request body")
            
            # Create a new log entry
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'message': message,
                'level': level
            }
            
            # Append to the in-memory database
            audit_logs.append(log_entry)
            
            # Log the message to the file
            log_message(f"{level}: {message}")
            
            resp.media = {'status': 'success', 'log': log_entry}
            resp.status = falcon.HTTP_CREATED
        except ValueError as ve:
            resp.media = {'error': str(ve)}
            resp.status = falcon.HTTP_BAD_REQUEST
        except Exception as e:
            resp.media = {'error': str(e)}
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR
            log_message(str(e))

# Create a Falcon API application
app = falcon.API()

# Add the AuditLogResource to the API
app.add_route('/audit-log', AuditLogResource())
