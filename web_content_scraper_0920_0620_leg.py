# 代码生成时间: 2025-09-20 06:20:51
# web_content_scraper.py
# A simple web content scraper using Falcon framework and Requests library.

import falcon
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Define a class for the web content scraper resource.
class WebContentScraper:
    def on_get(self, req, resp):
        # Extract the URL to scrape from the request query parameter.
        url_to_scrape = req.get_param('url')

        # Check if the URL is provided.
        if not url_to_scrape:
            raise falcon.HTTPBadRequest('Missing URL parameter', 'Please provide a URL to scrape.')

        try:
            # Send a GET request to the specified URL.
            response = requests.get(url_to_scrape)
            response.raise_for_status()  # Raise an exception for HTTP errors.

            # Parse the HTML content using BeautifulSoup.
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract and return the HTML content.
            resp.status = falcon.HTTP_200
            resp.media = {'content': str(soup)}
        except requests.exceptions.RequestException as e:
            # Handle any exceptions that occur during the request.
            raise falcon.HTTPInternalServerError('Error scraping content', str(e))

# Instantiate the Falcon API.
api = falcon.API()

# Add the WebContentScraper resource to the API.
api.add_route('/scrape', WebContentScraper())

# The main function to run the Falcon API.
if __name__ == '__main__':
    # Run the API on localhost port 8000.
    api.run(port=8000, host='localhost')
