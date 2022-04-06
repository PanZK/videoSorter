 #!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2022/03/10 00:53:34
@File    :   obtainPaths.py
@Software:   VSCode
@Author  :   PPPPAN 
@Version :   1.0
@Contact :   for_freedom_x64@live.com
'''

import os

#常见视频文件格式
VIDEPTYPE = ['mp4', 'MP4', 'avi', 'AVI', 'wmv', 'WMV','mkv', 'MKV', 'flv', 'FLV', 'mov', 'MOV', 'ts', 'TS', 'webm', 'WEBM']

class ObtainPaths():
    #初始化默认源目录为~/Downloads，默认目标目录为~/Movies
    def __init__(self, sourcePath = os.path.expanduser('~/Downloads'), targetPath = os.path.expanduser('~/Movies')):
        self.sourcePath = sourcePath
        self.targetPath = targetPath
        #self.pointer作为指针,指向当前播放视频是第几个
        self.pointer = 0
        #当前视频文件名
        self.fileName = ''
        #根据每次选择目录不同生成不同保存路径
        self.savePath = self.targetPath
        #建立命令列表
        self.commandList = []
        #获取源文件夹内文件列表
        self.videoList = os.listdir(self.sourcePath)

    #获取保存目标目录结构
    def getDirs(self, path):
        #获取目录下所有文件保存列表，保存至dirList
        dirList = os.listdir(path)
        exceptFilesDirList = []
        #清除列表中非目录内容，保存至exceptFilesDirList
        for i in range(len(dirList)):
            if os.path.isdir(path + '/' + dirList[i]):
                exceptFilesDirList.append(dirList[i])
        #若exceptFilesDirList为空，则说明已到达末端目录，返回-1进行表示；若非空则返回exceptFilesDirList列表
        if len(exceptFilesDirList) == 0:
            return -1
        else:
            return exceptFilesDirList
    
    def pathAppend(self, dir):              #根据每次选择目录不同，追加相应子目录
        self.savePath = self.savePath + '/' + dir
        # print('obt %s' % self.savePath)
        return self.savePath
    
    #一个视频完成后，将保存目录还原
    def pathRestore(self):
        self.savePath = self.targetPath
    
    #得到文件名
    def getFilename(self, path):
        (filepath, fileName) = os.path.split(path)
        self.fileName = fileName
        return fileName
    
    #返回保存路径
    def getSavePath(self):
        return self.savePath
    
    #返回命令列表
    def getCmdList(self):
        return self.commandList
    
    def getShellCommand(self):
        command = 'mv "%s/%s" "%s"' % (self.sourcePath, self.fileName, self.savePath)
        #将生成好的命令添加在命令列表中
        self.commandList.append(command)
        return command
    
    #获取下一个视频文件名
    def getNextVideo(self):
        #self.pointer作为指针，当指针未越界时：
        while self.pointer < len(self.videoList):
            #拿到当前序号，并将self.pointer+1
            i = self.pointer
            self.pointer += 1
            #检查文件名后缀是否为视频文件
            postfix = self.videoList[i].split('.')[-1]
            if (postfix in VIDEPTYPE) and (os.path.isfile(self.sourcePath + '/' + self.videoList[i])):
                #是文件且是视频格式，则返回该文件名
                return self.sourcePath + '/' + self.videoList[i]
        else:
            #到达末尾，结束，self.pointer归0，返回错误代码-1
            # print('到达末尾，结束')
            self.pointer = 0
            return -1

if __name__ == '__main__': 
    a = ObtainPaths(sourcePath = os.path.expanduser('~') + '/Scripts/Python/videoSorter.bak/videos', targetPath= os.path.expanduser('~') + '/Scripts/Python/videoSorter.bak/targetPath')
    print(a.getDirs('targetPath'))