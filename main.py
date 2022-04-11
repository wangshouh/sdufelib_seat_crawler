import asyncio
import json
from datetime import datetime

import aiohttp
import requests

from login import login_token


async def get_api_list(order_id):
    async with aiohttp.ClientSession() as session:
        complete_url = "http://libst.sdufe.edu.cn/api.php/v3areas/" + order_id
        async with session.get(complete_url, headers={"Referer": "test"}) as resp:
            content = await resp.json()
            area_data = content['data']['list']['childArea']
            all_data = []
            for i in area_data:
                need_data = {
                    'name': i['name'],
                    'book_time_id': i['area_times']['data']['list'][0]['id'],
                    'id': i['id']
                }
                all_data.append(need_data)
        return all_data


def get_all_api():
    with open("config.json", 'r') as f:
        order_id_list = json.load(f)
    loop = asyncio.get_event_loop()
    tasks = [get_api_list(order_id) for order_id in order_id_list]
    time_id_list = loop.run_until_complete(asyncio.gather(*tasks))
    return time_id_list


def get_url_list():
    now_day = datetime.now().strftime('%Y-%m-%d')
    now_time = datetime.now().strftime('%H:%M')
    api_list = get_all_api()
    api_url_list = []
    for floor in api_list:
        for area in floor:
            api_url = "http://libst.sdufe.edu.cn/api.php/spaces_old?area={}&segment={}&day={}&startTime={}&endTime=22:00".format(
                area['id'], area['book_time_id'], now_day, now_time)
            api_url_list.append((api_url, area['book_time_id'],))
    return api_url_list


def get_available_seat(resp):
    '''
    获取可用座位信息
    '''
    available_seat_list = []
    seat_list = resp['data']['list']
    for seat_info in seat_list:
        if seat_info['status'] == 1:
            available_seat_list.append(
                {
                    'seat_id': seat_info['id'],
                    'seat_no': seat_info['no'],
                    'segment': i['book_time_id'],
                    'seat_name': i['name'] + '-' + seat_info['no']
                }
            )

    return available_seat_list


async def get_api_content(api_url, available_seat_all):
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url, headers={"Referer": "test"}) as resp:
            api_content = await resp.json()
            available_seat = get_available_seat(api_content)
            return available_seat


def output_optimize(available_seat_all):
    '''
    输出座位
    '''
    print('name\t\t\tid\tsegment\treferer_url')
    for floor in available_seat_all:
        for segment in floor:
            if segment['available_seat'] != []:
                for seat in segment['available_seat']:
                    print(
                        seat['seat_name'], '\t',
                        seat['seat_id'], '\t',
                        seat['segment'],
                        segment['referer_url']
                    )


def book_seat(userid, segment, token, referer_url, order_id, s):
    '''
    预约座位
    '''
    headers = {
        'Referer': referer_url
    }
    data = {
        'access_token': token,
        'user_id': userid,
        'segment': segment,
        'type': '1',
        'operateChannel': '2'
    }
    r = s.post('http://libst.sdufe.edu.cn/api.php/spaces/{}/book'.format(order_id),
               headers=headers, data=data)
    print(r.json()['msg'])


now_day = datetime.now().strftime('%Y-%m-%d')
now_time = datetime.now().strftime('%H:%M')
config = load_config(now_day)
available_seat_all = []
api_list = []
s = requests.session()
for i in config:
    complete_url = i['complete_url']
    order_id = i['order_id']
    timeid_list = get_timeid_list(complete_url, order_id, s)
    api_url_list = get_api_url(timeid_list, now_day, now_time)
    api_list += api_url_list
print("api list爬取完成")
print(api_list)
# loop = asyncio.get_event_loop()
# tasks = [get_api_content(url) for url in api_list]
# available_seat_all = loop.run_until_complete(asyncio.gather(*tasks))
# print(available_seat_all)
#     available_seat_list = get_available_seat(url_dict, s)
#     available_seat_all.append(available_seat_list)
# output_optimize(available_seat_all)

# order_id = input('请输入您预约的id: ')
# segment = input('请输入您预约的segment: ')
# referer_url = input('请输入您预约的referer_url: ')
# userid = input('请输入您的学号: ')
# token = login_token(s, userid='202003140805' , password='300415')
# book_seat(userid, segment, token, referer_url, order_id, s)
