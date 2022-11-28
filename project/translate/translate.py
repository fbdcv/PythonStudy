import sys
import urllib.request
import urllib.parse
import json
import time

from PyQt5.Qt import *
from pynput import keyboard
from threading import Thread

class Translate(QWidget):

    def __init__(self):
        super().__init__()
        self.init_gui()


    def init_gui(self):
        # 字体
        font = QFont()
        font.setPointSize(20)
        font.setBold(5)
        font.setFamily("KaiTi_GB2312")
        self.setFont(font)
        # 搜索框
        self.text_input = QLineEdit("")
        self.text_input.setGeometry(0, 0, 450, 50)
        # 浏览框
        self.text_output = QTextBrowser()
        self.text_output.setGeometry(0, 40, 450, 200)
        self.text_output.setVisible(False)
        # 布局
        qlayout = QFormLayout()
        qlayout.addRow("", self.text_input)
        qlayout.addRow("", self.text_output)

        #self.setGeometry(650, 300,500, 250)
        self.setGeometry(650,300,500,50)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 去掉标题栏的代码
        self.setLayout(qlayout)
        self.show()

    def search(self):
        self.url = "https://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"

        self.head = {'Referer': 'https://fanyi.youdao.com/',
                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
                     }
        self.data = {}

        self.data['from'] = 'AUTO'
        self.data['to'] = 'AUTO'
        self.data['smartresult'] = 'dict'
        self.data['client'] = 'fanyideskweb'
        self.data['doctype'] = 'json'
        self.data['version'] = '2.1'
        self.data['keyfrom'] = 'fanyi.web'
        self.data['action'] = 'FY_BY_CLICKBUTTION'
        self.data['i'] = self.text_input.text()
        # 翻译
        data_tmp = urllib.parse.urlencode(self.data).encode('utf8')
        req = urllib.request.Request(self.url, data_tmp, self.head)
        response = urllib.request.urlopen(req)
        # 读取信息解码操作decode
        html = response.read().decode('utf8')
        # 使用json进行数据处理
        target = json.loads(html)
        # 清洗数据操作
        self.res = target['translateResult'][0][0]['tgt']
        self.text_output.moveCursor(self.text_output.textCursor().End)
        time.sleep(0.2)
        self.text_output.append(str(self.res))

ALT = False
ENTER = False
ESC = False
SPACE = False

def listen():  # 键盘监听函数
    def on_press(key):
        global ALT, ENTER, ESC, SPACE
        if key == keyboard.Key.alt or key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
            ALT = True
        # if key == keyboard.KeyCode(char='z') or key == keyboard.KeyCode(char='Z'):
        #     Z = True
        if key == keyboard.Key.space:
            SPACE = True
        if key == keyboard.Key.esc:
            ESC = True
        if key == keyboard.Key.enter:
            ENTER = True
        # print(ALT, Z, X, C)

        if ALT and SPACE:  # 检测到Alt和c同时按下时，启动/关闭录屏
            ALT = SPACE = False
            if translate.isMinimized():
                translate.showNormal()
            else:
                translate.showMinimized()


        if ESC:
            ESC = False
            if translate.text_output.isVisible():
                translate.text_output.setVisible(False)
                translate.setGeometry(650, 300, 500, 50)
                translate.setGeometry(650, 300, 500, 50)
                translate.text_input.clear()

        if ENTER:
            ENTER = False
            translate.setGeometry(650, 300, 500, 250)
            translate.text_output.setVisible(True)
            translate.search()


    def on_release(key):
        global ALT, ENTER, ESC, SPACE
        if key == keyboard.Key.alt or key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
            ALT = False
        # if key == keyboard.KeyCode(char='z') or key == keyboard.KeyCode(char='Z'):
        #     Z = False
        if key == keyboard.Key.space:
            SPACE = False
        if key == keyboard.Key.esc:
            ESC = False
        if key == keyboard.Key.enter:
            ENTER = False

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()



class ListenThread(Thread):  # 截屏监听线程，监听函数一定要放在后台线程里康康说明那个join了吗（￣︶￣）↗　

    def __init__(self):
        super().__init__()

    def run(self):
        listen()


if __name__ == "__main__":
    listenThread = ListenThread()  # 创建监听线程
    listenThread.start()
    # 每一PyQt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
    app = QApplication(sys.argv)
    # QWidget部件是PyQt5所有用户界面对象的基类。他为QWidget提供默认构造函数。默认构造函数没有父类。
    translate = Translate()
    # 系统exit()方法确保应用程序干净的退出
    sys.exit(app.exec_())
