# 代码生成时间: 2025-09-03 20:33:33
import falcon
import psutil
from falcon import HTTP_200, HTTP_500

# SystemPerformanceMonitor is a Falcon app that handles
# HTTP requests to monitor system performance.
class SystemPerformanceMonitor:
    def on_get(self, req, resp):
        """Handles the GET request to return system performance data."""
        try:
            # Collect system performance metrics
            system_info = self.get_system_info()

            # Set the HTTP status and response body
            resp.status = HTTP_200
            resp.media = system_info
        except Exception as e:
            # Handle any unexpected exceptions
            resp.status = HTTP_500
            resp.media = {"error": str(e)}

    def get_system_info(self):
        """Returns system performance metrics such as CPU usage, memory usage, etc."""
        # CPU usage percentage
        cpu_usage = psutil.cpu_percent(interval=1)

        # Memory usage
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        memory_available = memory.available

        # Disk usage
        disk_usage = psutil.disk_usage('/')
        total_space = disk_usage.total
        used_space = disk_usage.used
        free_space = disk_usage.free

        # Network I/O stats
        network_io = psutil.net_io_counters()
        bytes_sent = network_io.bytes_sent
        bytes_recv = network_io.bytes_recv

        # Create a dictionary with system performance metrics
        system_info = {
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "memory_available": memory_available,
            "total_space": total_space,
            "used_space": used_space,
            "free_space": free_space,
            "bytes_sent": bytes_sent,
            "bytes_recv": bytes_recv
        }
        return system_info

# Instantiate the Falcon app
app = falcon.App()

# Add a route that responds to the path /system-performance
monitor = SystemPerformanceMonitor()
app.add_route("/system-performance", monitor)