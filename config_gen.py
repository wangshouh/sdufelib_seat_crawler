import json
from login import get_login_api

print('name\tid\n三楼\t28\n四楼\t29\n五楼\t30\n六楼\t31\n七楼\t32\n')

order_id = input("请输入您预约楼层的id\(以','分割\): ")
username = input('请输入您的学号: ')
password = input('请输入您的密码: ')

order_id_list = order_id.split(',')

login_api = get_login_api(username, password)
with open('config.json', 'w') as f:
    config_dict = {
        "login_api": login_api,
        "order_id_list": order_id_list
    }
    f.write(json.dumps(config_dict))