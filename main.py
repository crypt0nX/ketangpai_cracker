import sys
import threading
from colorama import init, Fore
import util
import time
import bad
import os
import json

init(autoreset=False)


def read_config():
    with open('config.json') as f:
        file = f.read()
        f.close()
        config = json.loads(file)
        return config


def main(username, password):
    while True:
        auth_info = util.getToken(username, password)
        if not auth_info:
            sys.exit()
        token = auth_info
        course_info = util.get_isCheckAttence(token, util.getAllCourse(token))
        if course_info and course_info[0] == '1':
            print("发现考勤，课程为 %s, 考勤类型为数字考勤，开始爆破" % course_info[1])
            try:
                f = open('wordlist.txt', 'r')
                msg = f.read().split('\n')
                target_num = int(50)
                data = '{"id":"%s","code":"","reqtimestamp":%d}' % (course_info[2], int(round(time.time() * 1000)))
                i = 0
                while True:
                    config = read_config()
                    sign = config["is_success"]
                    if threading.active_count() - 1 < target_num and i < len(msg) and sign != "True":
                        t = threading.Thread(target=bad.exploit_code, args=(data, msg[i], token,))
                        t.start()
                        i += 1
                    elif i >= len(msg):
                        break
            except Exception:
                print("没有签到！")
        elif course_info and course_info[0] == '2':
            print("发现考勤，课程为 %s, 考勤类型为GPS考勤，开始签到" % course_info[1])
            try:
                timestamp = int(round(time.time() * 1000))
                data = '{"id":"%s","code":"","unusual":0,"latitude":"%s","longitude":"%s",' \
                       '"accuracy":"null","clienttype":1,"reqtimestamp":%d}' % (
                           course_info[2], config['latitude'], config['longitude'], timestamp)
                bad.geo_exploit(data, token)
            except Exception:
                print("没有签到！")
        else:
            print("没有签到或者签到类型不支持！！")
        print("正在等待下一次检查")
        time.sleep(2*60)


if __name__ == '__main__':
    main("your_username", "your_password")  # 改成你自己的用户名和密码
