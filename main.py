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

def get_url_dict(timeid_list, now_day, now_time):
    '''
    获取url列表
    '''
    for i in timeid_list:
        i['referer_url'] = "http://libst.sdufe.edu.cn/web/seat3?area={}&segment={}&day={}&startTime={}&endTime=22:00".format(i['id'], i['book_time_id'], now_day, now_time)
        i['api_url'] = "http://libst.sdufe.edu.cn/api.php/spaces_old?area={}&segment={}&day={}&startTime={}&endTime=22:00".format(i['id'], i['book_time_id'], now_day, now_time)
    return timeid_list

def get_available_seat(url_dict, s):
    '''
    获取可用座位信息
    '''
    available_seat_list = []
    for i in url_dict:
        headers = {
            'Referer': i['referer_url']
        }
        seat_list = s.get(i['api_url'], headers=headers).json()['data']['list']
        i['available_seat'] = []
        for seat_info in seat_list:
            if seat_info['status'] == 1:
                i['available_seat'].append(
                    {
                        'seat_id': seat_info['id'],
                        'seat_no': seat_info['no'],
                        'segment': i['book_time_id'],
                        'seat_name': i['name'] + '-' + seat_info['no']
                    }
                )

    return url_dict

def output_optimize(available_seat_all):
    '''
    输出座位
    '''
    print('name\t\t\tid\tsegment')
    for floor in available_seat_all:
        for segment in floor:
            if segment['available_seat'] != []:
                for seat in segment['available_seat']:
                    print(
                        seat['seat_name'], '\t', 
                        seat['seat_id'], '\t', 
                        seat['segment']
                        )

    


now_day = datetime.now().strftime('%Y-%m-%d')
now_time = datetime.now().strftime('%H:%M')
config = load_config(now_day)
available_seat_all = []

s = requests.session()
for i in config:
    complete_url = i['complete_url']
    order_id = i['order_id']
    timeid_list = get_timeid_list(complete_url, order_id, s)
    url_dict = get_url_dict(timeid_list, now_day, now_time)
    available_seat_list = get_available_seat(url_dict, s)
    available_seat_all.append(available_seat_list)
output_optimize(available_seat_all)
