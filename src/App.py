import os
import sys
from typing import *
import threading

import keyring

import tkinter as tk
from tkinter import scrolledtext

from src.User import User
from src.Xiaoya_Script import Xiaoya_scrpit



class App:
    def __init__(self,working_path:str,service_name:str): 
        self.current_user:User = None
        self.working_path = working_path
        self.service_name = service_name
        self.login_page()


    def login_page(self):
        def enter():
            is_remember = var_remember.get()
            username = entry_username.get()
            password = entry_password.get()
            not_show = var_not_show.get()
            if is_remember:  # 需要记住密码
                keyring.set_password(self.service_name, 'username', username)
                keyring.set_password(self.service_name, username, password)
            else:  # 不需要记住密码，则应该清空存储的密码
                temp1 = keyring.get_password(self.service_name, 'username')
                if temp1:
                    keyring.delete_password(self.service_name, temp1)
                    keyring.delete_password(self.service_name, 'username')

            if not_show:  # 不显示界面
                keyring.set_password(self.service_name, 'show', 'yes')
            else:  # 要显示界面
                keyring.set_password(self.service_name, 'show', 'no')

            self.current_user = User(username, password, not_show)
            self.main_page()

        self.login_window = tk.Tk()
        self.login_window.title("登录界面")
        self.login_window.geometry('600x400')

        # 设置字体样式
        font = ("Arial", 12)

        # 创建用户名标签和输入框
        label_username = tk.Label(self.login_window, text="用户名:", font=font)
        entry_username = tk.Entry(self.login_window, font=font, width=30)

        # 创建密码标签和输入框
        label_password = tk.Label(self.login_window, text="密码:", font=font)
        entry_password = tk.Entry(self.login_window, font=font, show="*", width=30)

        # 创建一个单独的 Frame，用于对复选框进行 grid 布局
        frame1 = tk.Frame(self.login_window)

        # 创建记住密码复选框
        var_remember = tk.BooleanVar()
        check_remember = tk.Checkbutton(frame1, text="记住密码", variable=var_remember, font=font)
        if keyring.get_password(service_name=self.service_name, username='username') is None:
            var_remember.set(False)
        else:
            var_remember.set(True)
            username = keyring.get_password(self.service_name, 'username')
            password = keyring.get_password(self.service_name, username)
            entry_username.insert(0, username)
            entry_password.insert(0, password)

        # 创建是否显示web界面复选框
        var_not_show = tk.BooleanVar()
        check_not_show = tk.Checkbutton(frame1, text="不显示web界面", variable=var_not_show, font=font)
        if keyring.get_password(service_name=self.service_name, username='show') is None:
            var_not_show.set(False)
        else:
            if keyring.get_password(service_name=self.service_name, username='show') == 'yes':
                var_not_show.set(True)
            else:
                var_not_show.set(False)

        # 创建登录按钮
        button_login = tk.Button(self.login_window, text="登录", command=enter, font=font, width=2)

        # 使用 grid 布局管理控件，设置控件居中
        self.login_window.grid_rowconfigure(0, weight=1)
        self.login_window.grid_rowconfigure(1, weight=1)
        self.login_window.grid_rowconfigure(2, weight=1)
        self.login_window.grid_rowconfigure(3, weight=1)

        self.login_window.grid_columnconfigure(0, weight=1)
        self.login_window.grid_columnconfigure(1, weight=1)

        # 使用 grid 布局来居中控件
        label_username.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        entry_username.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        label_password.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        entry_password.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        frame1.grid(row=2, column=0, columnspan=2, pady=10)

        check_remember.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        check_not_show.grid(row=0, column=1, padx=20, pady=10, sticky="w")

        # 登录按钮的列跨度设为 1，避免横跨整个窗口，保持按钮适中的宽度
        button_login.grid(row=3, column=0, columnspan=2, pady=20, sticky="nsew")

        self.login_window.mainloop()


    def main_page(self):
        # 创建主窗口
        self.main_window = tk.Tk()
        self.main_window.title("主页面")
        self.main_window.geometry('600x400')


        # 创建一个滚动文本框用于显示程序的运行情况
        self.output = scrolledtext.ScrolledText(self.main_window, width=60, height=15)
        self.output.pack(pady=20)
  
        
        self.xiaoya = Xiaoya_scrpit(working_path=self.working_path,output=self.output)
        # 登录,开新的线程，防止阻塞主界面的形成
        threading.Thread(target=self.xiaoya.login, args=(self.current_user.username,self.current_user.password,self.current_user.show_page)).start()
        

        # 创建一个标签提示用户
        self.label_instruction = tk.Label(self.main_window, text="请选择要完成的指令")
        self.label_instruction.pack(pady=20)

        # 创建列出所有待完成的任务按钮
        self.button_list_tasks = tk.Button(self.main_window, text="1.列出所有待完成的任务", command=self.list_tasks)
        self.button_list_tasks.pack(pady=10)

        # 创建完成所有自主观看任务按钮
        self.button_complete_tasks = tk.Button(self.main_window, text="2.完成所有自主观看任务", command=self.complete_tasks)
        self.button_complete_tasks.pack(pady=10)

        # 销毁登录界面
        self.login_window.destroy()
        # 运行主循环
        self.main_window.mainloop()


    def list_tasks(self):
        threading.Thread(target=self.xiaoya.ApplyTask, args=(1,)).start()


    def complete_tasks(self):
        threading.Thread(target=self.xiaoya.ApplyTask, args=(2,)).start()


if __name__ == '__main__':
    app = App()

