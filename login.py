import requests
from bs4 import BeautifulSoup
import re

def get_ticker(s):
    """
    获取lt参数,用于登录
    """

    url = 'http://ids.sdufe.edu.cn/authserver/login?service=http%3A%2F%2Flibst.sdufe.edu.cn%2Fcas%2Findex.php%3Fcallback%3Dhttp%3A%2F%2Flibst.sdufe.edu.cn%2Fhome%2Fweb%2Ff_second'
    resp = s.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    lt = soup.find("input", attrs={'name': "lt"}).attrs['value']
    return lt

def do_login(s, username, password, lt):
    """
    登入系统
    """
    url = 'http://ids.sdufe.edu.cn/authserver/login?service=http%3A%2F%2Flibst.sdufe.edu.cn%2Fcas%2Findex.php%3Fcallback%3Dhttp%3A%2F%2Flibst.sdufe.edu.cn%2Fhome%2Fweb%2Ff_second'
    data = {'lt': lt,
            'execution': 'e1s1',
            '_eventId': 'submit',
            'username': username,
            'password': password,
            'rmShown': '1'
            }
    resp = BeautifulSoup(s.post(url, data=data).text, 'lxml') 
    if resp.body.a['href'] == 'http://libst.sdufe.edu.cn/home/web/f_second':
        print('登录成功')
    else:
        print('登录失败')

def get_token(s):
    """
    获取token
    """
    url = 'http://libst.sdufe.edu.cn/home/web/f_second'
    resp = s.get(url)
    token = re.findall('''(?<='access_token':\").*(?=")''', resp.text)[0]
    return token


def login_token(s, username, password):
    """
    登入系统
    """
    lt = get_ticker(s)
    do_login(s, username, password, lt)
    token = get_token(s)
    return token