# 代码生成时间: 2025-08-20 06:25:54
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Inventory Management System using Falcon framework.
"""

import falcon
from falcon import HTTPError
from falcon.asgi import ASGIApp
import json

# Define the inventory data structure.
# This could be replaced with a database in a real-world application.
inventory = {
    "items": [
        {"id": 1, "name": "Apple", "quantity": 100},
        {"id": 2, "name": "Banana", "quantity": 150},
        {"id": 3, "name": "Carrot", "quantity": 200},
    ]
}

class InventoryResource:
    """Handles inventory-related requests."""

    def on_get(self, req, resp):
        """Return the current inventory as JSON."""
        resp.media = inventory
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        """Add a new item to the inventory."""
        try:
            new_item = req.media
            if not new_item or 'name' not in new_item or 'quantity' not in new_item:
                raise falcon.HTTPError(falcon.HTTP_400, 'Missing item details')
            new_item['id'] = len(inventory['items']) + 1
            inventory['items'].append(new_item)
            resp.status = falcon.HTTP_201
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_500, str(ex))

    def on_put(self, req, resp, item_id):
        """Update an existing item in the inventory."""
        try:
            item = next((item for item in inventory['items'] if item['id'] == item_id), None)
            if not item:
                raise falcon.HTTPError(falcon.HTTP_404, 'Item not found')
            updates = req.media
            item.update(updates)
            resp.status = falcon.HTTP_200
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_500, str(ex))

    def on_delete(self, req, resp, item_id):
        """Remove an item from the inventory."""
        try:
            global inventory
            inventory['items'] = [item for item in inventory['items'] if item['id'] != item_id]
            resp.status = falcon.HTTP_200
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_500, str(ex))

# Create an instance of the ASGI application
app = ASGIApp()

# Add routes to the application
app.add_route('/inventory', InventoryResource())
app.add_route('/inventory/{item_id}', InventoryResource())

if __name__ == '__main__':
    import asyncio
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)