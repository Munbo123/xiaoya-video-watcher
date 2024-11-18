import time
import os
import sys
from typing import *
import zipfile

import keyring
import requests
from tqdm import tqdm
from pprint import pprint
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import WebDriverException


# 是否显示界面，如果为True,则显示，如果为False，则不显示
show_web_page = True
# 是否记住账号密码，若为True,在第一次输入后会自动记住，下一次无需输入，若为False，则每次都需要输入账号密码
remember_password = True


# 获取工作路径
if hasattr(sys,'_MEIPASS'):
    working_path = os.getcwd()
else:
    working_path = os.path.dirname(__file__)
DRIVER_PATH = os.path.join(working_path,'driver','msedgedriver.exe')


# 定义常量
SERVICE_NAME = 'MyApp'
URL = r'https://whut.ai-augmented.com/app/jx-web/mycourse'


class User():
    def __init__(self,remember,service_name='MyApp'):
        if remember:    # 记住密码
            username = keyring.get_password(service_name,'username')
            if username:        # 密码存在
                self.username = username
                self.password = keyring.get_password(service_name,username)
            else:       # 密码不存在，输入并保存
                self.username = input("请输入用户名：")
                self.password = input("请输入密码：")
                keyring.set_password(service_name,self.username,self.password)
                keyring.set_password(service_name,'username',self.username)
        else:        # 不记住密码
            self.username = input("请输入用户名：")
            self.password = input("请输入密码：")
            username = keyring.get_password(service_name,'username')
            if username:        # 密码存在，清除密码
                keyring.delete_password(service_name,username)
                keyring.delete_password(service_name,'username')
            else:               # 密码不存在，什么都不需要做
                pass


class MyDriver():
    def __init__(self,working_path,show_web_page=True):
        self.show_web_page = show_web_page
        self.working_path = working_path     # driver文件夹应在工作目录下
        self.driver = None

        # 检查driver文件夹是否存在
        if not os.path.exists(os.path.join(self.working_path,"driver")):    # driver文件夹不存在
            os.makedirs(os.path.join(self.working_path,"driver"))
            with open(os.path.join(self.working_path,"driver",'说明.txt'),mode='w',encoding='utf-8') as f:  # 添加说明文件
                f.write(f'此文件夹存放的是脚本的driver程序，可以删除，但删除后下一次程序会花时间再次自动下载')
        else:   # driver文件夹存在
            pass


        # 配置options
        options = webdriver.EdgeOptions()
        options.add_argument('--ignore-certificate-errors') # 忽略证书警告
        options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 忽略证书警告
        if not self.show_web_page:  # 不显示网站页面（后台静默运行）
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument("--mute-audio")        # 网站静音
        else:   # 显示网站页面
            pass


        # 确保存在一个基础的driver
        if not os.path.exists(os.path.join(self.working_path,'driver','msedgedriver.exe')): # 不存在基础的driver，随便下载一个
            save_path = self.download_driver_zip('130.0.2849.56')
            self.unzip_file(zip_path=save_path)
        else:   # 存在基础的driver
            pass


        # 配置service对象
        service = Service(executable_path=os.path.join(self.working_path,'driver','msedgedriver.exe'))


        # 获取driver
        try:    # 用现存的driver尝试获取对象
            self.driver =  webdriver.Edge(service=service,options=options)  
        except WebDriverException as e: # 版本不匹配，下载新的driver
            version = e.msg.split()[-7]
            save_path = self.download_driver_zip(version)
            self.unzip_file(zip_path=save_path)
            self.driver = webdriver.Edge(service=service,options=options)


    def download_driver_zip(self,version:str) -> str:
        '''
        下载特定版本的driver，返回保存的路径
        '''
        driver_url = f'https://msedgedriver.azureedge.net/{version}/edgedriver_win64.zip'
        save_path = os.path.join(os.path.join(self.working_path,'driver'),'download_driver.zip')

        response = requests.get(url=driver_url,stream=True)
        with open(file=save_path,mode='wb') as f:
            for chunk in tqdm(response.iter_content(chunk_size=1024),desc="下载driver中……",total=(int(response.headers['Content-Length'])//1024)+1):
                if chunk:
                    f.write(chunk)
        print(f'driver下载成功！')
        return save_path


    def unzip_file(self,zip_path:str):
        '''
        解压文件并删除压缩包
        '''
        print(f'解压driver中……')       
        with zipfile.ZipFile(zip_path,'r') as zip_ref:
            zip_ref.extract(member='msedgedriver.exe',path=os.path.dirname(zip_path))
        print(f'解压成功！')
        os.remove(zip_path)


class Xiaoya_scrpit():
    def __init__(self,user:User):
        self.HomeworkDict = {}
        driver1 = MyDriver(working_path=working_path,show_web_page=show_web_page)
        self.login(driver1,user)
        self.ApplyTask(driver1)


    def login(self,driver1:MyDriver,user1:User):
        # 获取wait，driver和url
        driver = driver1.driver
        wait = WebDriverWait(driver, 10)
        url = r'https://whut.ai-augmented.com/app/jx-web/mycourse'


        print(f'正在登录中……')
        # 打开页面
        driver.get(url)

        # 点击不再提示分辨率问题
        input1 = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'label.css-1k979oh > span > input'))
        )
        input1.click()

        button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'button.css-1k979oh'))
        )
        button.click()


        # 最大化窗口
        driver.maximize_window()

        # 通过 ID 定位到 "统一身份认证" 标签项
        unified_identity_tab = wait.until(
            EC.element_to_be_clickable((By.ID, 'rc-tabs-0-tab-UnifiedIdentity'))
        )
        unified_identity_tab.click()


        # 通过name属性定位按钮
        login_button = wait.until(
            EC.element_to_be_clickable((By.NAME, 'password'))
        )
        login_button.click()


        # 输入账号
        username_input = wait.until(
            EC.visibility_of_element_located((By.ID, 'un'))
        )
        username_input.send_keys(f'{user1.username}')


        # 输入密码
        password_input = wait.until(
            EC.visibility_of_element_located((By.ID, 'pd'))
        )
        password_input.send_keys(f'{user1.password}')


        #登录
        login_button = wait.until(
            EC.element_to_be_clickable((By.ID,"index_login_btn"))
        )
        login_button.click()


        #暂不处理密码问题，这个可能会没有
        time.sleep(1)
        if not driver.find_elements(by=By.CSS_SELECTOR,value='noscript'):
            button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,'button.ant-btn-default >span'))
            )
            button.click()
        
        print("登陆成功！")


    def ApplyTask(self,driver1:MyDriver):
        '''
        进入每一个课程，并对每一个课程调用task
        '''
        driver = driver1.driver
        wait = WebDriverWait(driver, 10)
        page_num = 0
        course_num = 0

        print('请输入要完成的指令(输入数字)：')
        print('1.列出所有待完成的任务')
        print('2.完成所有自主观看任务')
        instructor = int(input())
        while True:
            # 找到课程页码，并点击
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'.ant-pagination-item'))
            )
            pages = driver.find_elements(by=By.CSS_SELECTOR,value='.ant-pagination-item')
            pages[page_num].click()
            # 找到当前页显示的所有课程，返回为列表
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'.card_list'))
            )
            courses = driver.find_elements(by=By.CSS_SELECTOR,value='.aia_course_card > .ta_mainInfo > span:nth-child(1)')
            # 进入课程界面
            courses[course_num].click()


            NameTag = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'span.group_name'))
                )
            print(f'\033[31m{NameTag.text}:\033[0m')    # 打印红色的课程名
            # 主要执行任务的部分
            if instructor==1:
                self.AllTaskName(driver1,NameTag.text)
                pprint(self.HomeworkDict)
            elif instructor==2:
                if self.AllTaskName(driver1,NameTag.text):
                    self.Finish_Task(driver1)
            else:
                print(f'无效的指令')


            # 回到主界面
            driver.get(url=URL)

            course_num+=1
            if course_num==8:   
                course_num = 0
                page_num+=1
            # 当前课程指向超过本页课程数量，则跳出循环
            if page_num>=len(pages) or course_num>=len(courses):
                break  


    def AllTaskName(self,driver1:MyDriver,CourseName):
        '''
        打印所有需要完成的任务(已经点进对应课程了)
        '''
        driver = driver1.driver
        wait = WebDriverWait(driver, 10)
        flag = True

        # 点击作业任务,可能需要先点击展开
        try:
            homework_task = wait.until(
                EC.presence_of_element_located((By.XPATH, "//li[@class='ant-menu-item ta_group_sider_item' and span[text()='作业任务']]"))
            )
            homework_task.click()
        except:
            # 展开
            button = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'i.trigger'))
            )
            button.click()
            # 再重新尝试点击
            homework_task = wait.until(
                EC.presence_of_element_located((By.XPATH, "//li[@class='ant-menu-item ta_group_sider_item' and span[text()='作业任务']]"))
            )
            homework_task.click()
        

        # 选中时：<input type="checkbox" class="ant-checkbox-input" value="" checked="">
        # 空白时：<input type="checkbox" class="ant-checkbox-input" value="">

        # 点击仅关注未完成任务
        undown_task = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@class='ant-checkbox-input']"))
        )
        if not undown_task.get_attribute('checked'):    # 没有选中，点击
            undown_task.click()
        else:   # 选中了，不需要点击
            pass


        message_per_page_button = driver.find_elements(by=By.CSS_SELECTOR,value='.ant-select-selection')
        if message_per_page_button:     #如果有每页显示选项，说明有任务
            #点击每页显示的选项
            message_per_page = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,'.ant-select-selection'))
            )
            message_per_page.click()

            #点击显示两百条
            button1 = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,'ul.ant-select-dropdown-menu > li:nth-child(5)'))
            )
            button1.click()

            count = 0
            main_handle = driver.current_window_handle
            task_num = len(driver.find_elements(by=By.CSS_SELECTOR,value='tr.ant-table-row-level-0 span span'))
            while count<task_num:
                tasks = driver.find_elements(by=By.CSS_SELECTOR,value='tr.ant-table-row-level-0 span span')
                task_name = tasks[count].text
                print(f'\t\033[33m{task_name}\033[0m')
                self.HomeworkDict[CourseName] = self.HomeworkDict.get(CourseName,[])+[task_name]
                flag = False
                # 回到任务界面，并继续循环，直到任务全部完成
                driver.switch_to.window(main_handle)
                count+=1
        else:   # 没有任务
            pass


        if flag:
            print(f'\t\033[32m本课程暂时没有任务\033[0m')     # 绿色
            return False
        else:
            return True


    def Finish_Task(self,driver1:MyDriver):
        '''
        完成课程界面的所有任务
        '''
        driver = driver1.driver
        wait = WebDriverWait(driver, 10)

        # 获取课程编号
        url = driver.current_url
        group_id = str(url.split('/')[-2])  # 去掉可能存在的查询参数

        # 获取所有的cookies
        cookies = driver.get_cookies()

        # 查找特定的cookie
        token = None
        for cookie in cookies:
            if cookie['name'] == 'WT-prd-access-token':
                token = cookie['value']
                break

        if token==None:
            token = input("token获取失败,请输入手动输入token: ") or os.environ.get("DEV_TOKEN")  # 获取token

        # 提交数据以完成自主观看任务
        endpoint = "https://whut.ai-augmented.com/api/jx-iresource/"
        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }


        url = f"{endpoint}resource/queryCourseResources?group_id={group_id}"  # 获取课程资源
        course_jobs = requests.get(url=url, headers=headers).json()["data"]
        if len(course_jobs)==0:
            print(f'该课程没有任何任务！')

        red_font = "\033[31m"
        green_font = "\033[32m"
        yellow_font = "\033[33m"
        blue_font = "\033[34m"
        magenta_font = "\033[35m"
        cyan_font = "\033[36m"
        orange_font = "\033[33m"
        reset_font = "\033[0m"

        for job in course_jobs:  # 遍历课程任务
            node_id = job["id"]  # 任务ID，在链接的最尾部
            job_type = job["type"]  # 任务类型
            name = job["name"]
            is_task = job["is_task"]

        
            if is_task:     # 是任务的话
                if job_type == 9:  # 9=视频
                    url = f"{endpoint}resource/task/studenFinishInfo?group_id={group_id}&node_id={node_id}"
                    assign_id = requests.get(url=url, headers=headers).json()[
                        "data"]["assign_id"]

                    url = f"{endpoint}resource/queryResource?node_id={node_id}"
                    result = requests.get(url=url, headers=headers).json()["data"]
                    quote_id = result["quote_id"]
                    media_id = result["resource"]["id"]
                    duration = result["resource"]["duration"]
                    task_id = result["task_id"]

                    data = {
                        "video_id": "0000000000000000000",  # 似乎不重要
                        "played": duration,
                        "media_type": 1,
                        "duration": duration,
                        "watched_duration": duration
                    }
                    url = f"{endpoint}vod/duration/{quote_id}"  # 提交视频观看时长
                    result = requests.post(url=url, headers=headers, json=data)

                    url = f"{endpoint}vod/checkTaskStatus"  # 完成视频任务
                    data = {
                        "group_id": group_id,
                        "media_id": media_id,
                        "task_id": task_id,
                        "assign_id": assign_id
                    }

                    result = requests.post(url=url, headers=headers, json=data).json()
                    if result['success']:
                        print(f"{name}\n\t{green_font}成功{result}{reset_font}")
                    else:
                        print(f"{name}\n\t{red_font}失败{result}{reset_font}")

                elif job_type == 6:  # 6=文档
                    task_id = job["task_id"]

                    url = f"{endpoint}resource/finishActivity"
                    data = {
                        "group_id": group_id,
                        "task_id": task_id,
                        "node_id": node_id
                    }
                    result = requests.post(url=url, headers=headers, json=data).json()
                    if result['success']:
                        print(f"{name}\n\t{green_font}成功{result}{reset_font}")
                    else:
                        print(f"{name}\n\t{red_font}失败{result}{reset_font}")


                else:
                    print(f"{name}\n\t{yellow_font}未知类型，跳过{reset_font}")
            else:           #不是任务（比如老师上传的ppt，视频，但没布置成作业的
                pass




if __name__ == '__main__':
    task1 = Xiaoya_scrpit()
    os.system('pause')
