# 代码生成时间: 2025-08-17 11:43:41
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Sorting App using Python and Falcon framework.
This app provides a simple interface to perform sorting on a list of numbers.
"""

import falcon

# Define the Sorting Resource
class SortingResource:
    def on_get(self, req, resp):
        # Get the list of numbers to sort from the query parameters
        raw_numbers = req.get_param('numbers', default='')
        if not raw_numbers:
            raise falcon.HTTPBadRequest(title="Missing numbers", description="Please provide a list of numbers to sort.")

        try:
            # Convert the query parameter into a list of integers
            numbers = [int(num) for num in raw_numbers.split(',')]
        except ValueError:
            raise falcon.HTTPBadRequest(title="Invalid numbers", description="Please provide a valid list of numbers.")

        # Sort the numbers
        sorted_numbers = sorted(numbers)

        # Set the response body to the sorted list of numbers
        resp.media = {'sorted_numbers': sorted_numbers}
        resp.status = falcon.HTTP_OK

# Create an API instance
api = falcon.API()

# Add the Sorting Resource
api.add_route('/sort', SortingResource())

# This function would be called by the server hosting the app
# def create_app():
#     return api

# For demonstration purposes, the following lines will run a development server
# if __name__ == '__main__':
#     import falcon
#     api = create_app()
#     api.run()
