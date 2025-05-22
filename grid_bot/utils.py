import json
import os

def load_orders(filename='orders.json'):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def save_orders(orders, filename='orders.json'):
    with open(filename, 'w') as f:
        json.dump(orders, f, indent=2)

