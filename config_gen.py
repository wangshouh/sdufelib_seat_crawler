import json

print('name\tid\n三楼\t28\n四楼\t29\n五楼\t30\n六楼\t31\n七楼\t32\n')

order_id = input("请输入您预约楼层的id\(以','分割\): ")

order_id_list = order_id.split(',')
with open('config.json', 'w') as f:
    f.write(json.dumps(order_id_list))