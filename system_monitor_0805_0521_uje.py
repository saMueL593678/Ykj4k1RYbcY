# 代码生成时间: 2025-08-05 05:21:22
# system_monitor.py
# System Performance Monitoring Tool using FALCON and Python

import falcon
import psutil
import json
from falcon import HTTP_200, HTTP_400, HTTP_500

# Define a class for the system monitor resource
class SystemMonitor:
    def on_get(self, req, resp):
        """
        GET method handler to provide system monitor data
        """
        try:
            # Collect system performance data
            system_data = {
                'cpu': {
                    'percent': psutil.cpu_percent(),
                },
                'memory': {
                    'total': psutil.virtual_memory().total,
                    'available': psutil.virtual_memory().available,
                    'percent': psutil.virtual_memory().percent,
                },
                'disk': {
                    'total': psutil.disk_usage('/').total,
                    'used': psutil.disk_usage('/').used,
                    'percent': psutil.disk_usage('/').percent,
                },
            }
            # Serialize the data to JSON and set the response body
            resp.body = json.dumps(system_data)
            resp.status = HTTP_200
        except Exception as e:
            # Handle any exceptions and return a 500 error
            resp.status = HTTP_500
            resp.body = json.dumps({'error': str(e)})

# Initialize the Falcon API
app = falcon.App()

# Add the SystemMonitor resource to the API
app.add_route('/', SystemMonitor())

# Run the API when the script is executed directly
if __name__ == '__main__':
    import sys
    from falcon import testing
    
    class TestSystemMonitor:
        def test_get(self):
            """
            Test the GET method of the SystemMonitor resource
            """
            sim_req, _ = testing.simulate_request('/')
            sim_resp = testing.simulate_response()
            app()(sim_req, sim_resp)
            assert sim_resp.status == HTTP_200
            assert 'cpu' in sim_resp.body
            assert 'memory' in sim_resp.body
            assert 'disk' in sim_resp.body
    
    testing.run_http_tests(TestSystemMonitor(), sys.argv)