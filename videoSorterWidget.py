#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2022/03/06 21:19:08
@File    :   videoSorter.py
@Software:   VSCode
@Author  :   PPPPAN 
@Version :   1.1
@Contact :   for_freedom_x64@live.com
'''

import sys, os
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QStackedLayout, QListWidget, QMessageBox, QFileDialog
from PyQt6.QtGui import QGuiApplication, QFont, QIcon, QImage,QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
from videoPlayerWidget import VideoPlayerWidget
from obtainPaths import ObtainPaths

class VideoSorterWidget(QWidget):
    #建立退出时发射的命令列表信号
    sinOutCommand = pyqtSignal(list)
    #初始化默认源目录为~/Downloads，默认目标目录为~/Movies
    def __init__(self, sourcePath = os.path.expanduser('~/Downloads'), targetPath = os.path.expanduser('~/Movies')):
        super().__init__()
        self.sourcePath = sourcePath
        self.targetPath = targetPath
        self.initUI()
        #os.system('/Applications/IINA.app/Contents/MacOS/IINA videos/1.mp4')
        self.setConnect()       #设置部件事件链接
        self.initMessageBox()   #初始化完成所有视频分选或退出程序时，发出的消息提示
        self.playFirstVideo()   #播放第一个视频

    def initUI(self):           #初始化部件
        # self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint)
        self.setWindowIcon(QIcon('static/ico.png'))
        self.videoDisplay = VideoPlayerWidget()                         #初始化播放器
        self.obtainPaths = ObtainPaths(self.sourcePath, self.targetPath)#初始化目录获取ObtainPaths
        #初始化各种组件
        self.title = QLabel('文件名')
        self.title.setFixedSize(960, 30)
        self.title.setObjectName('VideoTitle')
        self.dirTab = QPushButton('目标目录')
        self.dirTab.setObjectName('dirTab')
        self.cmdTab = QPushButton('已生成命令')
        self.cmdTab.setObjectName('cmdTab')
        self.dirList = QListWidget()
        self.dirList.setMinimumSize(200,480)
        self.setDirListItems(self.targetPath)   #给目标文件夹list赋初值
        self.cmdList = QListWidget()
        self.cmdList.addItems(['(空)'])
        self.cmdList.setMinimumSize(200,480)
        self.nextBtn = QPushButton('不知道，下一个')
        self.nextBtn.setFixedSize(200,30)
        self.nextBtn.setObjectName('nextBtn')
        self.cmdLabel = QLabel()
        self.cmdLabel.setFixedSize(960, 540)
        self.cmdLabel.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.cmdLabel.setObjectName('commandLabel')
        self.cmdLabel.move(0,100)
        
        videoLayout = QStackedLayout()
        videoLayout.addWidget(self.videoDisplay)
        videoLayout.addWidget(self.title)
        videoLayout.addWidget(self.cmdLabel)
        videoLayout.setStackingMode(QStackedLayout.StackingMode(1))
        
        tabLayout = QHBoxLayout()
        tabLayout.addWidget(self.dirTab)
        tabLayout.addWidget(self.cmdTab)

        self.infoLayout = QStackedLayout()
        self.infoLayout.addWidget(self.dirList)
        self.infoLayout.addWidget(self.cmdList)

        functionLayout = QVBoxLayout()
        functionLayout.addLayout(tabLayout)
        functionLayout.addLayout(self.infoLayout)
        functionLayout.addWidget(self.nextBtn)

        mainLayout = QHBoxLayout(self)
        mainLayout.addLayout(videoLayout)
        mainLayout.addLayout(functionLayout)
        mainLayout.setContentsMargins(0,0,0,0)
        mainLayout.setSpacing(0)

        self.setLayout(mainLayout)
        self.setWindowTitle('视频分拣小工具')
        self.setStyleSheet('#VideoTitle{color:white;background-color: rgba(20,20,20,50%);}#commandLabel{color:rgba(172,172,172,87%);margin-left:10;}#dirTab,#cmdTab{margin:0;padding:0;width:98;height:28;border-radius:20}#nextBtn{margin:0;padding:0;border-radius:20}')
        self.center()       # 窗口定位于屏幕中央显示

    #设置部件事件链接
    def setConnect(self):
        self.nextBtn.clicked.connect(self.slotNextVideo)
        self.dirList.itemClicked.connect(self.slotListClicked)
        self.dirTab.clicked.connect(self.slotSwitchInfoTab)
        self.cmdTab.clicked.connect(self.slotSwitchInfoTab)
    
    #初始化完成所有视频分选或退出程序时，发出的消息提示
    def initMessageBox(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Icon.Warning)
        self.msg.setWindowTitle('您将要退出')
        self.msg.setFont(QFont('"Heiti SC","PingFang SC","Hiragino Sans GB","STSong"')) #预设字体防卡死
        self.msg.setStandardButtons(QMessageBox.StandardButton.Close|QMessageBox.StandardButton.Cancel|QMessageBox.StandardButton.Save|QMessageBox.StandardButton.Yes)
        self.msg.setDefaultButton(QMessageBox.StandardButton.Yes)
        self.msg.setEscapeButton(QMessageBox.StandardButton.Cancel)
        self.msg.button(QMessageBox.StandardButton.Yes).setText('现在执行')
        self.msg.button(QMessageBox.StandardButton.Save).setText('保存至文件')
        self.msg.button(QMessageBox.StandardButton.Close).setText('仍然退出')
        self.msg.button(QMessageBox.StandardButton.Cancel).setText('取消')

    #添加功能函数
    def playVideo(self, path):
        self.videoDisplay.palyVideo(path)
        self.dirList.setEnabled(True)

    #根据path路径判断是否为末端目录，并操作：若为末级目录，则记录源文件和目标文件夹地址，保存命令；若非末级目录则在list中显示下级目录
    def setDirListItems(self, path):
        dirsList = self.obtainPaths.getDirs(path)
        if dirsList == -1:
            #若为末级目录，则记录源文件和目标文件夹地址，保存命令,返回-1
            self.dirList.setEnabled(False)
            self.dirList.clear()
            self.dirList.addItem('(空)')
            return -1
        else:
            #若非末级目录,则在list中显示下级目录,返回0
            self.dirList.clear()
            self.dirList.addItems(dirsList)
            return 0

    def setCmdListItems(self):      #填充命令列表
        cmdList = self.obtainPaths.getCmdList()
        self.cmdList.clear()
        self.cmdList.addItems(cmdList)

    def playFirstVideo(self):
        path = self.obtainPaths.getNextVideo()
        if path == -1:      #目录无视频文件
            self.videoDisplay.setText('当前目录无视频文件')
        else:               #排除目录无视频文件情况
            self.playVideo(path)
            self.title.setText('    ' + self.obtainPaths.getFilename(path))    

    def center(self):               # 窗口定位于屏幕中央显示
        screen = QGuiApplication.primaryScreen().geometry()
        self.move(int((screen.width() - 1160) / 2 + 50), int((screen.height() - 540) / 2 - 50))

    def executeCmd(self):           #逐一执行命令列表中的命令
        cmdList = self.obtainPaths.getCmdList()
        for item in cmdList:
            os.system(item)

    def closeEvent(self, event):    # 关闭窗口时弹出确认消息
        self.showMessageBox(event)

    def showMessageBox(self,event):
        if event == 0:
            #event为0表示已完成所有视频分拣工作
            self.msg.setText("\n已完成所有视频分拣工作。\n\n是否执行已生成归类命令，或将命令保存在文件中？")
            #已经完成所有分拣，故隐藏“取消”按钮
            self.msg.button(QMessageBox.StandardButton.Cancel).hide()
        else:
            #中途退出，传入事件event
            self.msg.setText("\n仍有视频未完成分拣，您将要退出。\n\n是否执行已生成归类命令，或将命令保存在文件中？")
        reply = self.msg.exec()                                 #显示MessageBox，并得到返回值
        if reply == QMessageBox.StandardButton.Cancel:          #点击取消按钮，返回主界面
            event.ignore()
        elif reply == QMessageBox.StandardButton.Close:         #点击仍然关闭按钮，退出程序
            sys.exit()
        elif reply == QMessageBox.StandardButton.Save:          #保存至文件
            flag = self.saveAsTxt(self.obtainPaths.getCmdList())    #得到保存文件的成功与否标志返回值
            if flag == 1:                                           #flag为1，所选保存的文件有误
                self.showMessageBox(event)                          #在此显示MessageBox
            elif flag == 0:                                         #成功保存至文件
                sys.exit()                                          #退出程序
            else:                                                   #保存文件返回值有误,退出程序
                QMessageBox.warning(self, "严重错误", "保存文件返回值有误", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
                sys.exit(-1)                                        #报错-1退出
        elif reply == QMessageBox.StandardButton.Yes:            #开始执行命令
            cmdList = self.obtainPaths.getCmdList()
            self.sinOutCommand.emit(cmdList)
            self.hide()
        else:
            sys.exit(-1)                                            #不太可能出现这个情况，出现了那就报错-1退出

    def saveAsTxt(self, cmdList):       # 保存为txt文件
        qFile = QFileDialog.getSaveFileName(self,'Open dir',self.sourcePath + '/VideoSorterCommand.txt')#跳出对话框选择命令保存文件
        if qFile == ('', ''):                   #若未选择保存的文件
            return 1                            #返回1表示，所选保存的文件有误
        if qFile[0].split('.')[-1]  != 'txt':   #判断文件格式
            QMessageBox.warning(self, "文件错误", "该文件非txt格式", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Ok)
            return 1                            #返回1表示，所选保存的文件有误
        else:                                   #若文件目录无误
            with open(qFile[0],'w',encoding='utf-8') as f:#使用with open()新建对象f
                for item in cmdList:
                    f.write(item + '\n')        #写入数据
                f.close()
            return 0                            #返回0表示，成功保存文件

    #添加各部件槽函数
    def slotNextVideo(self):            #点击“未知，下一个”按钮后，直接播放下一个视频
        path = self.obtainPaths.getNextVideo()  #获取下一个视频路径或错误代码
        if path != -1:
            #若能够正常获取视频路径，则停止当前视频，并变更正在播放的视频路径self.sourcePath,恢复至目标根目录并显示在list中,播放该视屏
            self.videoDisplay.stopVideo()
            self.sourcePath = path
            self.obtainPaths.pathRestore()
            self.setDirListItems(self.targetPath)
            self.playVideo(path)
            self.title.setText('    ' + self.obtainPaths.getFilename(path))
        else:
            #若错误代码为-1，则已到达末尾，无下一个视频文件，关闭按钮
            self.nextBtn.setEnabled(False)
            self.dirList.setEnabled(False)
            self.title.setText('    世界总有个尽头吧...')
            self.infoLayout.setCurrentIndex(1)
            self.videoDisplay.setText('<font style="font-size: 30px;">已无未整理视频</font>')
            self.showMessageBox(0)          #调用消息提示，执行分拣或保存命令，参数0表示已完成所有视频分拣工作
            # self.executeCmd()

    def slotListClicked(self, item):    #点击列表后保存路径并刷新列表
        # print('------ListClicked------')
        path = self.obtainPaths.pathAppend(item.text())
        flag = self.setDirListItems(path)   #执行setDirListItems在list中列出目录，并获取返回值flag
        if flag == -1:                      #若flag=-1，说明当前已为末级目录，则记录源文件和目标文件夹地址，保存命令,播放下一个视频
            shellCommand = self.obtainPaths.getShellCommand()   #保存单条命令
            self.cmdLabel.setText('已保存命令：%s ' % shellCommand)
            self.setCmdListItems()
            # self.videoDisplay.stopVideo()
            self.slotNextVideo()            #继续读取下一个视频

    def slotSwitchInfoTab(self):        #listStack切换infoLayout
        dic = { 'dirTab' : 0, 'cmdTab': 1}
        index = dic[self.sender().objectName()]
        self.infoLayout.setCurrentIndex(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    exe = VideoSorterWidget('/Users/panzk/Programming/Python/videoSorter.bak/videos','/Users/panzk/Programming/Python/videoSorter.bak/targetPath')
    exe.show()
    sys.exit(app.exec())