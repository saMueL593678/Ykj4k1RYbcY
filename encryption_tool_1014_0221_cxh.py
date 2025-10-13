# 代码生成时间: 2025-10-14 02:21:28
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Falcon Framework Encryption Tool
A simple tool to encrypt and decrypt files using the Falcon framework.
"""

import falcon
import os
from cryptography.fernet import Fernet

# Define the API document and error messages
API_DOCS = {
    "description": "A simple tool to encrypt and decrypt files",
    "operations": {
        "post": {
            "summary": "Encrypt or Decrypt a file",
            "notes": "Provide file content and encryption key in the request body.",
        }
    },
}

# Error messages
ERROR_INVALID_INPUT = "Invalid input: Please provide both file content and encryption key."
ERROR_ENCRYPTION_FAILED = "Encryption failed."
ERROR_DECRYPTION_FAILED = "Decryption failed."

class EncryptionTool:
    """
    A class that handles file encryption and decryption.
    """
    def __init__(self, key):
        self.key = key
        self.cipher = Fernet(key)

    def encrypt(self, file_content):
        """
        Encrypt the provided file content.
        :param file_content: The content of the file to encrypt.
        :return: The encrypted content as bytes.
        """
        try:
            return self.cipher.encrypt(file_content.encode())
        except Exception as e:
            raise falcon.HTTPInternalServerError(title=ERROR_ENCRYPTION_FAILED, description=str(e))

    def decrypt(self, encrypted_content):
        """
        Decrypt the provided encrypted content.
        :param encrypted_content: The content of the encrypted file.
        :return: The decrypted content as a string.
        """
        try:
            return self.cipher.decrypt(encrypted_content).decode()
        except Exception as e:
            raise falcon.HTTPInternalServerError(title=ERROR_DECRYPTION_FAILED, description=str(e))

# Falcon API setup
api = application = falcon.API()

# Define the resource for handling encryption and decryption requests
class FileEncryptionResource:
    def on_post(self, req, resp):
        """
        Handle POST requests to encrypt or decrypt files.
        :param req: The Falcon request object.
        :param resp: The Falcon response object.
        """
        # Get the JSON body from the request
        try:
            body = req.media
        except falcon.HTTPBadRequest:
            raise falcon.HTTPBadRequest(title="Invalid JSON", description="The JSON body is missing or malformed.")

        # Validate the input data
        if 'file_content' not in body or 'encryption_key' not in body:
            raise falcon.HTTPBadRequest(title=ERROR_INVALID_INPUT, description="Both file content and encryption key are required.")

        # Create an instance of EncryptionTool with the provided key
        encryption_tool = EncryptionTool(body['encryption_key'].encode())

        # Encrypt or decrypt the file content based on the 'action' parameter
        if body.get('action') == 'encrypt':
            encrypted_content = encryption_tool.encrypt(body['file_content'])
            resp.media = {
                'status': 'success',
                'encrypted_content': encrypted_content.decode()
            }
        elif body.get('action') == 'decrypt':
            decrypted_content = encryption_tool.decrypt(body['file_content'].encode())
            resp.media = {
                'status': 'success',
                'decrypted_content': decrypted_content
            }
        else:
            raise falcon.HTTPBadRequest(title="Invalid action", description="Action must be 'encrypt' or 'decrypt'.")

# Add the resource to the API
api.add_route('/', FileEncryptionResource())
