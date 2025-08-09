# 代码生成时间: 2025-08-10 06:52:29
# unzip_tool.py
# A Falcon-based API providing a file decompression service

import falcon
import zipfile
import os
from datetime import datetime
from werkzeug.utils import secure_filename

# Falcon API resource for file decompression
class UnzipResource:
    def on_post(self, req, resp):
        # Only allow JSON content type
        if req.content_type != "application/json":
            raise falcon.HTTPUnsupportedMediaType("Unsupported media type")

        try:
            # Parse the JSON request to get the file path
            file_info = req.media.get("file")
            if not file_info or not file_info.filename:
                raise falcon.HTTPBadRequest("No file provided")

            # Secure the filename
            secure_file_name = secure_filename(file_info.filename)
            download_folder = "./downloads/"
            zip_file_path = os.path.join(download_folder, secure_file_name)

            # Save the uploaded file
            with open(zip_file_path, "wb") as file:
                file.write(file_info.file.read())

            # Unzip the file
            unzip_folder = download_folder + "unzipped/" + datetime.now().strftime("%Y%m%d%H%M%S") + "/"
            os.makedirs(unzip_folder, exist_ok=True)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(unzip_folder)

            # Send a success response with the path to the unzipped files
            response_body = {"message": "File unzipped successfully", "destination": unzip_folder}
            resp.media = response_body
            resp.status = falcon.HTTP_200  # OK
        except zipfile.BadZipFile:
            resp.media = {"error": "Bad ZIP file. Cannot unzip."}
            resp.status = falcon.HTTP_400  # Bad Request
        except Exception as e:
            resp.media = {"error": str(e)}
            resp.status = falcon.HTTP_500  # Internal Server Error

# Setup Falcon API
api = falcon.API()
api.add_route('/unzip', UnzipResource())

# Uncomment the following lines to run the API directly from this script
# if __name__ == '__main__':
#     import sys
#     from wsgiref.simple_server import make_server
#     httpd = make_server('localhost', 8000, api)
#     print('Serving on localhost port 8000...')
#     httpd.serve_forever()