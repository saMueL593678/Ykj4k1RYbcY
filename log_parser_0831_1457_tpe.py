# 代码生成时间: 2025-08-31 14:57:22
# log_parser.py
# A Falcon-based web service for parsing log files.

import falcon
from falcon import API, Request, Response
import json
import re
import logging
from typing import Any, Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a regular expression pattern to match log entries
LOG_PATTERN = re.compile(r'^(\S+) (\S+) (\S+) \[(.*?)\] "(\S+) (\S+) (\S+)" (\d+) (\d+)$')

class LogParser:
    def on_get(self, req: Request, resp: Response) -> None:
        # Respond to a GET request with a form to upload a log file
        resp.media = {
            'form': 'Upload a log file'
        }
        resp.status = falcon.HTTP_200

    def on_post(self, req: Request, resp: Response) -> None:
        # Respond to a POST request with the parsed log data
        try:
            file_data = req.get_param('file')
            if file_data is None:
                raise falcon.HTTPBadRequest('No file uploaded', 'Please upload a log file.')

            # Parse the log file and extract data
            parsed_logs = self.parse_log(file_data)

            # Return the parsed data
            resp.media = parsed_logs
            resp.status = falcon.HTTP_200
        except Exception as e:
            # Log the error and return a 500 Internal Server Error
            logger.error(f'Error parsing log: {e}')
            raise falcon.HTTPInternalServerError('Error parsing log', str(e))

    def parse_log(self, log_data: str) -> List[Dict[str, Any]]:
        """
        Parse the log data and return a list of dictionaries representing each log entry.
        Each dictionary contains the parsed log fields.
        """
        parsed_logs = []
        for line in log_data.splitlines():
            match = LOG_PATTERN.match(line)
            if match:
                log_entry = {
                    'ip_address': match.group(1),
                    'user_id': match.group(2),
                    'username': match.group(3),
                    'datetime': match.group(4),
                    'request_method': match.group(5),
                    'request_url': match.group(6),
                    'http_version': match.group(7),
                    'response_code': int(match.group(8)),
                    'response_size': int(match.group(9))
                }
                parsed_logs.append(log_entry)
            else:
                logger.warning(f'Unmatched line: {line}')
        return parsed_logs

# Create the Falcon API object
api = API()

# Add the LogParser resource to the API
api.add_route('/logs', LogParser())

if __name__ == '__main__':
    # Run the API
    from wsgiref.simple_server import make_server
    httpd = make_server('0.0.0.0', 8000, api)
    logger.info('Starting Falcon API on http://localhost:8000/')
    httpd.serve_forever()