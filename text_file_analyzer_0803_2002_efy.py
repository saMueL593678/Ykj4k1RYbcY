# 代码生成时间: 2025-08-03 20:02:25
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Text File Analyzer using Falcon Framework

This program analyzes the content of a text file and provides
various statistics and insights about the content.
"""

import falcon
import os
from collections import Counter
from string import punctuation

# Define the Falcon API resource for text file analysis
class TextFileAnalyzer:
    def on_get(self, req, resp):
        # Check if the necessary query parameter 'filename' is provided
        filename = req.get_param('filename')
        if not filename:
            resp.body = 'Missing required parameter: filename'
            resp.status = falcon.HTTP_BAD_REQUEST
            return

        # Validate the file path and check if the file exists
        file_path = os.path.join(os.getcwd(), filename)
        if not os.path.isfile(file_path):
            resp.body = 'File not found'
            resp.status = falcon.HTTP_NOT_FOUND
            return

        try:
            # Read the content of the text file
            with open(file_path, 'r') as file:
                content = file.read()

            # Perform text analysis
            lines = content.splitlines()
            words = content.split()

            # Count the number of lines
            num_lines = len(lines)

            # Count the number of words
            num_words = len(words)

            # Count the number of characters (excluding punctuation)
            num_characters = sum(len(word) for word in words if word.isalpha())

            # Count the frequency of each word
            word_count = Counter(words)

            # Prepare the response data
            response_data = {
                'num_lines': num_lines,
                'num_words': num_words,
                'num_characters': num_characters,
                'word_frequency': dict(word_count)
            }

            # Set the response body and status code
            resp.body = response_data
            resp.status = falcon.HTTP_OK

        except Exception as e:
            # Handle any exceptions and return an error response
            resp.body = f'Error analyzing file: {str(e)}'
            resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR

# Configure the Falcon API app
app = falcon.API()

# Register the TextFileAnalyzer resource
app.add_route('/api/analyze', TextFileAnalyzer())
