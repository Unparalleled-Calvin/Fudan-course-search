import json
import requests
import time
import threading
import re
import base64

class CourseSearcher():

    def __init__(self):
        self.cookies = dict()
        self.cookies_file = 'cookies.txt'
        self.lessons_file = 'lessons.txt'
        self.info_file = 'info.txt'
        self.urls_file = 'urls.txt'
        with open(r"urls.txt", "r") as f:
            [self.qurl, self.curl] = f.read().splitlines()[0:2]
        self.lessonNo_list = list()
        self.form_data={
            'lessonNo': '' ,
            'courseCode': '',
            'courseName': '分布式',
        }

    def read_lessons(self):
        with open(self.lessons_file, 'r', encoding = 'utf-8') as f:
            self.lessonNo_list = f.read().splitlines()

    def read_cookies(self):
        with open(self.cookies_file, 'r', encoding='utf-8') as f:
            cookies_txt = f.read().strip(';')  # 读取文本内容
            # 由于requests只保持 cookiejar 类型的cookie，而我们手动复制的cookie是字符串需先将其转为dict类型后利用requests.utils.cookiejar_from_dict转为cookiejar 类型
            # 手动复制的cookie是字符串转为字典：
            for cookie in cookies_txt.split(';'):
                name, value = cookie.strip().split('=', 1)  # 用=号分割，分割1次
                self.cookies[name] = value  # 为字典cookies添加内容
        # 将字典转为CookieJar：
        cookiesJar = requests.utils.cookiejar_from_dict(
            self.cookies, cookiejar=None, overwrite=True)
        return cookiesJar

    # 刷课
    def search(self):
        self.read_lessons()
        self.session = requests.session()
        self.session.cookies = self.read_cookies()
        while True:
            for lessonNo in self.lessonNo_list:
                time.sleep(0.1)
                self.form_data['lessonNo'] = lessonNo
                # try:
                response = self.session.post(
                        self.qurl,
                        data = self.form_data,
                        timeout = 5
                )
                response = response.content.decode()
                self.is_course_available(response,lessonNo)
                # except Exception as e:
                #     print('cookies错误，请尝试更改cookies，并重新运行')
                #     continue

    def is_course_available(self,response,lessonNo):
        id_name = re.findall(r"""{id:([\d]+?),no:["']%s["'],name:["'](.+?)['"],"""%lessonNo,response)[0]
        ret = re.findall(r"""%s':{sc:([\d]+?),lc:([\d]+?)}"""%id_name[0],response.splitlines()[1])[0]
        if(int(ret[0])<int(ret[1])):
            print("课程序号为%s的%s，当前%s/%s，可选"%(lessonNo,id_name[1],ret[0],ret[1]))
            print("----------- 正在尝试选课中 --------------")
            self.frequent_course_request(id_name[0])
        else:
            print("课程序号为%s的%s，当前%s/%s，不可选"%(lessonNo,id_name[1],ret[0],ret[1]))

    # 抢课（捡漏）
    def frequent_course_request(self, course_id):
        form_data = {
            'optype': 'true',
            'operator0': str(course_id) + ':true:0',
            'captcha_response': self.get_captcha()
        }
        self.select_course(form_data)

    def select_course(self, form_data):
        try:
            response = self.session.post(
                url=self.curl,
                data=form_data,
                timeout=5
            )
            response = response.content.decode(encoding='utf-8')
            if(response.find('成功') != -1):
                print("选课成功")
            elif(response.find('已经选过') != -1):
                print("选课失败:你已经选过这门课了")
            elif(response.find('不开放') != -1):
                print("选课失败:当前选课不开放")
            elif(response.find('验证码') != -1):
                print('选课失败:验证码错误')
        except Exception as e:
            print(e)
            print("选课出错，请检查")

    def get_captcha(self):
        try:
            response = self.session.get(
                url='https://xk.fudan.edu.cn/xk/captcha/image.action',
                timeout=5
            )
            img_b64 = base64.b64encode(response.content).decode()
            # get captcha from remote api
            captcha = self.remote_captcha_identify(img_b64)
            return captcha
        except:
            print("获取验证码失败")
    
    def remote_captcha_identify(self, base64):
        with open(self.info_file, 'r', encoding = 'utf-8') as f:
            info_list = f.read().splitlines()
        data = {
            'image' : base64,
            'username' : info_list[0],
            'password' : info_list[1],
            'typeid' : 3
        }
        result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
        if result['success']:
            return result["data"]["result"]
        else:
            print(result["message"])
            return ""
            
if __name__ == "__main__":
    s = CourseSearcher()
    m = s.search()
