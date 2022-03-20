import requests
import json
from datetime import datetime

def load_config():
    with open('config.txt', 'r') as f:
        config = json.loads(f.read())

    complete_url = config['prefix_url'] + datetime.now().strftime('%Y-%m-%d')
    order_id = config['order_id']
    return complete_url, order_id

def get_timeid_list(complete_url, order_id, s):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'Referer': complete_url
        }

        book_info_api = "http://libst.sdufe.edu.cn/api.php/v3areas/" + order_id
        bookTimeId_list = []
        for i in s.get(book_info_api, headers=headers).json()['data']['list']['childArea']:
            bookTimeId_list.append(
                {
                    'name': i['name'],
                    'id': i['area_times']['data']['list'][0]['id']
                }
            )

        return bookTimeId_list

complete_url, order_id = load_config()
s = requests.session()
timeid_list = get_timeid_list(complete_url, order_id, s)
print(timeid_list)
