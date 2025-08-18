from subprocess import run
import sys
import os
from time import sleep as wait

class Main:
    def __init__(self):
        self.main()

    @staticmethod
    def next_page():
        for i in range(100):
            print()

    def main(self):
        self.next_page()

        print('欢迎使用系统cmd-path修复工具！')
        print('仅限Windows使用！')
        print('使用前请详细阅读README.html文件！')
        print('请使用管理员方式运行！')

        if os.name == 'nt':
            print('###############################################')
            print()
            print('Enter) 一键修复python的环境变量目录')
            print('q) 退出')
            print()
            print('###############################################')
            print()
            command=input('输入你的操作：')

            if command == '':
                self.one_click()

            else:
                quit(114514)

        else:
            print('你的电脑不支持！')

    def one_click(self):
        self.next_page()

        path=sys.executable
        user_path='C:/Users/%username%/AppData/Local/Programs/Python/ '
        command=run('setx -m path %path%;{}Scripts\;{};{}Launcher/;{}Python313/Scripts/;C:/Users/%username%/AppData/Roaming/Python/Python313/Scripts/'.format(path[:path.rfind('python.exe')],path[:path.rfind('python.exe')],user_path[:user_path.rfind(' ')],user_path[:user_path.rfind(' ')]),shell=True,text=True,capture_output=True)

        for i in range(5):
            print('正在修复目录：第 ' + str(i + 1) + ' 个，共 5 个')
            wait(0.1)

        if '成功: 指定的值已得到保存。'in command.stdout+command.stderr:
            print('修复成功！')
            wait(3)
            self.main()

        else:
            print('修复失败！')
            print(command.stdout+command.stderr)
            wait(3)
            self.main()

Main()