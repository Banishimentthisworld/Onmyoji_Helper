from PyQt5 import QtWidgets
import cv2
import numpy as np
from PyQt5.QtGui import *
import configparser
import os
import Onmyoji_Interface
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import win32gui, win32ui, win32con, win32api
import pyautogui
import win32con
import numpy
from PyQt5 import QtCore, QtGui, QtWidgets
from ctypes import windll
import time
from PIL import ImageFont, ImageDraw, Image

from Onmyoji_Interface import Ui_MainWindow
class Runthread(QThread):
    _signal = pyqtSignal(numpy.ndarray,int,int)

    def __init__(self, parent=None):
        super(Runthread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        while 1:
            global para_Rate
            # 获取窗口信息
            titlename = "阴阳师-网易游戏"
            # 根据titlename信息查找窗口
            hwnd = win32gui.FindWindow(0, titlename)
            # 获取左上和右下的坐标
            left, top, right, bottom = win32gui.GetClientRect(hwnd)
            # 截图图片的宽
            w = int((right - left))
            # 截图图片的高
            h = int((bottom - top))

            screen = QApplication.primaryScreen()
            img_pyqtt = screen.grabWindow(hwnd).toImage()
            ptr = img_pyqtt.constBits()
            ptr.setsize(img_pyqtt.byteCount())

            img_Oimyoji = np.array(ptr).reshape(img_pyqtt.height(), img_pyqtt.width(), 4)  # 注意这地方通道数一定要填4，否则出错

            time.sleep(1/para_Rate)
            self._signal.emit(img_Oimyoji, h, w)
                # if h != 0 and w != 0:
                #     stratPoint = win32gui.ClientToScreen(hwnd, (0, 0))
                #     # 置顶窗口
                #     # win32gui.EnableWindow(hwnd, True)
                #     # win32gui.SetForegroundWindow(hwnd)
                #     # time.sleep(0.01)
                #     # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）， 0号表示当前活跃窗口
                #     hwndDC = win32gui.GetWindowDC(0)
                #     # 根据窗口的DC获取mfcDC
                #     mfcDC = win32ui.CreateDCFromHandle(hwndDC)
                #     print(mfcDC)
                #     # mfcDC创建可兼容的DC
                #     saveDC = mfcDC.CreateCompatibleDC()
                #
                #     # 创建bigmap准备保存图片
                #     saveBitMap = win32ui.CreateBitmap()
                #     # 为bitmap开辟空间
                #     saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
                #
                #     # 高度saveDC，将截图保存到saveBitmap中
                #     saveDC.SelectObject(saveBitMap)
                #
                #     # 截取长宽为（w，h）的图片
                #     saveDC.BitBlt((0, 0), (w, h), mfcDC, stratPoint, win32con.SRCCOPY)
                #     # result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
                #     # 释放内存
                #     mfcDC.DeleteDC()
                #
                #     # 获取位图信息
                #     signedIntsArray = saveBitMap.GetBitmapBits(True)
                #
                #     img_Oimyoji = numpy.frombuffer(signedIntsArray, dtype='uint8')
                #     img_Oimyoji.shape = (h, w, 4)
                #
                #     self._signal.emit(img_Oimyoji, h, w)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # 设置窗体无边框
        self.setWindowFlags(Qt.FramelessWindowHint)

        # 全局变量
        global para_Rate,para_Resize,fontPath
        para_Rate = 30
        para_Resize = 100
        fontPath = "blod.ttf"

        # 控件初始化
        self.lab_Img.setStyleSheet("background-color:black")
        self.sil_Resize.setValue(100)
        self.sil_Rate.setValue(30)
        self.txt_Result.insertPlainText("-----自动书记人偶·阴阳师-----\n")

        # 退出按钮信号槽
        self.bn_Exit.triggered.connect(self.close)
        self.bn_Out.clicked.connect(self.close)
        # 开始按钮信号槽
        self.bn_Start.clicked.connect(self.Start)

    # 重写鼠标移动事件
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def Start0(self):

        # hwnd_title = dict()
        # def get_all_hwnd(hwnd, mouse):
        #     if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        #         hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
        #
        # win32gui.EnumWindows(get_all_hwnd, 0)
        #
        # # hd为存放句柄的数组，hh为计数符号
        # hd = [0]
        # hh = 0
        # # 筛选出所有阴阳师窗口，将其打印出来，并存放到数组中
        # for h, t in hwnd_title.items():
        #     if t == '阴阳师-网易游戏':
        #         hd.append(h)
        #         hh += 1
        #         print(hd[hh])

        # 获取窗口信息
        titlename = "阴阳师-网易游戏"
        # 根据titlename信息查找窗口
        hwnd = win32gui.FindWindow(0, titlename)
        # 置顶窗口
        win32gui.EnableWindow(hwnd, True)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.01)
        # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）， 0号表示当前活跃窗口
        hwndDC = win32gui.GetWindowDC(0)
        # 根据窗口的DC获取mfcDC
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        # mfcDC创建可兼容的DC
        saveDC = mfcDC.CreateCompatibleDC()
        # 创建bigmap准备保存图片
        saveBitMap = win32ui.CreateBitmap()

        # 获取左上和右下的坐标
        left, top, right, bottom = win32gui.GetClientRect(hwnd)
        stratPoint = win32gui.ClientToScreen(hwnd, (0, 0))

        # 截图图片的宽
        w = int((right - left))
        # 截图图片的高
        h = int((bottom - top))

        # 为bitmap开辟空间
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        # 高度saveDC，将截图保存到saveBitmap中
        saveDC.SelectObject(saveBitMap)

        # 截取长宽为（w，h）的图片
        saveDC.BitBlt((0, 0), (w, h), mfcDC, stratPoint, win32con.SRCCOPY)
        result = windll.user32.PrintWindow(hwnd,saveDC.GetSafeHdc(),0)

        # 获取位图信息
        signedIntsArray = saveBitMap.GetBitmapBits(True)
        img_Oimyoji = numpy.frombuffer(signedIntsArray, dtype='uint8')
        img_Oimyoji.shape = (h, w, 4)

        # 缩放
        if self.ckb_Resize.isChecked() == 1:
            img_Oimyoji = cv2.resize(img_Oimyoji,(int(w * self.sil_Resize.value()/100),int(h * self.sil_Resize.value()/100)))

        # 释放内存
        mfcDC.DeleteDC()

        # 将图片转换成Label显示对象
        img_test = cv2.cvtColor(img_Oimyoji, cv2.COLOR_BGR2RGB)
        QtImg = QtGui.QImage( img_test.data,
                              img_test.shape[1],
                              img_test.shape[0],
                              img_test.shape[1] * 3,
                              QtGui.QImage.Format_RGB888)
        self.lab_Img.setPixmap(QtGui.QPixmap.fromImage(QtImg))

    def Start(self):
        self.thread = Runthread()
        self.thread._signal.connect(self.callback)
        self.thread.start()  # 启动线程

    def callback(self,img_Oimyoji,h,w):
        global para_Rate,para_Resize,fontPath

        if h != 0 and w != 0:

            # 缩放
            if self.ckb_Resize.isChecked() == 1:
                para_Resize = self.sil_Resize.value()
                img_Oimyoji = cv2.resize(img_Oimyoji,
                                         (int(w *  para_Resize / 100), int(h *  para_Resize / 100)))
            else:
                para_Resize = 100

            # 采集帧率
            if self.ckb_Rate.isChecked() == 1:
                para_Rate = int(self.sil_Rate.value())
            else:
                para_Rate = 30

            # 输出控制信息
            # 流程状态输出
            font = ImageFont.truetype(fontPath,25)
            img_Pil = Image.fromarray(img_Oimyoji)
            draw = ImageDraw.Draw(img_Pil)
            fontText_Mod = "模式: 魂十"
            draw.text((10, int(h *  para_Resize / 100) - 50), fontText_Mod, font=font, fill=(0, 255, 0))

            # 采集参数输出
            txtOutpput_FPS = "FPS: " + str(para_Rate)
            txtOutpput_Resize = "缩放尺寸: (" + str(w * para_Resize/100) + " x " + str(h * para_Resize/100) + " )"
            draw.text((10, 20), txtOutpput_FPS, font=font, fill=(0, 255, 0))
            draw.text((10, 50), txtOutpput_Resize, font=font, fill=(0, 255, 0))
            # font = cv2.FONT_HERSHEY_SIMPLEX
            # cv2.putText(img_Oimyoji, txtOutpput_FPS, (10, 20), font, 0.7, (0, 255, 0), 2)
            # cv2.putText(img_Oimyoji, txtOutpput_Resize, (10, 50), font, 0.7, (0, 255, 0), 2)

            # PIL转换
            img_Oimyoji = np.array(img_Pil)

            # 将图片转换成Label显示对象
            img_test = cv2.cvtColor(img_Oimyoji, cv2.COLOR_BGR2RGB)
            QtImg = QtGui.QImage(img_test.data,
                                 img_test.shape[1],
                                 img_test.shape[0],
                                 img_test.shape[1] * 3,
                                 QtGui.QImage.Format_RGB888)
            self.lab_Img.setPixmap(QtGui.QPixmap.fromImage(QtImg))

        # 输出控制信息
        # self.txt_Result.insertHtml(
        #     '<html><head/><body><p><span style=" color:WhiteSmoke;">&nbsp;&nbsp;' + rec__txt + '</span></p></body></html>')
        # self.txt_Result.insertPlainText("\n")
        # self.txt_Result.moveCursor(self.txt_Result.textCursor().End)  # 文本框显示到底部



