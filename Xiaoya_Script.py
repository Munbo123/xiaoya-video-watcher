import time
import re
import os

import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import WebDriverException

from MyDriver import MyDriver


class Xiaoya_scrpit():
    def __init__(self,working_path,output:scrolledtext.ScrolledText):
        self.HomeworkDict = {}
        self.output = output
        self.URL = r'https://whut.ai-augmented.com/app/jx-web/mycourse'
        self.working_path = working_path


        self.ansi_color = {
            # Reset
            'reset_font': "\033[0m",
            
            # Text colors
            'black_font': "\033[30m",
            'red_font': "\033[31m",
            'green_font': "\033[32m",
            'yellow_font': "\033[33m",
            'blue_font': "\033[34m",
            'magenta_font': "\033[35m",
            'cyan_font': "\033[36m",
            'white_font': "\033[37m",

            # Bright text colors
            'bright_black_font': "\033[90m",
            'bright_red_font': "\033[91m",
            'bright_green_font': "\033[92m",
            'bright_yellow_font': "\033[93m",
            'bright_blue_font': "\033[94m",
            'bright_magenta_font': "\033[95m",
            'bright_cyan_font': "\033[96m",
            'bright_white_font': "\033[97m",

            # Background colors
            'black_bg': "\033[40m",
            'red_bg': "\033[41m",
            'green_bg': "\033[42m",
            'yellow_bg': "\033[43m",
            'blue_bg': "\033[44m",
            'magenta_bg': "\033[45m",
            'cyan_bg': "\033[46m",
            'white_bg': "\033[47m",

            # Bright background colors
            'bright_black_bg': "\033[100m",
            'bright_red_bg': "\033[101m",
            'bright_green_bg': "\033[102m",
            'bright_yellow_bg': "\033[103m",
            'bright_blue_bg': "\033[104m",
            'bright_magenta_bg': "\033[105m",
            'bright_cyan_bg': "\033[106m",
            'bright_white_bg': "\033[107m",

            # Text styles
            'bold': "\033[1m",
            'dim': "\033[2m",
            'italic': "\033[3m",  # Not widely supported
            'underline': "\033[4m",
            'blink': "\033[5m",
            'reverse': "\033[7m",
            'hidden': "\033[8m",
            'strike': "\033[9m",  # Not widely supported
        }
        # ANSI 转义符和颜色的映射表
        self.ansi_color_map = {
            # Text colors
            '30': 'black',
            '31': 'red',
            '32': 'green',
            '33': 'yellow',
            '34': 'blue',
            '35': 'magenta',
            '36': 'cyan',
            '37': 'white',

            # Bright text colors (mapped to standard brighter colors)
            '90': 'gray',
            '91': 'lightcoral',  # Bright red
            '92': 'lightgreen',
            '93': 'lightyellow',
            '94': 'lightskyblue',
            '95': 'orchid',      # Bright magenta
            '96': 'paleturquoise',
            '97': 'white',

            # Background colors
            '40': 'black',
            '41': 'red',
            '42': 'green',
            '43': 'yellow',
            '44': 'blue',
            '45': 'magenta',
            '46': 'cyan',
            '47': 'white',

            # Bright background colors (mapped to lighter backgrounds)
            '100': 'gray',
            '101': 'lightcoral',
            '102': 'lightgreen',
            '103': 'lightyellow',
            '104': 'lightskyblue',
            '105': 'orchid',
            '106': 'paleturquoise',
            '107': 'white',

            # Styles
            '0': 'black',          # Reset (use default color)
            '1': 'bold',        # Bold text (can use a font change in Tkinter)
            '2': 'dim',         # Dim (not directly supported in Tkinter)
            '3': 'italic',      # Italic (if supported by Tkinter fonts)
            '4': 'underline',   # Underline
            '5': 'blink',       # Blink (not supported in Tkinter)
            '7': 'reverse',     # Reverse (swap foreground and background colors)
            '8': 'black',          # Hidden (not supported in Tkinter)
            '9': 'overstrike',  # Overstrike (strikethrough, if supported)
        }

        
    def write_to_output(self, message):
        """
        解析带有 ANSI 转义符的文本并在 GUI 输出彩色文本。
        """
        print(message)
        # ANSI 转义符的正则表达式
        ansi_pattern = re.compile(r'\033\[(\d+)m')

        # 用于分割文本的部分
        segments = ansi_pattern.split(str(message))

        current_color = "black"  # 默认颜色
        for i, segment in enumerate(segments):
            if i % 2 == 0:  # 普通文本部分
                if segment:
                    self.output.tag_configure(current_color, foreground=current_color)
                    self.output.insert(tk.END, segment, current_color)
            else:  # ANSI 转义符部分
                color_code = segment
                current_color = self.ansi_color_map.get(color_code, "black")
        
        self.output.insert(tk.END,'\n')
        # 确保视图滚动到底部
        self.output.see(tk.END)


    def login(self,username,password,not_show_page):
        # 先初始化driver,存储在对象中
        self.driver = MyDriver(working_path=self.working_path,not_show_page=not_show_page).driver
        # 获取wait和url
        wait = WebDriverWait(self.driver, 10)
        url = r'https://whut.ai-augmented.com/app/jx-web/mycourse'


        self.write_to_output(f'正在登录中……')
        # 打开页面
        self.driver.get(url)

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
        self.driver.maximize_window()

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
        username_input.send_keys(f'{username}')


        # 输入密码
        password_input = wait.until(
            EC.visibility_of_element_located((By.ID, 'pd'))
        )
        password_input.send_keys(f'{password}')


        #登录
        login_button = wait.until(
            EC.element_to_be_clickable((By.ID,"index_login_btn"))
        )
        login_button.click()


        #暂不处理密码问题，这个可能会没有
        time.sleep(1)
        if not self.driver.find_elements(by=By.CSS_SELECTOR,value='noscript'):
            button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,'button.ant-btn-default >span'))
            )
            button.click()
        
        self.write_to_output("登陆成功！")


    def ApplyTask(self,task_num:int):
        '''
        进入每一个课程，并对每一个课程调用task
        '''
        wait = WebDriverWait(self.driver, 10)
        page_num = 0
        course_num = 0


        while True:
            # 找到课程页码，并点击
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'.ant-pagination-item'))
            )
            pages = self.driver.find_elements(by=By.CSS_SELECTOR,value='.ant-pagination-item')
            pages[page_num].click()
            # 找到当前页显示的所有课程，返回为列表
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'.card_list'))
            )
            courses = self.driver.find_elements(by=By.CSS_SELECTOR,value='.aia_course_card > .ta_mainInfo > span:nth-child(1)')
            # 进入课程界面
            courses[course_num].click()


            NameTag = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR,'span.group_name'))
                )
            self.write_to_output(f'\033[31m{NameTag.text}:\033[0m')    # 打印红色的课程名
            # 主要执行任务的部分
            if task_num==1:
                self._AllTaskName(NameTag.text)
            elif task_num==2:
                if self._AllTaskName(NameTag.text):
                    self._Finish_Task()
            else:
                self.write_to_output(f'无效的指令')

            # 回到主界面
            self.driver.get(url=self.URL)

            course_num+=1
            if course_num==8:   
                course_num = 0
                page_num+=1
            # 当前课程指向超过本页课程数量，则跳出循环
            if page_num>=len(pages) or course_num>=len(courses):
                break  
        self.write_to_output(self.HomeworkDict)


    def _AllTaskName(self,CourseName):
        '''
        打印所有需要完成的任务(已经点进对应课程了)
        '''
        wait = WebDriverWait(self.driver, 10)
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


        message_per_page_button = self.driver.find_elements(by=By.CSS_SELECTOR,value='.ant-select-selection')
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

            # 获取显示的所有任务
            tasks = self.driver.find_elements(by=By.CSS_SELECTOR,value='tr.ant-table-row-level-0')
            # 取得每一条任务
            for task in tasks:
                # 第一个td元素，下面有任务的名字
                name = task.find_element(by=By.CSS_SELECTOR,value='td:nth-of-type(1) > a >span >span').text
                # 第八个td元素，text内容即为截止时间
                end_time = task.find_element(by=By.CSS_SELECTOR,value='td:nth-of-type(8)').text
                # 输出信息
                self.write_to_output(f"\t{self.ansi_color['blue_font']}{name}  {end_time}{self.ansi_color['reset_font']}")
                # 添加到字典
                self.HomeworkDict[CourseName] = self.HomeworkDict.get(CourseName,[])+[name]
                flag = False




        if flag:
            self.write_to_output(f"\t{self.ansi_color['green_font']}本课程暂时没有任务{self.ansi_color['reset_font']}")     # 绿色
            return False
        else:
            return True


    def _Finish_Task(self):
        '''
        完成课程界面的所有任务
        '''
        wait = WebDriverWait(self.driver, 10)

        # 获取课程编号
        url = self.driver.current_url
        group_id = str(url.split('/')[-2])  # 去掉可能存在的查询参数

        # 获取所有的cookies
        cookies = self.driver.get_cookies()

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
            self.write_to_output(f'该课程没有任何任务！')


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
                        self.write_to_output(f"{name}\n\t{self.ansi_color['green_font']}成功{result}{self.ansi_color['reset_font']}")
                    else:
                        self.write_to_output(f"{name}\n\t{self.ansi_color['red_font']}失败{result}{self.ansi_color['reset_font']}")

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
                        self.write_to_output(f"{name}\n\t{self.ansi_color['green_font']}成功{result}{self.ansi_color['reset_font']}")
                    else:
                        self.write_to_output(f"{name}\n\t{self.ansi_color['red_font']}失败{result}{self.ansi_color['reset_font']}")


                else:
                    self.write_to_output(f"{name}\n\t{self.ansi_color['magenta_font']}未知类型，跳过{self.ansi_color['reset_font']}")
            else:           #不是任务（比如老师上传的ppt，视频，但没布置成作业的
                pass

