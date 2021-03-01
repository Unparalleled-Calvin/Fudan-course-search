### 复旦本科生刷课脚本

本脚本改写自https://github.com/ICYPOLE/Fudan-Course-Search [复旦研究生课程刷课、捡漏脚本]  by [ICYPOLE](https://github.com/ICYPOLE)



### 使用方法

将要蹲的**课程序号**，即选课查询表单的第一栏，按行写入lessons.txt

登录选课系统，提交一次请求，从浏览器network栏获得cookie，将cookie拷贝到cookies.txt文件中

cookie获得方式如图

![cookie获得方式](./cookie获得方式.png)

执行py文件，会不断对考察列表轮询，查看当前课程是否已选满。

![效果示意](./效果示意.png)



### 使用注意

1. 本脚本采用python编写，需要安装python。(可以自行打包成exe)

2. 由于脚本采用cookie进行发包，每次登陆选课系统cookie都不相同，使用脚本过程中不应在其他设备用同一账号登陆选课系统。

3. 由于本科生选课可能需要输入验证码等，所以脚本不涉及抢课操作

4. **使用者可配合win10toast包进行系统消息提示、或是yagmail包进行邮件提示**

5. 本脚本还处于测试阶段，如果出现bug，欢迎指出