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
from pymouse import PyMouse
import math
import random
from PIL import Image,ImageEnhance,ImageFilter

from Onmyoji_Interface import Ui_MainWindow
class Runthread(QThread):
    _signal = pyqtSignal(numpy.ndarray,int,int,int)

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
            self._signal.emit(img_Oimyoji, h, w,hwnd)
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
            # 将两个16位的值连接成一个32位的地址坐标




class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # 设置窗体无边框
        self.setWindowFlags(Qt.FramelessWindowHint)

        # 全局变量
        global para_Rate,para_Resize,fontPath,flag_H11,flag_H11_LC,H11_LC1,H11_LC0_Times,H11_LC0_Avg,H11_LC2_Compare ,H11_LC1_Times
        global  H11_LC1_Click
        flag_H11_LC = 1
        para_Rate = 30
        para_Resize = 100
        fontPath = "blod.ttf"
        flag_H11 = 0
        H11_LC1 = self.getImgHash(Image.open("H11_LC1.jpg"))
        H11_LC0_Times = 0
        H11_LC0_Avg = 0
        H11_LC2_Compare = 0
        H11_LC1_Click = 1
        H11_LC1_Times = 0

        # 控件初始化
        self.lab_Img.setStyleSheet("background-color:black")
        self.sil_Resize.setValue(100)
        self.sil_Rate.setValue(30)
        self.txt_Result.insertPlainText("-----自动书记人偶·阴阳师-----\n")
        self.cbx_KZMS.setCurrentIndex(1)
        self.cbx_FBLX.setCurrentIndex(1)

        # 退出按钮信号槽
        self.bn_Exit.triggered.connect(self.close)
        self.bn_Out.clicked.connect(self.close)
        # 开始按钮信号槽
        self.bn_Start.clicked.connect(self.Start)
        # 测试发送鼠标
        self.bn_SaveIni.clicked.connect(self.SendMouse)
        self.bn_LoadIni.clicked.connect(self.H11)

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

    def Start(self):
        # global flag_H11_LC, H11_LC0_Times,H11_LC1_Times
        # flag_H11_LC = 0
        # H11_LC0_Times = 0
        # H11_LC1_Times = 0
        self.thread = Runthread()
        self.thread._signal.connect(self.callback)
        self.thread.start()  # 启动线程

    def callback(self,img_Oimyoji,h,w,hwnd):
        global para_Rate,para_Resize,fontPath,flag_H11,H11_LC0_Avg,H11_LC2_Compare,H11_LC1_Click


        if h != 0 and w != 0:

            # 缩放
            if self.ckb_Resize.isChecked() == 1:
                para_Resize = self.sil_Resize.value()
                img_Oimyoji = cv2.resize(img_Oimyoji,
                                         (int(w *  para_Resize / 100), int(h *  para_Resize / 100)))
            else:
                para_Resize = 100

            # 图像缩放后尺寸
            img_img_Oimyoji_w = int(w * para_Resize / 100)
            img_img_Oimyoji_h = int(h * para_Resize / 100)

            img_Oimyoji_Origin = img_Oimyoji.copy()

            # 采集帧率
            if self.ckb_Rate.isChecked() == 1:
                para_Rate = int(self.sil_Rate.value())
            else:
                para_Rate = 30

            cv2.rectangle(img_Oimyoji,(int(img_img_Oimyoji_w * 0.39),int(img_img_Oimyoji_h * 0.18)), (int(img_img_Oimyoji_w * 0.95),int(img_img_Oimyoji_h * 0.87)), (0,255,0), 1)

            # region 图像处理
            # 魂十一
            if self.cbx_FBLX.currentIndex() == 1:
                global flag_H11_LC ,H11_Pos_x,H11_Pos_y,H11_R,H11_LC1,H11_LC0_Times,H11_LC1_Times
                H11_Pos_x = 0
                H11_Pos_y= 0

                img_H11 = img_Oimyoji.copy()
                img_H11_B = img_H11[:, :, 0]
                img_H11_ROI0 = img_H11_B.copy()
                img_H11_ROI0.fill(255)
                cv2.rectangle(img_H11_ROI0, (int(img_img_Oimyoji_w * 0.39), int(img_img_Oimyoji_h * 0.18)),
                              (int(img_img_Oimyoji_w * 0.95), int(img_img_Oimyoji_h * 0.87)), (0, 0, 0), -1)
                img_H11_Result = cv2.subtract(img_H11_B, img_H11_ROI0)

                ret, img_H11_Result = cv2.threshold(img_H11_Result, 180, 255, cv2.THRESH_BINARY)
                H11_LC0_Avg = round((np.sum(img_H11_Result) / (len(img_H11_Result) * len(img_H11_Result[0]))), 3)

                # 检测按钮
                if flag_H11_LC == 0 :
                    img_H11_Bnget = img_Oimyoji_Origin.copy()
                    img_H11_R = img_H11_Bnget[:, :, 2]
                    img_H11_ROI1 = img_H11_R.copy()
                    img_H11_ROI1.fill(255)
                    cv2.rectangle(img_H11_ROI1, (int(img_img_Oimyoji_w * 0.72), int(img_img_Oimyoji_h * 0.78)),
                                  (int(img_img_Oimyoji_w), int(img_img_Oimyoji_h)), (0, 0, 0), -1)
                    img_H11_Result2 = cv2.subtract(img_H11_R, img_H11_ROI1)
                    ret, img_H11_Result2 = cv2.threshold(img_H11_Result2, 180, 255, cv2.THRESH_BINARY)
                    binary, contours, hierarchy = cv2.findContours(img_H11_Result2, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
                    for i in range(len(contours)):
                        convexHull = cv2.convexHull(contours[i])
                        arcLength = cv2.arcLength(convexHull, True)
                        if arcLength > (img_img_Oimyoji_w  * 0.07*3.14) and arcLength < (img_img_Oimyoji_w  * 0.12*3.14):
                            (x, y), radius = cv2.minEnclosingCircle(contours[i])
                            center = (int(x), int(y))
                            cv2.circle(img_Oimyoji,center, int(radius), (0, 0, 255), 2)
                            if center[0] > img_img_Oimyoji_w*0.86:
                                cv2.circle(img_Oimyoji, center, int(radius/1.5), (0, 255, 0), 2)
                                H11_Pos_x = center[0]
                                H11_Pos_y = center[1]
                                H11_R = radius/1.5

                    if H11_LC0_Avg > 57 and H11_LC0_Avg < 61 and flag_H11_LC == 0:
                        H11_LC0_Times += 1
                        if H11_LC0_Times > 15:
                            H11_LC0_Times = 0
                            time.sleep(random.uniform(0.1, 0.5))
                            Pos_random  = random.uniform(- (H11_R),H11_R)
                            Pos_x = H11_Pos_x +Pos_random
                            Pos_y = H11_Pos_y+Pos_random

                            self.SendMouse(hwnd,Pos_x,Pos_y)
                            flag_H11_LC = 1
                    else:
                        H11_LC0_Times = 0

                # 检测是否打完
                if flag_H11_LC == 1:
                    img_H11_IsFinish = img_Oimyoji_Origin.copy()
                    img_H11_B = img_H11_IsFinish[:, :, 2]
                    img_H11_2 = img_H11_B[0:int(img_img_Oimyoji_h *0.18),0:int(img_img_Oimyoji_w *.10)]
                    H11_2 = Image.fromarray(img_H11_2)
                    H11_LC01 = self.getImgHash(H11_2)
                    H11_LC2_Compare = self.getMH(H11_LC1, H11_LC01)
                    H11_LC2_Compare = round(H11_LC2_Compare, 3)

                    if H11_LC2_Compare>80:
                        H11_LC1_Times = H11_LC1_Times + random.uniform(0.8, 2.0)
                        if H11_LC1_Times > 30 * H11_LC1_Click:
                            H11_LC1_Click += 1
                            # time.sleep(random.uniform(0.05, 0.15))
                            Pos_random = random.uniform(1, int(img_img_Oimyoji_h *0.18))
                            Pos_x = int(img_img_Oimyoji_h *0.18)+Pos_random
                            Pos_y = Pos_random*1.56
                            self.SendMouse(hwnd, Pos_x, Pos_y)


                    else:
                        if H11_LC1_Click > 1:
                            H11_LC1_Click = 1
                            H11_LC1_Times = 0

                      

                    # img_H11_ROI2 = img_H11_B.copy()
                    # img_H11_ROI2.fill(255)
                    # cv2.rectangle(img_H11_ROI2, (int(img_img_Oimyoji_w * 0), int(img_img_Oimyoji_h * 0)),
                    #               (int(img_img_Oimyoji_w *.10), int(img_img_Oimyoji_h *0.18)), (0, 0, 0), -1)
                    # img_H11_Result2 = cv2.subtract(img_H11_B, img_H11_ROI2)



            # endregion

            # region 参数输出
            # 流程状态输出
            font = ImageFont.truetype(fontPath, int(h / 25))
            img_Pil = Image.fromarray(img_Oimyoji)
            draw = ImageDraw.Draw(img_Pil)
            fontText_Mod = "副本类型：" + self.cbx_FBLX.currentText()
            draw.text((10, int(h * para_Resize / 100) - int(h / 25 * 2.5)), fontText_Mod, font=font,
                      fill=(0, 255, 0))


            # 控制模式输出
            fontText_CtrlMod = "控制模式：" + self.cbx_KZMS.currentText()
            draw.text((10, int(h * para_Resize / 100) - int(h / 25 * 4)), fontText_CtrlMod, font=font,
                      fill=(0, 255, 0))

            # 采集参数输出
            txtOutpput_FPS = "FPS: " + str(para_Rate)
            txtOutpput_Resize = "缩放尺寸: (" + str(w * para_Resize / 100) + " x " + str(
                h * para_Resize / 100) + " )"
            draw.text((10, 20), txtOutpput_FPS, font=font, fill=(0, 255, 0))
            draw.text((10, 50), txtOutpput_Resize, font=font, fill=(0, 255, 0))

            if self.cbx_FBLX.currentIndex() == 1:
                txtH11Result =  "大蛇："+ str(H11_LC0_Avg) + " 结束 " + str(H11_LC2_Compare)
                draw.text((10, int(h * para_Resize / 100) - int(h / 25 * 8.5)), "魂十一检测值：", font=font, fill=(0, 255, 0))
                draw.text((10, int(h * para_Resize / 100) - int(h / 25 * 7)), txtH11Result, font=font, fill=(0, 255, 0))
                if H11_LC0_Avg > 57 and H11_LC0_Avg < 61 :
                    txth11_LC = "流程：巫女大蛇界面"
                elif H11_LC2_Compare > 95:
                    txth11_LC = "流程：结束页面"
                else:
                    txth11_LC = "流程：其他"
                draw.text((10, int(h * para_Resize / 100) - int(h / 25 * 5.5)), txth11_LC, font=font, fill=(0, 255, 0))

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
            # endregion

        # 输出控制信息
        # self.txt_Result.insertHtml(
        #     '<html><head/><body><p><span style=" color:WhiteSmoke;">&nbsp;&nbsp;' + rec__txt + '</span></p></body></html>')
        # self.txt_Result.insertPlainText("\n")
        # self.txt_Result.moveCursor(self.txt_Result.textCursor().End)  # 文本框显示到底部




    def SendMouse(self,hwnd,Pos_x,Pos_y):


        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        # 截图图片的宽
        w = int((right - left))
        # 截图图片的高
        h = int((bottom - top))

        m = PyMouse()
        # 随机延时，抖动
        tr = random.uniform(0.4, 0.7)

        if self.cbx_KZMS.currentIndex() == 0:
            x1 = left + Pos_x
            y1 = top + Pos_y
            # 获取当前鼠标位置
            currentMouseX, currentMouseY = pyautogui.position()
            # pyautogui.moveTo(int(x1), int(y1))
            # pyautogui.click()
            h = win32gui.GetForegroundWindow()
            win32gui.SetForegroundWindow(hwnd)
            m.click(int(x1), int(y1), 1)
            win32gui.SetForegroundWindow(h)
            m.move(currentMouseX, currentMouseY)

            # pyautogui.moveTo(currentMouseX, currentMouseY)

        elif self.cbx_KZMS.currentIndex() == 1:

            long_position = win32api.MAKELONG(int(Pos_x), int(Pos_y))

            print(long_position)
            # # win32api.SendMessage(hwnd, win32con.MOUSEEVENTF_LEFTDOWN, win32con.MOUSEEVENTF_LEFTUP, long_position)

            # 点击左键
            win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)
            time.sleep(tr)
            # print(tr)
            win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, long_position)
            # time.sleep(0.05)
            # print(long_position)

    def H11(self):
        global flag_H11
        flag_H11 = 1

    # 获取灰度值
    def getGray(self,image_file):
        tmpls = []
        for h in range(0, image_file.size[1]):  # h
            for w in range(0, image_file.size[0]):  # w
                tmpls.append(image_file.getpixel((w, h)))
        return tmpls

    # 获取平均灰度值
    def getAvg(self, ls):
        # sum求和， len个数
        return sum(ls) / len(ls)

    # 比较100个字符有几个字符相同
    def getMH(self, a, b):
        dist = 0
        for i in range(0, len(a)):
            if a[i] == b[i]:
                dist += 1
        return (dist / len(a)) * 100

    # 获得图片相似度
    def getImgHash(self, pic):
        # 输入图像
        image_file = pic.copy()
        # 将图片缩小为12×12px
        image_file = image_file.resize((12, 12))
        # L为黑白模式
        image_file = image_file.convert("L")
        # 获取灰度，放到数组中
        Grayls = self.getGray(image_file)
        # 获取灰度平均值
        avg = self.getAvg(Grayls)
        # 接收1或0
        bitls = ''

        for h in range(1, image_file.size[1]-1):
            for w in range(1,image_file.size[0]-1):
                # 像素大于平均值的记为1，小于的记为0
                if image_file.getpixel((w,h)) >= avg:
                    bitls = bitls + '1'
                else:
                    bitls = bitls + '0'
        return bitls







