import time
import os
import sys
from typing import *
import zipfile

import keyring
import requests
from tqdm import tqdm
from pprint import pprint
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
        # 记住密码
        if remember:
            username = keyring.get_password(service_name,'username')
            # 密码存在
            if username:
                self.username = username
                self.password = keyring.get_password(service_name,username)
            # 密码不存在，输入并保存
            else:
                self.username = input("请输入用户名：")
                self.password = input("请输入密码：")
                keyring.set_password(service_name,self.username,self.password)
                keyring.set_password(service_name,'username',self.username)
        # 不记住密码
        else:
            self.username = input("请输入用户名：")
            self.password = input("请输入密码：")
            username = keyring.get_password(service_name,'username')
            # 密码存在，清除密码
            if username:
                keyring.delete_password(service_name,username)
                keyring.delete_password(service_name,'username')
            # 密码不存在，什么都不需要做
            else:
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




class xiaoya_scrpit():
    def __init__(self):
        self.HomeworkDict = {}
        driver1 = MyDriver(working_path=working_path,show_web_page=show_web_page)
        self.login(driver1)
        self.ApplyTask(driver1)
        pprint(self.HomeworkDict)


    def login(self,driver1:MyDriver):
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

        # 初始化用户对象，存储了账号密码
        user1 = User(remember=remember_password,service_name=SERVICE_NAME)


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
            elif instructor==2:
                self.do_tasks(driver1)
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
        打印所有需要完成的任务
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
                driver.close()
                driver.switch_to.window(main_handle)
                count+=1
        else:   # 没有任务
            pass


        if flag:
            print(f'\t\033[32m本课程暂时没有任务\033[0m')     # 绿色



    def do_tasks(self,driver1:MyDriver):
        '''
        完成课程界面的所有任务
        要求已经进入课程页面
        完成后不会返回主界面
        '''
        driver = driver1.driver
        wait = WebDriverWait(driver, 10)
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


        # 点击自主观看
        self_watch = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'.ant-tabs-nav-animated > :nth-child(1) > :nth-child(2)'))
        )
        self_watch.click()

        # 选中时：<input type="checkbox" class="ant-checkbox-input" value="" checked="">
        # 空白时：<input type="checkbox" class="ant-checkbox-input" value="">

        # 点击仅关注未完成任务
        undown_task = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@class='ant-checkbox-input']"))
        )

        if not undown_task.get_attribute('checked'):
            undown_task.click()
        

        #如果有每页显示选项，说明有任务，否则就是没任务，退出
        message_per_page_button = driver.find_elements(by=By.CSS_SELECTOR,value='.ant-select-selection')
        if message_per_page_button:
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

            tasks = driver.find_elements(by=By.CSS_SELECTOR,value='tr.ant-table-row-level-0 span span')
            while count<len(tasks):
                tasks = driver.find_elements(by=By.CSS_SELECTOR,value='tr.ant-table-row-level-0 span span')
                task_name = tasks[count].text
                tasks[count].click()
                count+=1
                #切换到视频页面
                handles = driver.window_handles
                for handle in handles:
                    driver.switch_to.window(handle)
                    time.sleep(2)
                    if f'{task_name}' in driver.title:
                        break
                # 完成观看任务
                if '.mp4' in task_name or '.flv' in task_name:
                    self.watch_video(driver=driver,wait=wait,video_name=task_name)
                elif '.pptx' in task_name:
                    self.watch_pptx(driver=driver,wait=wait,task_name=task_name)
                else:
                    print(f'无法识别的类型')
                
                # 回到任务界面，并继续循环，直到任务全部完成
                driver.close()
                driver.switch_to.window(main_handle)


    def watch_video(self,driver1,video_name='') -> None:
        '''
        要求当前已经切换到video页面中,完成任务后不会关闭页面
        '''
        driver = driver1.driver
        wait = WebDriverWait(driver, 10)
        # 开始播放视频
        video_start = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'.outter'))
        )
        video_start.click()


        # 找到进度条游标
        progress_marker = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".prism-player  .prism-progress"))
        )

        # 把视频拨到起始位置
        action = ActionChains(driver)
        action.move_to_element(progress_marker)
        xoffset = (progress_marker.size['width']/2)-5
        action.move_by_offset(xoffset=-xoffset,yoffset=0)
        action.click()
        action.perform()

        # 找到显示进度的文本
        progressing = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".progress_container > span"))
        )

        # 监测完成进度，当完成进度达到100%时退出
        while progressing.text != f'已观看:100%':
            action.move_to_element(progress_marker)
            xoffset = (progress_marker.size['width']/2)-5
            action.move_by_offset(xoffset=-xoffset,yoffset=0)
            action.click()
            time.sleep(1)
            action.move_to_element(progress_marker)
            xoffset = (progress_marker.size['width']/2)-5
            action.move_by_offset(xoffset=xoffset,yoffset=0)
            action.click()
            action.perform()
            print(f'正在观看{video_name} {progressing.text}')
            time.sleep(1)
        

        # 点击完成任务
        task_down = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'.btn_content'))
        )
        task_down.click()
        self.mp4+=1


    def watch_pptx(self,driver1,task_name:str='') -> None:
        '''
        要求当前已经切换到pptx页面中,完成任务后不会关闭页面
        '''
        driver = driver1.driver
        wait = WebDriverWait(driver, 10)
        while True:
            task_down = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,'.btn_content'))
            )
            task_down.click()
            try:
                button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,'button.ant-btn-primary'))
                )
                button.click()
            except:
                break
            time.sleep(1)
            print(f'正在观看：{task_name}')
        
        self.pptx+=1




if __name__ == '__main__':
    task1 = xiaoya_scrpit()
    os.system('pause')
