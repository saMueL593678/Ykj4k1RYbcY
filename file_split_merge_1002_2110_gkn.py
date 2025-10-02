# 代码生成时间: 2025-10-02 21:10:57
# file_split_merge.py
# This script provides a File Split and Merge tool using Python and Falcon framework.

import falcon
import os
import logging

# Define a logger
logger = logging.getLogger()

class FileSplitResource:
    """
    A Falcon resource for splitting and merging files.
    """
    def on_get(self, req, resp):
        """
        Handle GET requests for file operations.
        """
        try:
            # Check if the operation is splitting or merging
            operation = req.get_param('operation', required=True)
            file_path = req.get_param('file_path', required=True)
            chunk_size = req.get_param('chunk_size', default='1024')

            if operation == 'split':
                self.split_file(file_path, chunk_size)
            elif operation == 'merge':
                self.merge_files(file_path)
            else:
                raise ValueError('Invalid operation specified.')

            resp.status = falcon.HTTP_200
            resp.media = {'message': 'File operation completed successfully.'}
        except Exception as e:
            logger.error(f'Error occurred: {e}')
            resp.status = falcon.HTTP_500
            resp.media = {'error': str(e)}

    def split_file(self, file_path, chunk_size):
        """
        Split a file into chunks.
        """
        try:
            with open(file_path, 'rb') as file:
                index = 0
                while True:
                    data = file.read(int(chunk_size))
                    if not data:
                        break
                    chunk_file_name = f'{os.path.splitext(file_path)[0]}_part_{index}'
                    with open(chunk_file_name, 'wb') as chunk_file:
                        chunk_file.write(data)
                    index += 1
        except FileNotFoundError:
            raise FileNotFoundError(f'The file {file_path} does not exist.')
        except Exception as e:
            raise Exception(f'An error occurred while splitting the file: {e}')

    def merge_files(self, file_path):
        """
        Merge chunks into a single file.
        """
        try:
            base_name = os.path.splitext(file_path)[0]
            chunk_files = sorted([f for f in os.listdir() if f.startswith(base_name) and f.endswith('.part')])
            if not chunk_files:
                raise FileNotFoundError(f'No chunks found for merging into {file_path}.')

            with open(file_path, 'wb') as file:
                for chunk_file in chunk_files:
                    with open(chunk_file, 'rb') as chunk:
                        file.write(chunk.read())
                    os.remove(chunk_file)
        except FileNotFoundError:
            raise FileNotFoundError(f'The file {file_path} or chunks do not exist for merging.')
        except Exception as e:
            raise Exception(f'An error occurred while merging the files: {e}')

# Instantiate the API
app = falcon.App()

# Add the resource to the API
app.add_route('/files', FileSplitResource())

# Run the application (only for demonstration purposes, in real use you'd use a WSGI server)
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    make_server('', 8000, app).serve_forever()