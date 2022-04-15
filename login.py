import requests


def get_ticker(s):
    """
    获取lt参数,用于登录
    """

    url = 'http://ids.sdufe.edu.cn/authserver/login?service=http%3A%2F%2Flibst.sdufe.edu.cn%2Fcas%2Findex.php%3Fcallback%3Dhttp%3A%2F%2Flibst.sdufe.edu.cn%2Fhome%2Fweb%2Ff_second'
    resp = s.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    lt = soup.find("input", attrs={'name': "lt"}).attrs['value']
    return lt


def get_login_api(username, password):
    """
    登入系统
    """
    s = requests.session()
    lt = get_ticker(s)
    url = 'http://ids.sdufe.edu.cn/authserver/login?service=http%3A%2F%2Flibst.sdufe.edu.cn%2Fcas%2Findex.php%3Fcallback%3Dhttp%3A%2F%2Flibst.sdufe.edu.cn%2Fhome%2Fweb%2Ff_second'
    data = {'lt': lt,
            'execution': 'e1s1',
            '_eventId': 'submit',
            'username': username,
            'password': password,
            'rmShown': '1'
            }
    response = s.post(url, data=data)
    resp = BeautifulSoup(response.text, 'lxml')
    if resp.body.a['href'] == 'http://libst.sdufe.edu.cn/home/web/f_second':
        print('登录成功')
    else:
        print('登录失败')

    redit_list = response.history
    login_api = redit_list[len(reditList)-1].headers["location"]
    return login_api


def get_token(s, login_api):
    """
    获取token
    """

    _ = s.get(login_api)

    return s
