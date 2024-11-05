from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import WebDriverException
import keyring
import time
import os
import sys
from typing import *
import requests
from tqdm import tqdm
import zipfile
DriverType = TypeVar('DriverType', bound=webdriver.Edge)
WaitType = TypeVar('WaitType',bound=WebDriverWait)



# 这三项可以进行修改
# 是否显示界面，如果为True,则显示，如果为False，则不显示
show_web_page = True
# 是否记住账号密码，若为True,在第一次输入后会自动记住，下一次无需输入，若为False，则每次都需要输入账号密码
remember_password = True
# 你的浏览器驱动地址，目前只支持edge浏览器，请先根据以下操作查看浏览器版本
# 1.打开Edge浏览器。
# 2.点击右上角的三个点（更多操作）。
# 3.选择“帮助和反馈”。
# 4.点击“关于Microsoft Edge”。
# 5.浏览器会自动打开一个新的标签页，显示版本信息，如：版本 130.0.2849.46 (正式版本) (64 位)。
# 接下来请进入网站https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver，下载对应版本浏览器驱动（一个msedgedriver.exe文件），并将下面的地址换成你的exe文件的地址

if hasattr(sys,'_MEIPASS'):
    working_path = os.getcwd()
else:
    working_path = os.path.dirname(__file__)
DRIVER_PATH = os.path.join(working_path,'driver','msedgedriver.exe')





# 下面的熟悉Python的可以看
SERVICE_NAME = 'MyApp'
URL = r'https://whut.ai-augmented.com/app/jx-web/mycourse'


class MyScript():
    def __init__(self):
        self.mp4 = 0
        self.pptx = 0
        driver = self.get_driver()
        if driver:
            wait = WebDriverWait(driver, 10)
            try:
                print(f'正在登录中……')
                self.login(driver=driver,wait=wait)
                self.do_courses(driver=driver,wait=wait)
            except Exception as e:
                print(f'{e}')
                print(f'出现错误')
                print('\n\n')
                os.system('pause')
        print(f'共观看了{self.mp4}个视频')
        print(f'共观看了{self.pptx}个ppt')

    
    def get_driver(self) -> DriverType:
        options = webdriver.EdgeOptions()
        # 忽略证书警告
        options.add_argument('--ignore-certificate-errors')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # 不显示网站页面（后台静默运行）
        if not show_web_page:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        # 网站静音
        options.add_argument("--mute-audio")
        service = Service(executable_path=DRIVER_PATH)

        # 检查driver文件夹是否存在
        if not os.path.exists(os.path.dirname(DRIVER_PATH)):
            os.makedirs(os.path.dirname(DRIVER_PATH))
        # 添加说明文件
        with open(os.path.join(os.path.dirname(DRIVER_PATH),'说明.txt'),mode='w',encoding='utf-8') as f:
            f.write(f'此文件夹存放的是小雅自动观看脚本的driver程序，可以删除，但删除后下一次程序会花时间再次自动下载')
        
        try:
            # 检查是否存在基础的driver文件,没有则随便下载一个
            if not os.path.exists(DRIVER_PATH):
                save_path = self.download_driver_zip('130.0.2849.56')
                self.unzip_file(zip_path=save_path)
            driver = webdriver.Edge(service=service,options=options)
            return driver
        except WebDriverException as e:
            version = e.msg.split()[-7]
            save_path = self.download_driver_zip(version)
            self.unzip_file(zip_path=save_path)

            try:
                driver = webdriver.Edge(service=service,options=options)
                return driver
            except:
                return None


    def download_driver_zip(self,version:str) -> str:
        '''
        下载特定版本的driver，返回保存的路径
        '''
        driver_url = f'https://msedgedriver.azureedge.net/{version}/edgedriver_win64.zip'
        save_path = os.path.join(os.path.dirname(DRIVER_PATH),'download_driver.zip')

        try:
            response = requests.get(url=driver_url,stream=True)
            with open(file=save_path,mode='wb') as f:
                for chunk in tqdm(response.iter_content(chunk_size=1024),desc="下载driver中……"):
                    if chunk:
                        f.write(chunk)
            print(f'driver下载成功！')
            return save_path
        except:
            print(f'driver下载失败！')
            return ''


    def unzip_file(self,zip_path:str) -> bool:
        '''
        解压文件，返回状态值
        '''
        print(f'解压driver中……')
        if not os.path.exists(zip_path):
            print(f'解压失败！')
            return False
        
        try:
            with zipfile.ZipFile(zip_path,'r') as zip_ref:
                zip_ref.extract(member='msedgedriver.exe',path=os.path.dirname(zip_path))
            print(f'解压成功！')
            os.remove(zip_path)
            return True
        except:
            print(f'解压失败！')
            return False


    @staticmethod
    def save_credentials(username, password):
        keyring.set_password(SERVICE_NAME, 'username', username)
        keyring.set_password(SERVICE_NAME, username, password)

    @staticmethod
    def get_saved_username():
        return keyring.get_password(SERVICE_NAME, 'username')

    @staticmethod
    def get_saved_password(username):
        return keyring.get_password(SERVICE_NAME, username)

    def delete_saved_credentials(self):
        saved_username = self.get_saved_username()
        if saved_username:
            keyring.delete_password(SERVICE_NAME, saved_username)
        keyring.delete_password(SERVICE_NAME, 'username')
        
        

    def login(self,driver:DriverType,wait:WaitType) -> None:
        driver.get(url=URL)

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


        if remember_password:
            username = MyScript.get_saved_username()
            password = MyScript.get_saved_password(username)
            if not (username and password):
                username = input('请输入用户名：')
                password = input('请输入密码：')
                self.delete_saved_credentials()
                MyScript.save_credentials(username=username,password=password)
        else:
            username = input('请输入用户名：')
            password = input('请输入密码：')
            self.delete_saved_credentials()
            MyScript.save_credentials(username=username,password=password)

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
        if not driver.find_elements(by=By.CSS_SELECTOR,value='noscript'):
            button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,'button.ant-btn-default >span'))
            )
            button.click()


    def do_courses(self,driver:DriverType,wait:WaitType) -> dict:
        '''
        进入所有课程，并完成自主观看任务
        '''
        page_num = 0
        course_num = 0


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
            # 完成该课程中的全部任务
            self.do_tasks(driver=driver,wait=wait)
            # 回到主界面
            driver.get(url=URL)

            course_num+=1
            # 当前课程指向超过本页课程数量，则跳出循环
            if course_num==8:
                course_num = 0
                page_num+=1

            if page_num>=len(pages) or course_num>=len(courses):
                break  

    def do_tasks(self,driver:DriverType,wait:WaitType) -> None:
        '''
        完成课程界面的所有任务
        要求已经进入课程页面
        完成后不会返回主界面
        '''

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


    def watch_video(self,driver:DriverType,wait:WaitType,video_name='') -> None:
        '''
        要求当前已经切换到video页面中,完成任务后不会关闭页面
        '''
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


    def watch_pptx(self,driver=DriverType,wait=WaitType,task_name:str='') -> None:
        '''
        要求当前已经切换到pptx页面中,完成任务后不会关闭页面
        '''

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
    task1 = MyScript()
