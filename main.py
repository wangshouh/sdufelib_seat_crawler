import requests
import json
from datetime import datetime

with open('config.txt', 'r') as f:
    prefix_url = f.read()

complete_url = prefix_url + datetime.now().strftime('%Y-%m-%d')
print(complete_url)
