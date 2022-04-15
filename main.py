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


def get_available_seat(resp, segament):
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
                    'segment': segament,
                    'seat_name': seat_info['area_name'] + '-' + seat_info['no']
                }
            )

    return available_seat_list


async def get_api_content(api_url, segament):
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url, headers={"Referer": "test"}) as resp:
            api_content = await resp.json()
            available_seat = get_available_seat(api_content, segament)
            return available_seat


def output_optimize(available_seat_all):
    '''
    输出座位
    '''
    print('name\t\tid\tsegment')
    for floor in available_seat_all:
        for seat in floor:
            print(
                seat['seat_name'], '\t',
                seat['seat_id'], '\t',
                seat['segment'],
            )


def book_seat(userid, segment, token, order_id, s):
    '''
    预约座位
    '''
    headers = {
        'Referer': "test"
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


def main():
    api_list = get_url_list()
    loop = asyncio.get_event_loop()
    tasks = [get_api_content(url, segament) for url, segament in api_list]
    available_seat_all = loop.run_until_complete(asyncio.gather(*tasks))
    output_optimize(available_seat_all)

    order_id = input('请输入您预约的id: ')
    segment = input('请输入您预约的segment: ')
    userid = input('请输入您的学号: ')
    password = input('请输入您的密码: ')
    token = login_token(s, userid , password)
    book_seat(userid, segment, token, order_id, s)

if __name__ == '__main__':
    main()