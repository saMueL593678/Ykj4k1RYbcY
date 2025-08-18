# 代码生成时间: 2025-08-19 06:07:52
# interactive_chart_generator.py
# This script is an example of an interactive chart generator using Falcon framework.

import falcon
from falcon import HTTPError
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from io import BytesIO

class ChartResource:
    """ Handles GET requests to /chart. """
    def on_get(self, req, resp):
        """ Handles GET requests. """
        # Get chart type from query parameters
        chart_type = req.get_param('type', True)
        
        # Validate chart type
        if chart_type not in ['bar', 'line', 'pie']:
            raise falcon.HTTPBadRequest('Invalid chart type', 'Chart type must be one of: bar, line, pie')
        
        # Generate sample data
        x = [1, 2, 3, 4, 5]
        y = [2, 3, 5, 7, 11]
        
        # Generate chart based on type
        if chart_type == 'bar':
            plt.bar(x, y)
        elif chart_type == 'line':
            plt.plot(x, y)
        elif chart_type == 'pie':
            plt.pie(y)
        
        # Save figure to buffer
        buf = BytesIO()
        canvas = FigureCanvasAgg(plt.gcf())
        canvas.print_png(buf)
        buf.seek(0)
        
        # Set response headers
        resp.set_header('Content-Type', 'image/png')
        
        # Write buffer to response
        resp.body = buf.read()

# Create Falcon API app
app = falcon.App()

# Add route for chart resource
app.add_route('/chart', ChartResource())

# Define run function to start the service
def run():
    """Starts the Falcon service."""
    from wsgiref.simple_server import make_server
    try:
        # Start the Falcon API
        print('Starting interactive chart generator service on port 8080...')
        make_server('0.0.0.0', 8080, app).serve_forever()
    except Exception as e:
        print('Error starting interactive chart generator service: ', str(e))

if __name__ == '__main__':
    run()