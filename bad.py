import requests
import sys
import os
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.adapters.DEFAULT_RETRIES = 10


def exploit_post_code(data, token):
    main_url = 'https://openapiv51.ketangpai.com/AttenceApi/checkin'
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/65.0.3325.181 Safari/537.36",
        "Token": "%s" % token}
    re = requests.post(url=main_url, data=data, headers=headers)
    re.keep_alive = False
    if r"\u7b7e\u5230\u6210\u529f" in re.text:
        msg = "签到成功，正确代码为%s" % str(data["code"])
        print(msg)
        return False
        '''
        cmd = "kill -9 " + str(os.getpid())
        os.system(cmd)
        sys.exit(1)
        '''


def exploit_code(data, payload, token):
    dict_data = eval(data)
    dict_data["code"] = payload
    msg = '正在尝试%s' % str(payload)
    sys.stdout.write(str(msg) + '\r')
    try:
        exploit_post_code(dict_data, token)
    except Exception as e:
        exploit_code(data, payload, token)


def geo_exploit(data, token):
    main_url = 'https://openapiv51.ketangpai.com/AttenceApi/checkin'
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/65.0.3325.181 Safari/537.36",
        "Token": "%s" % token}
    re = requests.post(url=main_url, data=data, headers=headers)
    re.keep_alive = False
    if r"\u7b7e\u5230\u6210\u529f" in re.text:
        msg = "签到成功"
        print(msg)
        '''
        cmd = "kill -9 " + str(os.getpid())
        os.system(cmd)
        sys.exit(1)
        '''
