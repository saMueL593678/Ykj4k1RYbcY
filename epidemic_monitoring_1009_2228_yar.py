# 代码生成时间: 2025-10-09 22:28:59
# epidemic_monitoring.py
# This script uses the Falcon framework to create an API for monitoring infectious diseases.

import falcon
from falcon import API, HTTP_200, HTTP_500
import json

# Define a simple in-memory database for disease data
disease_database = {
    "diseases": {
        "FLU": {"cases": 150, "severe": 20},
        "DENGUE": {"cases": 75, "severe": 5}
    }
}


class DiseaseResource:
    """Handles GET requests to retrieve disease data."""
    def on_get(self, req, resp):
        """Handles GET requests for disease data."""
        try:
            # Retrieve disease data from the database
            disease_data = disease_database["diseases"]
            resp.status = HTTP_200
            resp.body = json.dumps(disease_data)
        except Exception as e:
            # Handle any unexpected errors
            resp.status = HTTP_500
            resp.body = json.dumps({"error": str(e)})

    def on_post(self, req, resp):
        """Handles POST requests to add or update disease data."""
        try:
            # Parse the JSON body of the request
            data = json.loads(req.bounded_stream.read().decode())
            # Update the disease data in the database
            for disease, stats in data.items():
                disease_database["diseases"][disease] = stats
            resp.status = HTTP_200
            resp.body = json.dumps({"message": "Disease data updated"})
        except KeyError as e:
            resp.status = HTTP_400
            resp.body = json.dumps({"error": f"Missing key: {e}"})
        except Exception as e:
            resp.status = HTTP_500
            resp.body = json.dumps({"error": str(e)})


# Create an API instance
app = API()

# Add a route for the DiseaseResource
app.add_route('/diseases', DiseaseResource())

# You can run the application using the command:
# python -m falcon app

