# 代码生成时间: 2025-08-18 22:29:00
# web_content_scraper.py

"""
A simple web content scraper built using the Falcon framework and requests library.
This script demonstrates how to create a Falcon service that fetches
web content from a specified URL and returns it as plain text.
"""

# Import necessary modules
import falcon
import requests
from falcon import API
from requests.exceptions import RequestException

# Define a Falcon resource for scraping web content
class WebContentScraper:
    """
    Falcon resource for scraping web content from a given URL.
    It fetches the content and returns it as plain text.
    """
    def on_get(self, req, resp):
        """
        Handle GET requests to scrape web content.

        Args:
            req (falcon.Request): The incoming request.
            resp (falcon.Response): The outgoing response.
        """
        # Extract the URL from the request query parameters
        url = req.get_param("url")
        if not url:
            raise falcon.HTTPBadRequest("Missing 'url' parameter")

        try:
            # Fetch the content from the URL
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            # Return the text content of the response
            resp.media = response.text
            resp.status = falcon.HTTP_200
        except RequestException as e:
            # Handle any request exceptions and return an error response
            raise falcon.HTTPInternalServerError(
                f"Failed to scrape content: {str(e)}"
            )

# Create the Falcon API and add the WebContentScraper resource
api = API()
api.add_route("/scraper", WebContentScraper())

# Define the main function to run the Falcon API
def main():
    """
    Main function to run the Falcon API.
    This function should be called when the script is executed directly.
    """
    # Run the Falcon API on the default port 8000
    api.run(port=8000, host="0.0.0.0")

# Check if this script is being run directly and execute the main function
if __name__ == "__main__":
    main()