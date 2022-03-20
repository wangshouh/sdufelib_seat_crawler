import requests
import json
from datetime import datetime

def load_config():
    with open('config.txt', 'r') as f:
        config = json.loads(f.read())

    complete_url = config['prefix_url'] + datetime.now().strftime('%Y-%m-%d')
    order_id = config['order_id']
    return complete_url, order_id

complete_url, order_id = load_config()
print(complete_url)
