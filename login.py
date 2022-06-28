import base64
import hashlib
import json
import random
import string

import requests
from bs4 import BeautifulSoup
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

BLOCK_SIZE = 16


def generate_random_str(length):
    """
    生成随机字符串
    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def encrypt(plain_text, key):
    private_key = key.encode("utf-8")
    plain_text = pad((generate_random_str(
        64) + plain_text).encode('utf-8'), 16)
    iv = generate_random_str(16)
    print(iv)
    cipher = AES.new(private_key, AES.MODE_CBC, iv.encode("utf-8"))
    return base64.b64encode(cipher.encrypt(plain_text)).decode('utf-8')


def get_login_params(url, s):
    """
    获取lt参数,用于登录
    """

    resp = s.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    lt = soup.find("input", attrs={'id': "execution"}).attrs['value']
    salt = soup.find("input", attrs={'id': "pwdEncryptSalt"}).attrs['value']
    return lt, salt


def get_login_api(username, password):
    """
    登入系统
    """


def get_login_api(username, password):
    """
    登入系统
    """
    url = "http://ids.sdufe.edu.cn/authserver/login?service=http%3A%2F%2Flibst.sdufe.edu.cn%2Fcas%2Findex.php%3Fcallback%3Dhttp%3A%2F%2Flibst.sdufe.edu.cn%2Fhome%2Fweb%2Ff_second"

    headers = {
        'Host': 'ids.sdufe.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en,en-US;q=0.8,zh-CN;q=0.7,zh;q=0.5,zh-TW;q=0.3,zh-HK;q=0.2',
        'Origin': 'http://ids.sdufe.edu.cn',
        'DNT': '1',
        'Referer': 'http://ids.sdufe.edu.cn/authserver/login?service=http%3A%2F%2Flibst.sdufe.edu.cn%2Fcas%2Findex.php%3Fcallback%3Dhttp%3A%2F%2Flibst.sdufe.edu.cn%2Fhome%2Fweb%2Ff_second',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    s = requests.session()
    execution, salt = get_login_params(url, s)
    print(salt)
    password = encrypt(password, salt)
    print(password)

    data = {
        'lt': '',
        '_eventId': 'submit',
        'username': username,
        'password': password,
        "captcha": "",
        "execution": execution,
        "cllt": "userNameLogin",
        "dllt": "generalLogin"
    }
    response = s.post(url, data=data)
    resp = BeautifulSoup(response.text, 'html.parser')
    print(resp)
    if resp.body.a['href'] == 'http://libst.sdufe.edu.cn/home/web/f_second':
        print('登录成功')
    else:
        print('登录失败')

    redit_list = response.history
    login_api = redit_list[len(redit_list)-1].headers["location"]
    return "http://libst.sdufe.edu.cn" + login_api
