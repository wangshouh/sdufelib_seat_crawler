print('name\tid\n三楼\t28\n四楼\t29\n五楼\t30\n六楼\t31\n七楼\t32\n')

order_id = input('请输入您预约楼层的id: ')

with open('config.txt', 'w') as f:
    f.write('http://libst.sdufe.edu.cn/web/seat2/area/{}/day/'.format(order_id))