import requests
import json
from datetime import datetime
from login import login_token

def load_config(now_day):
    '''
    读取配置文件
    '''
    with open('config.json', 'r') as f:
        config = json.loads(f.read())


    for i in config:
        i['complete_url'] = i['prefix_url'] + now_day
    return config

def get_timeid_list(complete_url, order_id, s):
    '''
    获取时间id列表
    '''
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

def get_url_list(timeid_list, now_day, now_time):
    '''
    获取url列表
    '''
    for i in timeid_list:
        i['referer_url'] = "http://libst.sdufe.edu.cn/web/seat3?area={}&segment={}&day={}&startTime={}&endTime=22:00".format(i['id'], i['book_time_id'], now_day, now_time)
        i['api_url'] = "http://libst.sdufe.edu.cn/api.php/spaces_old?area={}&segment={}&day={}&startTime={}&endTime=22:00".format(i['id'], i['book_time_id'], now_day, now_time)
    return timeid_list

def get_available_seat(url_list, s):
    '''
    获取座位信息
    '''
    available_seat_list = []
    for i in url_list:
        headers = {
            'Referer': i['referer_url']
        }
        seat_list = s.get(i['api_url'], headers=headers).json()['data']['list']
        i['available_seat'] = []
        for seat_info in seat_list:
            if seat_info['status'] == 1:
                i['available_seat'].append(seat_info['no'])
        for j in i['available_seat']:
            available_seat_list.append(
                '{}-{}'.format(i['name'], j)
            )
    return available_seat_list

now_day = datetime.now().strftime('%Y-%m-%d')
now_time = datetime.now().strftime('%H:%M')
config = load_config(now_day)
available_seat_all = []

s = requests.session()
for i in config:
    complete_url = i['complete_url']
    order_id = i['order_id']
    timeid_list = get_timeid_list(complete_url, order_id, s)
    url_list = get_url_list(timeid_list, now_day, now_time)
    available_seat_list = get_available_seat(url_list, s)
    available_seat_all.append(available_seat_list)
print(available_seat_all)
