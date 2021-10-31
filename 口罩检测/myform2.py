# coding=gbk
"""
作者：川川
@时间  : 2021/10/30 15:52
群：970353786
"""
#视频检测系统逻辑功能设计
from form2 import Ui_Form
import numpy
import cv2
import csv
import sys, time
from detection import Mask_detect
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class MyDesiger(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyDesiger, self).__init__(parent)
        self.setupUi(self)
        self.star_show()
        self.info = [["姓名","学号","学院","口罩佩戴情况","日期"]]
        self.VideoTimer = Video()
        self.VideoTimer.changePixmap.connect(self.setImage)   #信号与槽函数连接
        self.VideoTimer.detectPixmap.connect(self.setDetect)  #信号与槽函数连接
        self.VideoTimer.run_over.connect(self.finish_detect)  #信号与槽函数连接
        self.VideoTimer.update_data.connect(self.add_data)    #信号与槽函数连接

    def shoot_play(self):#摄像头展示
        if self.name.text()=='' or self.ID.text()=='' or self.xueyuan.text()=='':#学生信息填写不完整，无法开始检测
            QMessageBox.information(self, '信息不完整', '请正确填写完整信息',QMessageBox.Yes)
        else:
            self.VideoTimer.working = True  # 使摄像和检测线程能工作
            self.VideoTimer.start()

    def frame_detect(self):#检测每一帧
        if self.VideoTimer.working:
            self.VideoTimer.setDetect()

    def detect_quit(self):#结束检测
        self.close()

    def getinfo(self):#导出检测情况登记文件
        with open('resource\\info.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in self.info:
                writer.writerow(row)
        QMessageBox.information(self, '导出成功', '文件保存路径为:resource\\info.csv', QMessageBox.Yes)

    def star_show(self):#初始化显示界面
        frame = QPixmap('resource\\sample.jpg').scaled(self.labelplay.width(), self.labelplay.height())
        self.labelplay.setPixmap(frame)#显示示例图片
        image = QPixmap('resource\\sample_detection.jpg').scaled(self.labeldete.width(), self.labeldete.height())
        self.labeldete.setPixmap(image)#显示示例图片
        paddlehub = QPixmap('resource\\paddlehub.png').scaled(self.labelpaddle.width(), self.labelpaddle.height())
        self.labelpaddle.setPixmap(paddlehub)#显示示例图片

    def finish_detect(self,kz):#检测完毕，弹出检测结果信息提示
        self.star_show()
        QMessageBox.information(self, '检测结果:', kz+'!!', QMessageBox.Yes)
        self.name.clear()
        self.ID.clear()
        self.xueyuan.clear()

    def add_data(self,kz):#检测完毕，记录表信息更新
        self.model.appendRow([
            QStandardItem(self.name.text()),
            QStandardItem(self.ID.text()),
            QStandardItem(self.xueyuan.text()),
            QStandardItem(kz),
            QStandardItem(time.strftime('%Y.%m.%d',time.localtime(time.time()))),
        ])
        self.info.append([self.name.text(), self.ID.text(), self.xueyuan.text(),kz,time.strftime('%Y.%m.%d',time.localtime(time.time()))])

    def setImage(self, frame):   #传送摄像头图像
        self.labelplay.setPixmap(QPixmap.fromImage(QImage(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),640/2,480/2,13)))

    def setDetect(self, image):  #传送检测情况图像
        self.labeldete.setPixmap(QPixmap.fromImage(QImage(cv2.cvtColor(image, cv2.COLOR_BGR2RGB),640/2,480/2,13)))

class Video(QThread):
    changePixmap = pyqtSignal(numpy.ndarray)  #设置摄像头图像触发信号
    detectPixmap = pyqtSignal(numpy.ndarray)  #设置检测图像触发信号
    update_data = pyqtSignal(str)             #设置信息更新信号
    run_over = pyqtSignal(str)                #设置检测完毕信号
    def __init__(self):
        QThread.__init__(self)
        self.detect = False   #是否能检测
        self.working = False  #是否能工作
        self.count = 0        #检测到人脸的次数

    def run(self):
        cap = cv2.VideoCapture(0)  #打开摄像头
        while self.working:        #循环读取图像
            ret, frame = cap.read()
            frame = cv2.resize(frame,(320,240))
            self.changePixmap.emit(frame)  #显示图像
            if self.detect:
                img = frame.copy()
                detected_image,num,kz=Mask_detect(img)#口罩检测
                self.detectPixmap.emit(detected_image)#显示口罩检测结果
                if num > 0:
                    self.count += 1
            if self.count >= 6:#超过6帧检测到人脸就停止检测
                self.detect = False
                self.working = False
                self.count = 0  #计数清零
                self.run_over.emit(kz)#发射检测结束信号
                self.update_data.emit(kz)#发射信息更新信号
        cap.release()#释放摄像头资源

    def setDetect(self):
        self.detect = True
    def setquit(self):
        self.detect = False
        self.working = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MyDesiger()
    ui.show()
    sys.exit(app.exec_())
