#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2022/03/14 11:50:44
@File    :   executeCmdWidget.py
@Software:   VSCode
@Author  :   PPPPAN 
@Version :   1.0
@Contact :   for_freedom_x64@live.com
'''

import sys, os
from PyQt6.QtWidgets import QApplication, QWidget, QProgressBar, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import QThread, QMutex, pyqtSignal

class Thread(QThread):

    sinOutCmdNum = pyqtSignal(int)
    sinOutFinished = pyqtSignal(bool)

    def __init__(self, cmdList=''):
        super().__init__()
        self.commandList = cmdList
        self.qmut = QMutex() # 创建线程锁
    
    def run(self):
        self.qmut.lock()
        for i in range(len(self.commandList)):
            os.system(self.commandList[i])
            self.sinOutCmdNum.emit(i)
        self.sinOutFinished.emit(True)   
        self.qmut.unlock()     

class ExecuteCmdWidget(QWidget):
    def __init__(self, cmdList=''):
        super().__init__()
        self.commandList = cmdList
        self.initUI()
        self.setconnect()

    def initUI(self):
        self.setFixedSize(700,140)
        self.infoLabel = QLabel('是否开始执行命令')
        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0,len(self.commandList))
        self.progressBar.setFormat('%p')
        self.progressBar.setFixedSize(600,20)
        self.percentLabel = QLabel('0%')
        self.beginBtn = QPushButton('开始')
        self.quitBtn = QPushButton('退出')
        self.beginBtn.setFixedWidth(180)
        self.quitBtn.setFixedWidth(180)
        progressLayout = QHBoxLayout()
        progressLayout.addWidget(self.progressBar)
        progressLayout.addWidget(self.percentLabel)
        btnLayout = QHBoxLayout()
        btnLayout.addWidget(self.beginBtn)
        btnLayout.addWidget(self.quitBtn)

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.infoLabel)
        mainLayout.addLayout(progressLayout)
        mainLayout.addLayout(btnLayout)
        self.setLayout(mainLayout)

    def setconnect(self):
        self.quitBtn.clicked.connect(self.slotQuit)
        self.beginBtn.clicked.connect(self.slotExecuteCmd)

    def slotExecuteCmd(self):
        self.beginBtn.setEnabled(False)
        self.threading = Thread(self.commandList)
        self.threading.sinOutCmdNum.connect(self.slotChangeState)
        self.threading.sinOutFinished.connect(self.slotFinishedCmd)
        self.threading.start()

    def slotQuit(self):
        sys.exit()
    
    def slotChangeState(self, i):
        self.progressBar.setValue(i+1)
        percent = '{:.1f}'.format((i + 1)/len(self.commandList) * 100)
        self.percentLabel.setText(percent)
        self.infoLabel.setText('执行：' + self.commandList[i])

    def slotFinishedCmd(self, flag):
        if flag == True:
            self.infoLabel.setText('已完成所有文件分拣')
        else:
            self.infoLabel.setText('在哪里出了问题')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    testList = []
    for i in range(1,101):
        testList.append('echo ' + str(i))
    exe = ExecuteCmdWidget(testList)
    exe.show()
    sys.exit(app.exec())
