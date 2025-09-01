# 代码生成时间: 2025-09-02 05:12:51
# order_processing_service.py
# This service handles order processing using Falcon framework.

from falcon import Falcon, API
from falcon_cors import CORS
import json

# Define the Order class to encapsulate order data
class Order:
    def __init__(self, order_id, customer_id, product_id, quantity):
        self.order_id = order_id
        self.customer_id = customer_id
        self.product_id = product_id
        self.quantity = quantity

    def to_json(self):
        """Converts order data to JSON format."""
        return json.dumps({
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "quantity": self.quantity
        })

# Define the OrderService class to handle order processing logic
class OrderService:
    def __init__(self):
        self.orders = {}

    def create_order(self, order_id, customer_id, product_id, quantity):
        """Creates a new order and adds it to the database."""
        if order_id in self.orders:
            raise Exception("Order already exists.")
        self.orders[order_id] = Order(order_id, customer_id, product_id, quantity)
        return self.orders[order_id].to_json()

    def get_order(self, order_id):
        """Retrieves an order by its ID."""
        if order_id not in self.orders:
            raise Exception("Order not found.")
        return self.orders[order_id].to_json()

# Define a Falcon resource to handle HTTP requests
class OrderResource:
    def __init__(self, order_service):
        self.order_service = order_service

    def on_post(self, req, resp):
        "