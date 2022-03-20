import requests
import json
import time

area_api_url = 'http://libst.sdufe.edu.cn/api.php/v3areas/27'

headers = {"Referer" : "http://libst.sdufe.edu.cn/home/web/seat/area/27"}

area_info = requests.get(area_api_url, headers=headers).json()

print(area_info)