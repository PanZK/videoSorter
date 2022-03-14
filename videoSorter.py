#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2022/03/12 18:44:43
@File    :   videoSorter.py
@Software:   VSCode
@Author  :   PPPPAN 
@Version :   1.0
@Contact :   for_freedom_x64@live.com
'''

import sys        
from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtGui import QPixmap
from initialPathWidget import InitialPathWidget
from videoSorterWidget import VideoSorterWidget
from executeCmdWidget import ExecuteCmdWidget

class VideoSorter():
    def __init__(self):
        self.pathBox = InitialPathWidget()
        self.pathBox.sinOut.connect(self.slotCreateVideoSorter)
    
    def slotCreateVideoSorter(self, paths):
        self.mainProgram = VideoSorterWidget(paths[0], paths[1])
        self.mainProgram.sinOutCommand.connect(self.slotCreatExeWidget)
        self.mainProgram.show()

    def slotCreatExeWidget(self, cmdList):
        self.exeCommand = ExecuteCmdWidget(cmdList)
        self.exeCommand.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)                #启动界面
    splash = QSplashScreen(QPixmap(r"static/cover.png"))
    splash.show()                               #展示启动图片
    app.processEvents()                         #防止进程卡死
    exe = VideoSorter()                         #建立主题程序
    exe.pathBox.show()
    splash.finish(exe.pathBox)                  #关闭启动界面
    sys.exit(app.exec())

#pyinstaller --windowed --onefile --clean --noconfirm videoSorter.py --icon=static/icon.png