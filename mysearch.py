import json
import requests
import time
import threading
import re


class CourseSearcher():

    def __init__(self):
        self.cookies = dict()
        self.cookies_file = 'cookies.txt'
        self.lessons_file = 'lessons.txt'
        self.url = 'https://xk.fudan.edu.cn/xk/stdElectCourse!queryLesson.action?profileId=1527'
        self.lessonNo_list = list()
        self.form_data={
            'lessonNo': '' ,
            'courseCode': '',
            'courseName': '',
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
                time.sleep(1.5)
                self.form_data['lessonNo'] = lessonNo
                try:
                    response = self.session.post(
                            self.url,
                            data = self.form_data,
                            timeout = 5
                    )
                    response = response.content.decode()
                    self.is_course_available(response,lessonNo)
                except:
                    print('cookies错误，请尝试更改cookies，并重新运行')
                    continue

    def is_course_available(self,response,lessonNo):
        id_name = re.findall(r"""{id:([\d]+?),no:["']%s["'],name:["'](.+?)['"],"""%lessonNo,response)[0]
        ret = re.findall(r"""%s':{sc:([\d]+?),lc:([\d]+?)}"""%id_name[0],response.splitlines()[1])[0]
        if(int(ret[0])<int(ret[1])):
            print("课程序号为%s的%s，当前%s/%s，可选"%(lessonNo,id_name[1],ret[0],ret[1]))
        else:
            print("课程序号为%s的%s，当前%s/%s，不可选"%(lessonNo,id_name[1],ret[0],ret[1]))
        
        
if __name__ == "__main__":
    s = CourseSearcher()
    m = s.search()
