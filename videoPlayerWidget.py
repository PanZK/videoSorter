#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2022/03/10 00:53:46
@File    :   videoPlayerWidget.py
@Software:   VSCode
@Author  :   PPPPAN 
@Version :   1.0
@Contact :   for_freedom_x64@live.com
'''

import cv2,sys
from PyQt6.QtWidgets import QApplication, QLabel
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QThread, QMutex, pyqtSignal, Qt

class Thread(QThread):
    sinOut = pyqtSignal(QImage)

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.cap = cv2.VideoCapture(path)
        self.playing = False
        self.qmut = QMutex() # 创建线程锁

    def __del__(self):
        #线程状态改变与线程终止
        if self.playing == True:
            cv2.destroyAllWindows()
        # ----------------print('线程挂起')
        self.playing = False
    
    def run(self):
        self.qmut.lock()
        self.playing = True
        #设置帧率
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        if fps == float('inf'):
            fps = 24
        
        if self.cap.isOpened():
            #防止空帧出现，设置i=10帧空余量
            i = 10
            # ---------------print('已打开视频%s' % self.path)
            #逐帧播放读取视频信息转化成QImage格式后通过playImage函数逐帧显示给viedeoDisplay
            while self.cap.isOpened() and (self.playing or i):
                if i > 0:
                    i -= 1
                self.playing, self.frame = self.cap.read()
                if self.playing:
                    #将每帧视频信息转化成QImage格式
                    qImg = self.convCvImgtoQImg(self.frame)
                    #将转化好的QImage对象作为参数发送信号，显示给viedeoDisplay
                    self.sinOut.emit(qImg)
                #根据帧率不同设置相应等待时间
                cv2.waitKey(int(1000/fps))
            cv2.destroyAllWindows()
            self.wait()
            self.playing = False
        else:
            # -------------------print('视频%s打开失败' % self.path)
            self.wait()
            self.playing = False
        self.qmut.unlock()
    
    #将视频信息数组转化成QImage格式
    def convCvImgtoQImg(self, cvImg):
        #将BGR转为RGB信息
        frame = cv2.cvtColor(cvImg, cv2.COLOR_BGR2RGB)
        #将numpy.array转化成QImage格式
        qImg = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format.Format_RGB888)
        return qImg

class VideoPlayerWidget(QLabel):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        #UI初始化，设置窗口大小、对齐方式、部件ID、背景颜色
        self.setMinimumSize(960,540)
        self.setText('<font style="font-size: 30px;">Video Display</font>')
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setObjectName('VideoPlayerWidget')
        self.setStyleSheet('#VideoPlayerWidget{color:white;background-color:black}')
        #self.playImage(QImage('1.png'))
    
    def playImage(self, frame):
        #将numpy数组格式转化为QPixmap
        fitPixmap = QPixmap.fromImage(frame)
        #Qt.AspectRatioMode.KeepAspectRatio按比例缩放
        fitPixmap = fitPixmap.scaled(960, 540, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.setPixmap(fitPixmap)

    def palyVideo(self, path):
        #开启线程进行视频渲染
        self.videoThreading = Thread(path)
        # -----------------print('建立线程')
        self.videoThreading.sinOut.connect(self.playImage)
        self.videoThreading.start()

    #结束正在渲染视频的线程
    def stopVideo(self):
        self.videoThreading.terminate()
        self.videoThreading.wait()
        cv2.destroyAllWindows()
        self.videoThreading.playing = False
        self.setText('Video Display')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = VideoPlayerWidget()
    w.show()
    # w.palyVideo('videos/1.mp4')
    w.palyVideo('/Users/panzk/Programming/Python/videoSorter/videos/1.mp4')
    sys.exit(app.exec())