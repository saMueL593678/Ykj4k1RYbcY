# 代码生成时间: 2025-09-13 23:29:46
# hash_calculator_service.py
# A Falcon service providing hash calculation functionality.

import falcon
import hashlib
import logging
from falcon import HTTPBadRequest, HTTPInternalServerError

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the HashCalculator class
class HashCalculator:
    def on_get(self, req, resp):
        """
        Handle GET requests to calculate hash values.
        Uses query parameters 'algorithm' and 'input' to calculate the hash.
        """
        try:
            algorithm = req.get_param('algorithm', required=True)
            input_data = req.get_param('input', required=True)
        except falcon.HTTPMissingHeader:
            raise HTTPBadRequest("Missing 'algorithm' or 'input' parameter.", "Both 'algorithm' and 'input' parameters are required.")
        
        try:
            hash_value = self.calculate_hash(algorithm, input_data)
            resp.media = {'hash': hash_value}
            resp.status = falcon.HTTP_OK
        except ValueError:
            raise HTTPBadRequest("Invalid 'algorithm' parameter.", "Only MD5, SHA1, and SHA256 are supported.")
        except Exception as e:
            logger.error("Error calculating hash: %s", str(e))
            raise HTTPInternalServerError("Internal server error while calculating hash.", "An error occurred while calculating the hash.")

    def calculate_hash(self, algorithm, input_data):
        """
        Calculate hash for given algorithm and input data.
        Supported algorithms: MD5, SHA1, SHA256
        """
        if algorithm.upper() == 'MD5':
            return hashlib.md5(input_data.encode()).hexdigest()
        elif algorithm.upper() == 'SHA1':
            return hashlib.sha1(input_data.encode()).hexdigest()
        elif algorithm.upper() == 'SHA256':
            return hashlib.sha256(input_data.encode()).hexdigest()
        else:
            raise ValueError("Unsupported algorithm.")

# Instantiate the API
api = falcon.API()

# Add route
api.add_route("/hash", HashCalculator())
