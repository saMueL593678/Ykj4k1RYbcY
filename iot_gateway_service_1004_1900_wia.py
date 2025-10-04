# 代码生成时间: 2025-10-04 19:00:50
# iot_gateway_service.py

# Import necessary libraries
import falcon
def create_app():
    # Define the API resource for managing IoT gateways
    class IotGatewayResource:
        def on_get(self, req, resp):
            """
            Handles GET requests, listing all IoT gateways.
            Returns a JSON array of gateways.
            """
            try:
                # Fetch IoT gateways from a database or other storage.
                # Here we use a mock list for demonstration purposes.
                gateways = [
                    {'id': 1, 'name': 'Gateway 1', 'status': 'online'},
                    {'id': 2, 'name': 'Gateway 2', 'status': 'offline'}
                ]
                resp.media = gateways
                resp.status = falcon.HTTP_200
            except Exception as e:
                # Handle any exceptions that may occur
                resp.media = {'error': str(e)}
                resp.status = falcon.HTTP_500

        def on_post(self, req, resp):
            """
            Handles POST requests, adding a new IoT gateway.
            Returns the newly created gateway info.
            """
            try:
                # Extract JSON data from the request
                gateway_data = req.media
                # Validate and create a new gateway
                # Here we mock the creation process
                new_gateway = {'id': len(gateway_data) + 1, 'name': gateway_data['name'], 'status': 'online'}
                resp.media = new_gateway
                resp.status = falcon.HTTP_201
            except KeyError as ke:
                # Handle missing fields in the request
                resp.media = {'error': f'Missing field: {ke}'}
                resp.status = falcon.HTTP_400
            except Exception as e:
                # Handle any other exceptions
                resp.media = {'error': str(e)}
                resp.status = falcon.HTTP_500

    # Setup the Falcon API
    app = falcon.API()
    # Add the IotGatewayResource to handle /gateways endpoint
    app.add_route('/gateways', IotGatewayResource())
    return app

# If this module is run as the main program, create and start the API
if __name__ == '__main__':
    app = create_app()
    # You can use gunicorn or any WSGI server to run the app
    # For example: gunicorn -b :8000 iot_gateway_service:app
    print("Starting IoT Gateway API...")
    # Start the API in a development server
    # Warning: This is not suitable for production
    from wsgiref.simple_server import make_server
    httpd = make_server('0.0.0.0', 8000, app)
    httpd.serve_forever()