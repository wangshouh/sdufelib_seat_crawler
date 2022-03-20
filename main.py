import requests
import json
from datetime import datetime

def load_config(now_day):
    with open('config.txt', 'r') as f:
        config = json.loads(f.read())

    complete_url = config['prefix_url'] + now_day
    order_id = config['order_id']
    return complete_url, order_id

def get_timeid_list(complete_url, order_id, s):
        headers = {
            'Referer': complete_url
        }

        book_info_api = "http://libst.sdufe.edu.cn/api.php/v3areas/" + order_id
        bookTimeId_list = []
        for i in s.get(book_info_api, headers=headers).json()['data']['list']['childArea']:
            bookTimeId_list.append(
                {
                    'name': i['name'],
                    'book_time_id': i['area_times']['data']['list'][0]['id'],
                    'id': i['id']
                }
            )

        return bookTimeId_list

def get_referer_url_list(complete_url, order_id, s, now_day, now_time):
    for i in timeid_list:
        i['referer_url'] = "http://libst.sdufe.edu.cn/web/seat3?area={}&segment={}&day={}}&startTime={}&endTime=22:00"


now_day = datetime.now().strftime('%Y-%m-%d')
now_time = datetime.now().strftime('%H:%M')
complete_url, order_id = load_config(now_day)
# s = requests.session()
# timeid_list = get_timeid_list(complete_url, order_id, s)
print(now_time)
