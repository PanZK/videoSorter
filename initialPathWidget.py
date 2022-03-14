#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2022/03/10 22:42:19
@File    :   initialPathWidget.py
@Software:   VSCode
@Author  :   PPPPAN 
@Version :   1.0
@Contact :   for_freedom_x64@live.com
'''

import sys
from os import path
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QFileDialog, QMessageBox, QFontDialog
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QGuiApplication

class InitialPathWidget(QWidget):

    sinOut = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.initUI()
        #设置部件事件链接
        self.setConnect()

    def initUI(self):
        self.setFixedSize(500,260)
        # font, isok = QFontDialog.getFont()
        # font = QFont('"PingFang SC","Hiragino Sans GB","STSong"')
        # font.setPointSize(30)
        # print(font.family())
        # self.setFont(font)

        self.info = QLabel('<font style="font-size: 18px;">请选择目录</font><br><br>请将&nbsp;&nbsp;杂七杂八电影或视频的文件夹选为&nbsp;&nbsp;源目录<br>请将&nbsp;&nbsp;干净卫生分类整理的文件夹选为&nbsp;&nbsp;目标目录')
        self.info.setWordWrap(True)
        self.info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sourceLineEdit = QLineEdit()
        self.sourceLineEdit.setPlaceholderText("视频所在源目录")
        self.sourceLineEdit.setObjectName("sourceFilePathlineEdit")
        self.sourceDirBtn = QPushButton("视频文件夹..")

        sourceLayout = QHBoxLayout()
        sourceLayout.setContentsMargins(0, 0, 0, 0)
        sourceLayout.setObjectName("horizontalLayout")
        sourceLayout.addWidget(self.sourceLineEdit)
        sourceLayout.addWidget(self.sourceDirBtn)

        self.targetLineEdit = QLineEdit()
        self.targetLineEdit.setObjectName("targetFilePathlineEdit")
        self.targetLineEdit.setPlaceholderText("整理目标目录")
        self.targetDirBtn = QPushButton("目标文件夹..")

        targetLayout = QHBoxLayout()
        targetLayout.setContentsMargins(0, 0, 0, 0)
        targetLayout.setObjectName("horizontalLayout")
        targetLayout.addWidget(self.targetLineEdit)
        targetLayout.addWidget(self.targetDirBtn)

        self.confirmBtn = QPushButton('确定')
        self.confirmBtn.setFixedSize(200,30)
        self.cancelBtn = QPushButton('取消')
        self.cancelBtn.setFixedSize(200,30)

        btnLayout = QHBoxLayout()
        btnLayout.addWidget(self.confirmBtn)
        btnLayout.addWidget(self.cancelBtn)

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.info)
        mainLayout.addLayout(sourceLayout)
        mainLayout.addLayout(targetLayout)
        mainLayout.addLayout(btnLayout)

        self.setLayout(mainLayout)
        self.setObjectName("widget")
        # 窗口定位于屏幕中央显示
        self.center()

        # self.setStyleSheet('*{font-family:"PingFang SC","Hiragino Sans GB","STSong";}')
        # self.filePathlineEdit = QLineEdit(self.widget)
        # self.filePathlineEdit.setObjectName("filePathlineEdit")
        # self.horizontalLayout.addWidget(self.filePathlineEdit)

    def setConnect(self):
        self.sourceDirBtn.clicked.connect(self.slotSourceDir)
        self.targetDirBtn.clicked.connect(self.slotTargetDir)
        self.cancelBtn.clicked.connect(sys.exit)
        self.confirmBtn.clicked.connect(self.slotConfirm)

    #设置视频目录按钮槽函数
    def slotSourceDir(self):
        videoDir = QFileDialog.getExistingDirectory(self,'Open dir',path.expanduser('~'), QFileDialog.Option.ShowDirsOnly)
        self.sourceLineEdit.setText(videoDir)

    #设置目标目录按钮槽函数
    def slotTargetDir(self):
        targetDir = QFileDialog.getExistingDirectory(self,'Open dir',path.expanduser('~'), QFileDialog.Option.ShowDirsOnly)
        self.targetLineEdit.setText(targetDir)

    #设置确认按钮槽函数，既判断内容是否非空，并提交给主程序
    def slotConfirm(self):
        #设置标志符为真
        self.sign = True
        #初始化消息提示
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle('内容错误')
        msg.setFont(QFont('"Heiti SC","PingFang SC","Hiragino Sans GB","STSong"'))
        #获得源目录和目标目录
        sourceDir = self.sourceLineEdit.text()
        targetDir = self.targetLineEdit.text()
        if sourceDir == '':
            #如果源目录空
            self.sign = False
            msg.setText("视频文件夹<font color='red'>不可为空</font>!!!")
            msg.setDetailedText("The details are as follows:\n必须赋予源视频文件的目录")
            msg.exec()
        elif not path.isdir(sourceDir):
            #如果源目录不是目录
            self.sign = False
            msg.setText("视频文件夹所选<font color='red'>为非目录</font>!!!")
            msg.setDetailedText("The details are as follows:\n必须赋予源视频文件的目录")
            msg.exec()
        elif not path.exists(sourceDir):
            #如果源目录不存在
            self.sign = False
            msg.setText("视频文件夹所选<font color='red'>不存在</font>!!!")
            msg.setDetailedText("The details are as follows:\n必须赋予源视频文件的目录")
            msg.exec()
        elif targetDir == '':
            #如果目标目录空
            self.sign = False
            msg.setText("目标文件夹<font color='red'>不可为空</font>!!!")
            msg.setDetailedText("The details are as follows:\n必须赋予目标文件夹")
            msg.exec()
        elif not path.isdir(targetDir):
            #如果目标目录不是目录
            self.sign = False
            msg.setText("目标文件夹所选<font color='red'>为非目录</font>!!!")
            msg.setDetailedText("The details are as follows:\n必须赋予目标文件夹")
            msg.exec()
        elif not path.exists(targetDir):
            #如果目标目录不存在
            self.sign = False
            msg.setText("目标文件夹所选<font color='red'>不存在</font>!!!")
            msg.setDetailedText("The details are as follows:\n必须赋予源视频文件的目录")
            msg.exec()

        #目录正常
        if self.sign:
            #发出信号，参数为源目录和目标目录的元组，并关闭当前窗口
            self.sinOut.emit((sourceDir,targetDir))
            # print((sourceDir, targetDir))
            self.close()
    
    # 窗口定位于屏幕中央显示
    def center(self):
        screen = QGuiApplication.primaryScreen().geometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2 - 100))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = InitialPathWidget()
    exe.show()
    sys.exit(app.exec())