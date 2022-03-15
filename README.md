<h1  align="center">Video Sorter</h1>

<p align="center">Video Sorter 是一个用Python3编写的视频分拣工具。</p>

---

## Origin

&emsp;&emsp;电脑中下载文件夹积累的各种视频过多，想整理到视频专用文件夹内，但又嫌逐一打开复制过去甚烦。遂在学习Python过程中做了Video Sorter当做实践。

## Features

- 视频显示部分使用[opencv-python](https://github.com/opencv/opencv-python)渲染
- 程序界面使用[PyQt6](https://pypi.org/project/PyQt6/)制作
- 分拣完成后会形成分拣终端命令列表，可选择立即执行或保存为 `txt`
- 运行程序直接选择视频堆积所在文件夹(如 `~/Downloads` )、视频归类整理文件夹(如 `~/Moives` )
- 使用过程中，程序会逐一展示文件夹中的各视频文件，同时在右侧列表处展示目标整理文件夹的结构，点击列表单元进入下级目录，若为末级目录则直接形成命令，并开始下一个视频操作
- 目前只支持源目录下视频读取遍历，不支持源目录的子目录视频读取遍历

## How to use

1. 下载[release](https://github.com/PanZK/videoSorter/releases)中的 `dmg` 文件，打开后将Video Sorter拉进 `Applications` 文件夹，即可在程序坞中找到；
2. 打开运行Video Sorter，开始会选择视频所在文件夹(比如选择 `~/Downloads` )、视频归类整理文件夹(比如选择 `~/Moives` )；
3. 选择好正确目录后，程序会自动播放获取到的视频，并在右侧列表处列出目标目录的各文件夹，点击右侧列表进行分类；
4. 列表进入末级目录后便可自动生成相应终端中的 `mv` 命令，点击右侧列表上方的tab标签可切换查看目录结构或已生成命令；
5. 待所有视频遍历结束，或中途退出程序时，可选择将已生成命令现在执行，或保存为 `txt` 文件以便后续使用。

---

<p align="center">
  Enjoy it!
</p>
