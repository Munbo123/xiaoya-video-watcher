import os
import zipfile

import requests
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.common.exceptions import WebDriverException



class MyDriver():
    def __init__(self,working_path,not_show_page=False):
        self.not_show_page = not_show_page
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
        if self.not_show_page:  # 不显示网站页面（后台静默运行）
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

