## SDUFE Library Reservation Seat Monitoring Crawler

### How to use

1. Install Python package `requests`.You can use `pip install requests` to install it.
1. Run the `config.py` file.You can use command `python config.py` to run file.
1. Run the `main.py` file.The program output is similar to `['四层南-035']`.You need to confirm the exact location based on the campus you located.

### Additional information

1. If you are in China, you can use [TUNA pypi mirror](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/) to install `requests`. The command is `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests`.
1. Now, the crawler config only support Shengjing(圣井) campus.

1. If you in other campus, you can read source code and modify it.