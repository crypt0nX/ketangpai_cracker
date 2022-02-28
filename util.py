import time
import requests
import json


def getToken(username, password):
    mainUrl = 'https://openapiv52.ketangpai.com/UserApi/login'
    data = {"email": "", "password": "", "remember": "1", "code": "", "mobile": "", "type": "login",
            "timestamp": 1643722734225, 'email': username, 'password': password,
            'timestamp': int(round(time.time() * 1000))}
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    }
    re = requests.post(url=mainUrl, data=data, headers=headers)
    re = eval(re.text)
    try:
        token = re["data"]["token"]
        uid = re["data"]["uid"]
        result = token
        print("登录成功")
        return result
    except Exception:
        print("登录失败")
        return False

def getAllCourse(token):
    mainUrl = 'https://openapiv5.ketangpai.com/courseApi/semesterCourseList'
    data = {"isstudy": "1", "search": "", "reqtimestamp": int(round(time.time() * 1000))}
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
        "Token": "%s" % token}
    re = requests.post(url=mainUrl, data=data, headers=headers)
    re = json.loads(re.text)['data']
    return re


def get_isCheckAttence(token, courseList):
    mainUrl = 'https://openapiv5.ketangpai.com//AttenceApi/getNotFinishAttenceStudent'
    data = {"courseid": "", "reqtimestamp": int(round(time.time() * 1000))}
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
        "Token": "%s" % token}
    for id in courseList:
        data["courseid"] = id['id']
        re = requests.post(url=mainUrl, data=data, headers=headers)
        re = eval(re.text)
        if re["data"]["lists"]:
            type_id = re["data"]["lists"][0]['type']
            course_id = re["data"]["lists"][0]['id']
            course_name = id['coursename']
            return [type_id, course_name, course_id]
