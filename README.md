# <center>xiaoya-video-watcher</center>
# <div align=right><font size=4 face="仿宋">小雅视频观看助手</font></div>


## 1.功能介绍：
- 由于近期武汉理工大学的小雅进行了更新，在进行自主观看任务时,如果打开新的页面，之前的视频就会暂停，导致曾经的多开操作无法进行，极大地拖慢了🍐兵们刷水课任务的进度，所以我打算写一个脚本，来进行自动观看


## 2.注意事项：
- 目前程序还不是很完善，只是自己做来用的，后面会逐渐更新,萌新自己乱写的代码，也十分欢迎大佬pr，有问题也可以提出issue
- *待更新内容*：
  - [ ] GUI界面
  - [ ] 自动检测浏览器环境并下载驱动
  - [ ] 打包成exe文件发布release
  - [ ] 尝试利用小雅平台反复点击会跳进度的bug，来快速完成观看
  - [ ] 尝试使用窗口多开，同时观看多个视频
  - [ ] 完善ppt和mp3等多种形式自主观看任务的支持
  - [ ] 支持除了edge之外的浏览器


## 3.使用方法：<div align=left><font size=2>目前其实就一个脚本，熟悉python的直接复制运行就行了</font></div>


- 1. 第一步，克隆本仓库
  ```bash
  git clone https://github.com/Munbo123/xiaoya-video-watcher.git
  ```


- 2. 第二步，切换到本地仓库
  ```bash
  cd ./xiaoya-video-watcher
  ```


- 3. 第三步，安装虚拟环境并激活(我使用的是python3.12.6)
  ```bash
  python -m venv .venv
  ./.venv/Script/activate
  ```


- 4. 第四步，安装依赖库
  ```bash
  pip install -r ./requirements.txt
  ```


- 5. 第五步，查看浏览器版本（目前只支持edge浏览器）：
  - 1. 打开Edge浏览器。
  - 2. 点击右上角的三个点（更多操作）。
  - 3. 选择“帮助和反馈”。
  - 4. 点击“关于Microsoft Edge”。
  - 5. 浏览器会自动打开一个新的标签页，显示版本信息，如：版本 130.0.2849.46 (正式版本) (64 位)。
    ![图片加载失败](./pictures/浏览器版本.png "浏览器版本")


- 6. 第六步，下载对应的浏览器驱动，要求和浏览器版本号对应，建议直接把浏览器更新到最新版，这样对应的驱动直接就在第一页了（以后可能会做自动下载的功能）
    - [edge浏览器驱动下载地址] : https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver

- 7. 第七步，复制下载好的驱动的路径，打开`小雅PPT&video自动观看.py`文件,将其写入`DRIVER_PATH`变量
  
  
- 8. 第八步，运行程序
  ```bash
  python '.\小雅PPT&video自动观看.py'
  ```


## 4. 可选设置
- 1. 程序中的`show_web_page`变量，设置为True，则在运行时会显示web界面，方便看当前的进度以及在什么地方出现了错误。设置为False，则不会显示web界面，仅命令行输出
- 2. 程序中的`remember_password`变量，设置为True，则会记住密码，第一次仍需要输入，但后面再使用就不需要输入密码了。设置为False，则在每次运行时会要求输入账号密码，***注意，这里的账号密码是指智慧理工大的账号密码***，该程序不会以任何方式盗取你的密码，不信可以让懂Python的同学看一下代码。





